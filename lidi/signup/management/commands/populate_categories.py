from django.core.management.base import BaseCommand
from signup.models import Category


class Command(BaseCommand):
    def _create_tags(self):
        category = Category(name="Apprentice")
        category.save()

        category = Category(name="Jedi")
        category.save()

    def handle(self, *args, **options):
        self._create_tags()
