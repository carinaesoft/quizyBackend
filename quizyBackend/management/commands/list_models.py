from django.core.management.base import BaseCommand
from django.apps import apps


class Command(BaseCommand):
    help = 'List all models and their fields'

    def handle(self, *args, **options):
        for model in apps.get_models():
            self.stdout.write(self.style.SUCCESS(f'Model: {model.__name__}'))
            fields = model._meta.get_fields()
            for field in fields:
                self.stdout.write(f'  Field: {field.name} (Type: {field.get_internal_type()})')
