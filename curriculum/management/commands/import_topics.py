import json
from django.core.management.base import BaseCommand
from curriculum.models import Standard, Topic
from pathlib import Path

#find project root
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

#point to fixtures explicitly
FIXTURES_DIR = BASE_DIR / "fixtures"
TOPICS_JSON = FIXTURES_DIR / "math_topics.json"
TOPICS_MAP_JSON = FIXTURES_DIR / "topics_map.json"

class Command(BaseCommand):
    help = "Imports topics from JSON and attaches them to the correct Standard"

    def handle(self, *args, **kwargs):
        # Load all topics
        with open(TOPICS_JSON, "r", encoding="utf-8") as f:
            all_topics = {t["id"]: t for t in json.load(f)}

        # Load mapping
        with open(TOPICS_MAP_JSON, "r", encoding="utf-8") as f:
            mapping = json.load(f)

        created = 0
        for std_code, topic_ids in mapping.items():
            try:
                std = Standard.objects.get(code=std_code)
            except Standard.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"⚠ No Standard found for code {std_code}, skipping..."))
                continue

            for topic_id in topic_ids:
                topic_data = all_topics.get(topic_id)
                if not topic_data:
                    self.stdout.write(self.style.WARNING(f"⚠ No topic found for ID {topic_id}, skipping..."))
                    continue

                title = topic_data["title"]
                desc = topic_data["description"]

                obj, created_topic = Topic.objects.get_or_create(
                    standard=std,
                    title=title,
                    defaults={"description": desc}
                )
                if created_topic:
                    created += 1
                    self.stdout.write(self.style.SUCCESS(f"✓ Linked {title} → {std_code}"))

        self.stdout.write(self.style.SUCCESS(f"Done! {created} topics linked."))
