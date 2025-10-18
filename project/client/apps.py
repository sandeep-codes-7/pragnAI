from django.apps import AppConfig
import os
import mongoengine

class ClientConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'client'

    def ready(self):
        # connect once when Django app registry is ready (development)
        mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/techblogs')
        # safe: avoid reconnecting if already connected
        try:
            # use alias 'default' by default
            mongoengine.connect(host=mongo_uri, alias='default')
        except Exception:
            # swallow or log in production; during dev you may want error surface
            pass