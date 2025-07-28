from .models import SkillSet, UserSkillProgress

def has_mastered_standard(user, standard):
    skillsets = SkillSet.objects.filter(related_standards=standard).distinct()
    for skillset in skillsets:
        progress = UserSkillProgress.objects.filter(user =user, skill_set = skillset, is_mastered=True).exists()
        if not progress:
            return False

    return True