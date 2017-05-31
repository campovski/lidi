from django.core.management.base import BaseCommand
from signup.models import ProgrammingLanguage


class Command(BaseCommand):
	def _create_tags(self):
		language = ProgrammingLanguage(name="C")
		language.save()

		language = ProgrammingLanguage(name="C++")
		language.save()

		language = ProgrammingLanguage(name="Pascal")
		language.save()

		language = ProgrammingLanguage(name="Python 2")
		language.save()

		language = ProgrammingLanguage(name="Python 3")
		language.save()

		language = ProgrammingLanguage(name="Java")
		language.save()

		language = ProgrammingLanguage(name="C#")
		language.save()

		language = ProgrammingLanguage(name="Fortran")
		language.save()

	def handle(self, *args, **options):
		self._create_tags()
