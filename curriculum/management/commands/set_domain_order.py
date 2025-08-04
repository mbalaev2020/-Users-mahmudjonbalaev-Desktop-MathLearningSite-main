import re
import unicodedata
from pathlib import Path
from django.core.management.base import BaseCommand
from curriculum.models import Grade, Domain

CURRICULUM_FILE = "Curriculum.txt"

# Match domains like "1. Algebra" or "* Algebra"
DOMAIN_RE = re.compile(r"^(?:\d+\.\s+|\*\s+)(.+)$")

class Command(BaseCommand):
    help = "Sets the sort_order field for Domain objects based on Curriculum.txt"

    def handle(self, *args, **kwargs):
        text = Path(CURRICULUM_FILE).read_text(encoding="utf-8")
        text = unicodedata.normalize("NFC", text).replace("\ufeff", "").replace("\xa0", "")

        current_grade = None
        domain_position = 0

        for raw_line in text.splitlines():
            line = raw_line.strip()
            if not line:
                continue

            # SHSAT → Grade 9
            if line.upper() == "SHSAT":
                current_grade = Grade.objects.get(level=9)
                domain_position = 0
                self.stdout.write(self.style.MIGRATE_HEADING("Found SHSAT (Grade 9)"))
                continue

            # SAT → Grade 10
            if line.upper() == "SAT":
                current_grade = Grade.objects.get(level=10)
                domain_position = 0
                self.stdout.write(self.style.MIGRATE_HEADING("Found SAT (Grade 10)"))
                continue

            # Detect "Grade 3", "Grade 6", etc.
            if line.lower().startswith("grade"):
                level = int(re.search(r"\d+", line).group(0))
                current_grade = Grade.objects.get(level=level)
                domain_position = 0
                self.stdout.write(self.style.MIGRATE_HEADING(f"Found Grade {level}"))
                continue

            # Detect domain names like "1. Fractions" or "* Fractions"
            d_match = DOMAIN_RE.match(line)
            if d_match and current_grade:
                domain_position += 1
                domain_name = d_match.group(1).strip()

                try:
                    domain = Domain.objects.get(grade=current_grade, name=domain_name)
                    domain.sort_order = domain_position
                    domain.save()
                    self.stdout.write(self.style.SUCCESS(
                        f"✔ Grade {current_grade.level}: '{domain_name}' → sort_order {domain_position}"
                    ))
                except Domain.DoesNotExist:
                    self.stdout.write(self.style.WARNING(
                        f"⚠ Domain not found in DB: '{domain_name}' (Grade {current_grade.level})"
                    ))

        self.stdout.write(self.style.SUCCESS("✅ All domain sort_orders updated."))
