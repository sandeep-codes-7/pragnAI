from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
# from client.models import BlogPost
from client.models import User

SAMPLE = [
    {
        # "title": "Getting started with AI blogging",
        # "category_or_subject": "AI",
        # "content": "A quick guide to get started with AI-powered blogging and tools.",
        # "author": "Sandeep",
        # "tags": ["ai", "blogging", "guide"],
        # "comments": ["you are good",],
        "name": "Sandeep",
        "username": "sandeep",
        "password": "90909",
        "username": "san_90"
    },
    # {
    #     "title": "Performance tuning for Django apps",
    #     "category_or_subject": "Performance",
    #     "content": "Tips and tricks to optimize Django apps for production.",
    #     "author": "Sandeep",
    #     "tags": ["django", "performance", "ops"],
    #     "comments": ["you are good",],
    # },
    # {
    #     "title": "Designing interactive UI with Tailwind",
    #     "category_or_subject": "Frontend",
    #     "content": "How to build modern interactive UI quickly using TailwindCSS.",
    #     "author": "Sandeep",
    #     "tags": ["tailwind", "ui", "css"],
    #     "comments": ["you are good",],
    # },
    # {
    #     "title": "Deploying with Docker and Compose",
    #     "category_or_subject": "DevOps",
    #     "content": "A practical Docker + Compose workflow for small Django projects.",
    #     "author": "Sandeep",
    #     "tags": ["docker", "deploy", "devops"],
    #     "comments": ["you are good",],
    # },
    # {
    #     "title": "N/A",
    #     "category_or_subject": "N/A",
    #     "content": "N/A",
    #     "author": "N/A",
    #     "tags": [],#["docker", "deploy", "devops"]
    #     "comments": ["you are empty",],
    # },
]

class Command(BaseCommand):
    help = "Seed sample BlogPost documents into MongoDB (mongoengine)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear", action="store_true", help="Remove existing blog_posts collection before seeding"
        )

    def handle(self, *args, **options):
        if options["clear"]:
            self.stdout.write("Clearing existing blog_posts collection...")
            User.drop_collection()

        now = datetime.utcnow()
        created = []
        for i, item in enumerate(SAMPLE, start=1):
            doc = User(
                # title=item["title"],
                # category_or_subject=item["category_or_subject"],
                # content=item["content"],
                # author=item.get("author", ""),
                # tags=item.get("tags", []),
                # created_at=now - timedelta(days=(len(SAMPLE) - i)),
                # comments=item.get("comments", [])
                name=item["name"],
                username=item["username"],
                password=item["password"],
                email=item["username"],
                # username=item.get("username", "")
            )
            doc.save()
            created.append(str(doc.id))

        self.stdout.write(self.style.SUCCESS(f"Seeded {len(created)} posts. IDs: {', '.join(created)}"))

