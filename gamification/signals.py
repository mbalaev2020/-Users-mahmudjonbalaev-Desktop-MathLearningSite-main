from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from .models import LoginStreak, GardenState, UserProgress, Plant
from curriculum.models import Domain #categories

User = get_user_model()

@receiver(post_save, sender=User)
def create_gamification_data(sender, instance, created, **kwargs):
    if not created:
        return

    user = instance

    #create login streak
    LoginStreak.objects.get_or_create(user = user)

    #create garden streak
    GardenState.objects.get_or_create(user = user)

    #create one UserProgfress and plant per category
    domains = Domain.objects.all()
    for domain in domains:
        slug = domain.slug
        UserProgress.objects.get_or_create(user = user, category = slug)
        Plant.objects.get_or_create(user = user, category = slug)