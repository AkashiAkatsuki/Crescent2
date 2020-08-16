from django.apps import AppConfig
from django.db.models.signals import post_migrate
from apps.api.models import Word


class ApiConfig(AppConfig):
    name = 'api'

    def ready(self):
        post_migrate.connect(
            self.init_table,
            sender=self
        )
    
    def init_table(self):
        Word.objects.get_or_create(id=-1, name="EOS", category=9)
