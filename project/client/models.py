from django.db import models
from datetime import datetime
from mongoengine import Document, StringField, DateTimeField, ListField, ImageField, IntField, EmailField


class Path(Document):
    title = StringField(required=True, max_length=200)
    # category_or_subject = StringField(required=True, max_length=100)
    content = StringField(required=True)
    # author = StringField(max_length=100)
    description = StringField(required=True, max_length=200)
    created_at = DateTimeField(default=datetime.now)
    tags = ListField(StringField(max_length=50))
    meta = {'collection': 'paths'}

    def __str__(self):
        return self.title or str(self.id)
    
class User(Document):
    exp = IntField(default=0)
    name = StringField(required=True, max_length=100)
    pic = ImageField()
    username = StringField(required=True, max_length=100)
    email = StringField(required=True, max_length=100)
    password = StringField(required=True, max_length=100)
    interests = ListField(StringField(max_length=50))
    created_at = DateTimeField(default=datetime.now)
    about = StringField(max_length=200)
    current_path = ListField(StringField(max_length=200))
    completed_paths = ListField(StringField(max_length=200))
    meta = {'collection': 'users'}
    def __str__(self):
        return self.username or str(self.id)
    
class ForNewsLetter(Document):
    email = EmailField()