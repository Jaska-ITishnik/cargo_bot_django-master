import os

from django.apps import AppConfig


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

    def ready(self):
        if os.environ.get('RUN_MAIN') == 'true':  # This ensures it only runs in the main process
            from app.scheduler_utils import start_scheduler
            print('Starting scheduler...')
            start_scheduler()
