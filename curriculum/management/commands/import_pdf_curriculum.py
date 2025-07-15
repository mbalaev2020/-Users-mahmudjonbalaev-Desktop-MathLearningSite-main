import re
from pathlib import Path
from django.core.management.base import BaseCommand
from curriculum.models import Grade, Domain, Standard

PDF_TEXT_FILE = "Curriculum.txt"  # Make sure this is saved as plain text in your root or app directory

# Patterns
GRADE_HEADER_RE = re.compile(r"Grade (\d+)")
DOMAIN_LINE_RE = re.compile(r"^\d+\.\s+(.+)$")               # e.g., "1. Operations and Algebraic Thinking"
SUBSKILL_LINE_RE = re.compile(r"^[\u2022\-]\s+(.+)$")       # bullets: • or -

class Command(BaseCommand):
    help = "Imports curriculum from a .txt file into Grade, Domain, and Standard models."

    def handle(self, *args, **options):
        try:
            text = Path(PDF_TEXT_FILE).read_text(encoding="utf-8")
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"Could not find file: {PDF_TEXT_FILE}"))
            return

        current_grade = None
        domain = None
        created_domains = 0
        created_standards = 0

        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue

            # Detect grade header
            g_match = GRADE_HEADER_RE.match(line)
            if g_match:
                level = int(g_match.group(1))
                current_grade, _ = Grade.objects.get_or_create(level=level)
                self.stdout.write(self.style.MIGRATE_HEADING(f"Grade {level} found"))
                continue

            # Detect domain
            d_match = DOMAIN_LINE_RE.match(line)
            if d_match and current_grade:
                domain_title = d_match.group(1).strip()
                domain, dom_created = Domain.objects.get_or_create(
                    grade=current_grade,
                    name=domain_title,
                    defaults={"slug": re.sub(r"\W+", "-", domain_title.lower())[:120]},
                )
                if dom_created:
                    created_domains += 1
                    self.stdout.write(self.style.SUCCESS(f"  + Domain created: {domain_title}"))

                continue  # Wait for bullet point sub-skills to follow

            # Detect subskill line
            s_match = SUBSKILL_LINE_RE.match(line)
            if s_match and current_grade and domain:
                skill_title = s_match.group(1).strip()

                next_standard_num = domain.standards.count() + 1
                std_code = f"{current_grade.level}.{domain.id:02d}.{next_standard_num:02d}"

                _, std_created = Standard.objects.get_or_create(
                    domain=domain,
                    code=std_code,
                    defaults={"description": skill_title},
                )
                if std_created:
                    created_standards += 1
                    self.stdout.write(self.style.NOTICE(f"    - Sub-skill added: {std_code} → {skill_title}"))
                continue

        # Final output
        self.stdout.write(self.style.SUCCESS(
            f"\n✔ Import complete!\n  → {created_domains} domains created\n  → {created_standards} standards created"
        ))