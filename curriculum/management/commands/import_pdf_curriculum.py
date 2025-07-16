import re
import unicodedata
from pathlib import Path
from django.core.management.base import BaseCommand
from curriculum.models import Grade, Domain, Standard

PDF_TEXT_FILE = "Curriculum.txt"  # Make sure this is saved as plain text in your root or app directory

# Flexible pattern for domains
DOMAIN_FLEX_RE = re.compile(r"^\s*\d+\s*[\.\)]\s*(.+)$")  # matches "1. Something" or "1) Something"

class Command(BaseCommand):
    help = "Imports curriculum from a .txt file into Grade, Domain, and Standard models."

    def handle(self, *args, **options):
        try:
            #  Read text & clean BOM + hidden unicode spaces
            raw_text = Path(PDF_TEXT_FILE).read_text(encoding="utf-8")
            text = unicodedata.normalize("NFKC", raw_text)      # normalize weird Unicode (① → 1)
            text = text.replace("\ufeff", "").replace("\xa0", " ")  # remove BOM & non-breaking spaces
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"Could not find file: {PDF_TEXT_FILE}"))
            return

        current_grade = None
        current_domain = None
        created_domains = 0
        created_standards = 0

        for raw_line in text.splitlines():
            line = raw_line.strip()
            if not line:
                continue

            #  Detect Grade
            if line.lower().startswith("grade"):
                level = int(re.search(r"\d+", line).group(0))
                current_grade, _ = Grade.objects.get_or_create(level=level)
                self.stdout.write(self.style.MIGRATE_HEADING(f"Grade {level} found"))
                current_domain = None  # reset domain when new grade starts
                continue

            #Detect SHSAT AND SAT
            if line.startswith("SHSAT"):
                current_grade, _ = Grade.objects.get_or_create(level=9)
                current_grade.display_name = "SHSAT"
                current_grade.save()
                self.stdout.write(self.style.MIGRATE_HEADING("SHSAT found"))
                current_domain = None
                continue

            if line.startswith("SAT"):
                current_grade, _ = Grade.objects.get_or_create(level=10)
                current_grade.display_name = "SAT"
                current_grade.save()
                self.stdout.write(self.style.MIGRATE_HEADING("SAT found"))
                current_domain = None
                continue

            #  Detect Domain normally (starts with digit + dot or digit + ) )
            if current_grade:
                d_match = DOMAIN_FLEX_RE.match(line)
                if d_match:
                    domain_title = d_match.group(1).strip()
                    current_domain, dom_created = Domain.objects.get_or_create(
                        grade=current_grade,
                        name=domain_title,
                        defaults={"slug": re.sub(r"\W+", "-", domain_title.lower())[:120]},
                    )
                    if dom_created:
                        created_domains += 1
                        self.stdout.write(self.style.SUCCESS(f"  + Domain created: {domain_title}"))
                    continue

            #  Fallback Domain detection (if we’re inside a grade, not a bullet, not another grade)
            if current_grade and not line.startswith("*") and not line.lower().startswith("grade") and len(line.split()) > 2:
                current_domain, dom_created = Domain.objects.get_or_create(
                    grade=current_grade,
                    name=line,
                    defaults={"slug": re.sub(r"\W+", "-", line.lower())[:120]},
                )
                if dom_created:
                    created_domains += 1
                    self.stdout.write(self.style.WARNING(f"  + [Fallback] Domain created: {line}"))
                continue

            #  Detect Standards (starts with *)
            if current_grade and current_domain and line.startswith("*"):
                skill_title = line.lstrip("* ").strip()

                next_standard_num = current_domain.standards.count() + 1
                std_code = f"{current_grade.level}.{current_domain.id:02d}.{next_standard_num:02d}"

                _, std_created = Standard.objects.get_or_create(
                    domain=current_domain,
                    code=std_code,
                    defaults={"description": skill_title},
                )
                if std_created:
                    created_standards += 1
                    self.stdout.write(self.style.NOTICE(f"    - Sub-skill added: {std_code} → {skill_title}"))
                continue

        #  Final output summary
        self.stdout.write(self.style.SUCCESS(
            f"\nImport complete!\n  → {created_domains} domains created\n  → {created_standards} standards created"
        ))
