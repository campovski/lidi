from django.core.management.base import BaseCommand
from signup.models import Language


class Command(BaseCommand):
	def _create_tags(self):
		language = Language(name="English")
		language.save()

		language = Language(name="German")
		language.save()

	def handle(self, *args, **options):
		self._create_tags()
