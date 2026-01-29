from rest_framework import serializers
from .models import Plant, UserProgress, LoginStreak, Badge, GardenState
from curriculum.models import Domain
from assessments.models import Test
from practice.models import SkillSet

class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = ['category', 'growth_stage']

class UserProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProgress
        fields = ['category', 'percent_complete', 'skills_mastered']

class LoginStreakSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginStreak
        fields = ['current_streak', 'longest_streak']

class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = ['badge_type', 'unlocked_on']

class GardenStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = GardenState
        fields = ['health_score', 'visual_theme']

class CategorySerializer(serializers.ModelSerializer):
    grade = serializers.SerializerMethodField()

    class Meta:
        model = Domain
        fields = ['slug', 'name', 'grade']

    def get_grade(self, obj):
        return obj.grade.__str__()

class SkillSetProgressSerializer(serializers.ModelSerializer):
    completed = serializers.SerializerMethodField()

    class Meta:
        model = SkillSet
        fields = ['id', 'title', 'completed']

    def get_completed(self, obj):
        user = self.context['request'].user
        return obj.is_completed_by(user)

class TestProgressSerializer(serializers.ModelSerializer):
    skillsets = serializers.SerializerMethodField()
    unlocked = serializers.SerializerMethodField()

    class Meta:
        model = Test
        fields = ['id', 'title', 'unlocked', 'skillsets']

    def get_unlocked(self, obj):
        return obj.is_unlocked_for(self.context['request'].user)

    def get_skillsets(self, obj):
        skillsets = SkillSet.objects.filter(related_standards__in = obj.standards.all())
        return SkillSetProgressSerializer(skillsets, many=True, context = self.context).data
    def is_unlocked_for(self, user):
        return True