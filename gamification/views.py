from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from datetime import date, datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from assessments.models import Test
from practice.models import PracticeQuestion , SkillSet
from practice.utils import evaluate_skillset_readiness, evaluate_test_readiness
from curriculum.models import Domain
from .models import (
    UserProgress,
    Plant,
    LoginStreak,
    Badge,
    GardenState
)
from .serializers import (
    PlantSerializer,
    LoginStreakSerializer,
    BadgeSerializer,
    GardenStateSerializer,
    CategorySerializer,
    TestProgressSerializer
)

@login_required(login_url='/login/')
def dashboard_page(request):
    user = request.user

    # Test progress + test readiness
    tests = Test.objects.all()
    test_progress = []
    for test in tests:
        progress = TestProgressSerializer(test, context={"request": request}).data
        progress["readiness"] = evaluate_test_readiness(user, test)  # ✅ add readiness status
        test_progress.append(progress)

    # SkillSet readiness (unchanged)
    skillsets = SkillSet.objects.all()
    skillset_status = [
        {
            "id": s.id,
            "title": s.title,
            "readiness": evaluate_skillset_readiness(user, s)
        }
        for s in skillsets
    ]

    return render(request, "gamification/dashboard.html", {
        "test_progress": test_progress,
        "skillset_status": skillset_status
    })

class DashboardAPIView(APIView):
    permission_classes = [IsAuthenticated] #Only logged in users

    def get(self, request):
        user = request.user

        #Get all plants
        plants = Plant.objects.filter(user=user)
        plant_data = PlantSerializer(plants, many = True).data

        #Get streaks (if exists)
        try:
            streak = LoginStreak.objects.get(user=user)
            streak_data = LoginStreakSerializer(streak).data
        except LoginStreak.DoesNotExist:
            streak_data = {'current_streak': 0, 'longest_streak': 0}

        #Get badges earned
        badges = Badge.objects.filter(user=user)
        badges_data = BadgeSerializer(badges, many = True).data

        #get garden state
        try:
            garden = GardenState.objects.get(user=user)
            garden_data = GardenStateSerializer(garden).data
        except GardenState.DoesNotExist:
            garden_data = {'health_score': 100, 'visual_theme': 'default'}

        #build and return combined response
        return Response({
            'plants': plant_data,
            'streaks': streak_data,
            'badges': badges_data,
            'garden': garden_data,
        })



class StreakUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        today = date.today()

    #get or create a streak record

        streak , created = LoginStreak.objects.get_or_create(user = user)

    #if brand new start the streak
        if created or streak.last_login is None:
            streak.current_streak = 1
        else:
            days_since = (today - streak.last_login).days

            if days_since == 1:
                streak.current_streak +=1
            elif days_since > 1:
                streak.current_streak = 1 # streak broken
        #if 0, same day login dont increment again


        if streak.current_streak > streak.longest_streak:
            streak.longest_streak = streak.current_streak

        streak.last_login = today
        streak.save()

        return Response({
            "status": "success",
            "data": {
                "current_streak": streak.current_streak,
                "longest_streak": streak.longest_streak
            }
        })




class ProgressUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        category = request.data.get("category")
        skill_mastered = request.data.get("skill_mastered", False)

        if not category:
            return Response({
                "status": "error",
                "message": "Category is required."
            }, status=400)

        if not Domain.objects.filter(slug=category).exists():
            return Response({
                "status": "error",
                "message": "Invalid category."
            }, status=400)

        try:
            # Get or create the UserProgress record
            progress, _ = UserProgress.objects.get_or_create(user=user, category=category)

            if skill_mastered:
                progress.skills_mastered += 1

            # Get total skills based on domain
            domain = Domain.objects.get(slug=category)
            total_skills = PracticeQuestion.objects.filter(
                skill_set__related_standards__domain=domain
            ).distinct().count()

            if total_skills == 0:
                total_skills = 1  # avoid divide-by-zero

            # Update progress
            progress.percent_complete = round((progress.skills_mastered / total_skills) * 100, 1)
            progress.last_updated = datetime.now()
            progress.save()

            # Update plant growth
            plant, _ = Plant.objects.get_or_create(user=user, category=category)
            percent = progress.percent_complete

            if percent >= 100:
                stage = "bloomed"
            elif percent >= 50:
                stage = "budding"
            elif percent > 0:
                stage = "seedling"
            else:
                stage = "seedling"

            plant.growth_stage = stage
            plant.save()

            return Response({
                "status": "success",
                "data": {
                    "updated_progress": {
                        "category": category,
                        "percent_complete": progress.percent_complete,
                        "skills_mastered": progress.skills_mastered
                    },
                    "new_stage": stage
                }
            })

        except Exception as e:
            return Response({
                "status": "error",
                "message": str(e)
            }, status=500)



class BadgeListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        badges = Badge.objects.filter(user=user)
        serialized = BadgeSerializer(badges, many = True)
        return Response({
            "status": "success",
            "data": serialized.data
        })




class GardenView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        plants = Plant.objects.filter(user=user)
        serialized = PlantSerializer(plants, many=True)
        return Response({
            "status": "success",
            "data": serialized.data
        })

class CategoryListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        domains = Domain.objects.all()
        serialized = CategorySerializer(domains, many = True)
        return Response({
            "status": "success",
            "data": serialized.data
        })

class TestProgressView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, test_id):
        test = Test.objects.get(pk = test_id)
        serializer = TestProgressSerializer(test, context={'request': request})
        return Response(serializer.data)

class AllTestProgressAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        tests = Test.objects.all()
        progress_data = [
            TestProgressSerializer(test, context = {"request": request}).data
            for test in tests
        ]
        return Response(progress_data)