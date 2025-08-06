from .models import SkillSet, UserSkillProgress, Attempt

def has_mastered_standard(user, standard):
    skillsets = SkillSet.objects.filter(related_standards=standard).distinct()
    for skillset in skillsets:
        progress = UserSkillProgress.objects.filter(user =user, skill_set = skillset, is_mastered=True).exists()
        if not progress:
            return False

    return True

def evaluate_skillset_readiness(user, skillset):
    # All attempts for this user + skillset
    attempts = Attempt.objects.filter(user=user, question__skill_set=skillset)

    # Unique questions attempted
    question_ids = attempts.values_list("question_id", flat=True).distinct()
    total_questions = question_ids.count()

    correct_attempts = attempts.filter(is_correct=True).count()
    total_attempts = attempts.count()

    avg_attempts_per_question = total_attempts / total_questions if total_questions else 0
    accuracy = correct_attempts / total_attempts if total_attempts else 0

    if avg_attempts_per_question > 2 or accuracy < 0.7:
        return "needs_review"
    return "ready"
