from django.core.management.base import BaseCommand

from vacancies.handlers import clean_expired_vacancies


class Command(BaseCommand):
    help = 'Delete old vacancies'

    def handle(self, *args, **kwargs):
        clean_expired_vacancies()