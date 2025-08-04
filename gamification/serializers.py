from rest_framework import serializers
from .models import Plant, UserProgress, LoginStreak, Badge, GardenState
from curriculum.models import Domain

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
        return str(obj.grade)


