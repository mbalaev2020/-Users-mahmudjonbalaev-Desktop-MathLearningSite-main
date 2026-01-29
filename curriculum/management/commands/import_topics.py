import json
from django.core.management.base import BaseCommand
from curriculum.models import Standard, Topic  # ensure Topic exists in curriculum.models
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
FIXTURES_DIR = BASE_DIR / "fixtures"
TOPICS_JSON = FIXTURES_DIR / "math_topics.json"
TOPICS_MAP_JSON = FIXTURES_DIR / "topics_map.json"

class Command(BaseCommand):
    help = "Imports topics from JSON and attaches them to the correct Standard"

    def handle(self, *args, **kwargs):
        with open(TOPICS_JSON, "r", encoding="utf-8") as f:
            all_topics = {t["id"]: t for t in json.load(f)}

        with open(TOPICS_MAP_JSON, "r", encoding="utf-8") as f:
            mapping = json.load(f)

        created = 0
        updated = 0

        for std_code, topic_ids in mapping.items():
            std = Standard.objects.filter(code=std_code).first()
            if not std:
                self.stdout.write(self.style.WARNING(f"⚠ No Standard found for code {std_code}, skipping..."))
                continue

            for topic_id in topic_ids:
                data = all_topics.get(str(topic_id)) or all_topics.get(topic_id)
                if not data:
                    self.stdout.write(self.style.WARNING(f"⚠ Topic id {topic_id} missing in math_topics.json"))
                    continue

                # Fields expected: title, description (adjust to your Topic model)
                obj, was_created = Topic.objects.update_or_create(
                    external_id=str(topic_id),  # if your Topic has this; else use unique_together on (standard,title)
                    defaults={
                        "standard": std,
                        "title": data.get("title", f"Topic {topic_id}"),
                        "description": data.get("description", ""),
                    },
                )
                created += int(was_created)
                updated += int(not was_created)

        self.stdout.write(self.style.SUCCESS(f"✅ Topics import complete: created={created}, updated={updated}"))
