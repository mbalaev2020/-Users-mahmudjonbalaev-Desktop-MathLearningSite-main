import random
import re
from pathlib import Path
from django.core.management.base import BaseCommand
from PyPDF2 import PdfReader

from curriculum.models import Standard
from practice.models import SkillSet, PracticeQuestion, Attempt

class Command(BaseCommand):
    help = "Import a multiplication PDF as PracticeQuestions under a SkillSet"

    def add_arguments(self, parser):
        parser.add_argument("pdf_path", type=str, help="Path to the PDF")
        parser.add_argument("--skillset", type=str, required=True, help="Name of the SkillSet")
        parser.add_argument("--standard-code", type=str, help="Exact Standard code like 3.01.01")
        parser.add_argument("--reset", action="store_true", help="Clear existing questions & attempts first")

    def handle(self, *args, **options):
        pdf_path = options["pdf_path"]
        skillset_title = options["skillset"]
        standard_code = options.get("standard_code")
        reset_flag = options["reset"]

        # check if PDF exists
        if not Path(pdf_path).exists():
            self.stdout.write(self.style.ERROR("PDF not found"))
            return

        # extract text from PDF
        reader = PdfReader(pdf_path)
        pdf_text = '\n'.join(page.extract_text() for page in reader.pages)

        # parse multiplication problems like: 1) 6 × 7
        problem_lines = re.findall(r"\d+\)\s+(\d+)\s+×\s+(\d+)", pdf_text)
        if not problem_lines:
            self.stdout.write(self.style.ERROR("No problems found"))
            return

        parsed_problems = [(int(a), int(b), int(a) * int(b)) for a, b in problem_lines]

        # find Standard by exact code
        try:
            if standard_code:
                standard = Standard.objects.get(code=standard_code)
            else:
                self.stdout.write(self.style.ERROR("You must pass --standard-code."))
                return
        except Standard.MultipleObjectsReturned:
            self.stdout.write(self.style.ERROR(
                f"Multiple standards found with code '{standard_code}'. Please make sure it's unique."
            ))
            return
        except Standard.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Standard with code '{standard_code}' not found!"))
            return

        # find or create SkillSet
        skillset, created = SkillSet.objects.get_or_create(
            title=skillset_title,
            defaults={"description": f"Auto-imported from {Path(pdf_path).name}"}
        )
        skillset.related_standards.add(standard)

        # optional: reset existing questions + attempts
        if reset_flag:
            count_q = skillset.practice_questions.count()
            count_a = Attempt.objects.filter(question__skill_set=skillset).count()
            skillset.practice_questions.all().delete()
            Attempt.objects.filter(question__skill_set=skillset).delete()
            self.stdout.write(self.style.WARNING(f"Reset: Deleted {count_q} questions and {count_a} attempts."))

        # insert practice questions
        created_count = 0
        skipped_count = 0
        for a, b, correct in parsed_problems:
            question_text = f"What is {a} x {b}?"

            # prevent duplicates
            if PracticeQuestion.objects.filter(skill_set=skillset, question_text=question_text).exists():
                skipped_count += 1
                continue

            # auto-generate 3 wrong answers
            wrongs = set()
            while len(wrongs) < 3:
                wrong_candidate = correct + random.randint(-10, 10)
                if wrong_candidate > 0 and wrong_candidate != correct:
                    wrongs.add(wrong_candidate)
            wrongs = list(wrongs)

            # mix choices
            all_choices = wrongs + [correct]
            random.shuffle(all_choices)
            correct_index = all_choices.index(correct)
            correct_letter = ['A', 'B', 'C', 'D'][correct_index]

            # save question
            PracticeQuestion.objects.create(
                skill_set=skillset,
                question_text=question_text,
                choice_a=str(all_choices[0]),
                choice_b=str(all_choices[1]),
                choice_c=str(all_choices[2]),
                choice_d=str(all_choices[3]),
                correct_answer=correct_letter,
                explanation_text=f"Correct answer is {a} x {b} = {correct}"
            )
            created_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"Finished! Created {created_count} new questions into SkillSet '{skillset.title}'. Skipped {skipped_count} duplicates."
        ))
