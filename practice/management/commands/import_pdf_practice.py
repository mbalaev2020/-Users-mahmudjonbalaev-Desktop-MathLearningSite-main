import random
import re
from pathlib import Path
from django.core.management.base import BaseCommand
from PyPDF2 import PdfReader


from curriculum.models import Standard
from practice.models import SkillSet, PracticeQuestion

class Command(BaseCommand):

    help = "Import a multiplication PDF as PracticeQuestions under a SkillSet "

#command argurments
    def add_arguments(self, parser):
        parser.add_argument("pdf_path", type=str, help="Path to the PDF")
        parser.add_argument("--skillset", type=str, required=True, help="Name of the SkillSet")
        parser.add_argument("--standard", type=str, required=True,  help="Name of Standard")


    def handle(self, *args, **options):
        pdf_path = options["pdf_path"]
        skillset_title = options["skillset"]
        standard_name = options["standard"]

        #check if pdf exists
        if not Path(pdf_path).exists():
            self.stdout.write(self.style.ERROR("PDF not found"))
            return

        #extract from pdf
        reader = PdfReader(pdf_path)
        pdf_text = '\n'.join(page.extract_text() for page in reader.pages)

        # parse problems like 1) 2)
        problem_lines = re.findall(r"\d+\)\s+(\d+)\s+×\s+(\d+)", pdf_text)
        if not problem_lines:
            self.stdout.write(self.style.ERROR("No problems found"))
            return

        parsed_problems = [(int(a), int(b), int(a) * int(b)) for a, b in problem_lines]

        #find standard
        try:
            standard = Standard.objects.get(description__icontains=standard_name)
        except Standard.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Standard '{standard_name}' not found! Create it first."))
            return

        #find or create skillset
        skillset, created = SkillSet.objects.get_or_create(
            title=skillset_title,
            defaults={"description": f"Auto-imported from {Path(pdf_path).name}"}
        )
        skillset.related_standards.add(standard)

        #insert practice questions
        created_count = 0
        for a,b, correct in parsed_problems:
            #question text
            question_text = f"What is {a} x {b}?"

            #auto generate 3 wrong answers
            wrongs = set()
            while len(wrongs) < 3:
                wrong_candidate = correct + random.randint(-10,10)
                if wrong_candidate > 0 and wrong_candidate != correct:
                    wrongs.add(wrong_candidate)
            wrongs=list(wrongs)

            #combine correct + wrong answers
            all_choices = list(wrongs) + [correct]
            random.shuffle(all_choices)

            #determine correct
            correct_index = all_choices.index(correct)
            correct_letter = ['A', 'B', 'C', 'D'][correct_index]

            #save questions:
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

        self.stdout.write(self.style.SUCCESS(f"Created {created_count} questions into SkillSet '{skillset.title}'"))