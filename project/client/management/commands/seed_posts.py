from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
from client.models import Path

import os
import random
from client.models import User


SAMPLE = [
    {
        "title": "Django Basics",
        # "category_or_subject": "web dev",
        "content": "A quick guide to get started with Django.",
        "description": "Intro to Django and project setup.",
        "tags": ["django", "webdev", "backend"],
    },
    {
        "title": "REST APIs",
        # "category_or_subject": "backend",
        "content": "Designing and building RESTful APIs.",
        "description": "Best practices for API development.",
        "tags": ["api", "rest"],
    },
    {
        "title": "Frontend Essentials",
        # "category_or_subject": "frontend",
        "content": "HTML, CSS and modern JS fundamentals.",
        "description": "Fundamentals for building user interfaces.",
        "tags": ["html", "css", "javascript"],
    },
    {
        "title": "DevOps",
        # "category_or_subject": "frontend",
        "content": "Containerization, Docker, Kubernetes",
        "description": "Understanding DevOps",
        "tags": ["Devops", "Docker", "cloud"],
    },
]


USER_SAMPLE = [
    {
        "name": "Alice",
        "username": "alice99",
        "email": "alice@example.com",
        "password": "password123",
        "interests": ["frontend", "design"],
    },
    {
        "name": "Bob",
        "username": "bob_dev",
        "email": "bob@example.com",
        "password": "secret",
        "interests": ["backend", "databases"],
    },
    {
        "name": "Carol",
        "username": "carol_ai",
        "email": "carol@example.com",
        "password": "topsecret",
        "interests": ["ai", "ml"],
    },
]


class Command(BaseCommand):
    help = "Seed sample Path documents/rows (mongoengine Path Document)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear", action="store_true", help="Remove existing Path records before seeding"
        )

    def handle(self, *args, **options):
        # Clear existing records if requested
        if options.get("clear"):
            self.stdout.write("Clearing existing Path records...")
            try:
                # mongoengine Document has drop_collection
                if hasattr(Path, "drop_collection"):
                    Path.drop_collection()
                    self.stdout.write(self.style.SUCCESS("Dropped Path collection."))
                else:
                    # fallback (if Path were a Django model)
                    Path.objects.all().delete()
                    self.stdout.write(self.style.SUCCESS("Deleted Path objects (fallback)."))
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"Could not clear automatically: {e}"))

        now = datetime.utcnow()
        created_ids = []

        for i, item in enumerate(SAMPLE, start=1):
            created_at = item.get("created_at", now - timedelta(days=(len(SAMPLE) - i)))
            payload = {
                "title": item.get("title", "Untitled"),
                "content": item.get("content", ""),
                "description": item.get("description", ""),
                "created_at": created_at,
                "tags": item.get("tags", []),
            }

            try:
                # Construct and save a Path document (works with mongoengine Document)
                obj = Path(**payload)
                obj.save()
                obj_id = str(getattr(obj, "id", getattr(obj, "pk", "(unknown)")))
                created_ids.append(obj_id)
                self.stdout.write(self.style.SUCCESS(f"Created: {payload['title']} (id={obj_id})"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Failed to create '{payload.get('title','(no title)')}': {e}"))

        self.stdout.write(self.style.SUCCESS(f"Seeded {len(created_ids)} posts. IDs: {', '.join(created_ids)}"))

        # --- Seed Users ---
        self.stdout.write('\nSeeding demo users...')
        # determine local images to use for pic field
        static_img_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'static', 'images')
        local_images = []
        try:
            if os.path.isdir(static_img_dir):
                for f in os.listdir(static_img_dir):
                    if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.gif')):
                        local_images.append(os.path.join(static_img_dir, f))
        except Exception:
            local_images = []

        # fallback external animal images (unsplash / placeholder)
        # external_imgs = [
        #     'https://images.unsplash.com/photo-1518717758536-85ae29035b6d?w=800&q=80',
        #     'https://images.unsplash.com/photo-1504208434309-cb69f4fe52b0?w=800&q=80',
        #     'https://images.unsplash.com/photo-1517841905240-472988babdf9?w=800&q=80',
        # ]

        created_users = []
        for u in USER_SAMPLE:
            try:
                pic_choice = None
                if local_images:
                    # use relative path for static serving (Django staticfiles) if local
                    chosen = random.choice(local_images)
                    # convert to path relative to 'client/static' for storage (optional)
                    # use URL path starting from '/static/' so templates can show it
                    rel = os.path.relpath(chosen, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'static'))
                    pic_choice = '/static/' + rel.replace('\\', '/')
                else:
                    # pic_choice = random.choice(external_imgs)
                    pass

                user_payload = {
                    'name': u.get('name'),
                    'username': u.get('username'),
                    'email': u.get('email'),
                    'password': u.get('password'),
                    'interests': u.get('interests', []),
                    # 'pic': pic_choice,
                    'created_at': datetime.utcnow(),
                    'about': f"Hi, I'm {u.get('name')} and I like {', '.join(u.get('interests', []))}",
                }

                obj = User(**user_payload)
                obj.save()
                created_users.append(str(getattr(obj, 'id', getattr(obj, 'pk', '(unknown)'))))
                self.stdout.write(self.style.SUCCESS(f"Created user: {user_payload['username']} pic={pic_choice}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Failed to create user {u.get('username')}: {e}"))

        self.stdout.write(self.style.SUCCESS(f"Seeded {len(created_users)} users. IDs: {', '.join(created_users)}"))

