from django.core.management.base import BaseCommand, CommandError

from vacancies.jobparser.tasks import parse


class Command(BaseCommand):
    help = 'Run job parsers in separated workers'

    def handle(self, *args, **kwargs):
        # Спарсить вакансии
        parse()
