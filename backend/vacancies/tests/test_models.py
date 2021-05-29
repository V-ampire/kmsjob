from django.test import TestCase
import datetime

from ..models import Vacancy


class VacancyTestCase(TestCase):

    def setUp(self):
        self.current_date = datetime.datetime.now()
        self.vacancy = Vacancy.objects.create(
            name='test'
        )

    def test_get_todays_vacancies(self):
        vacancies = Vacancy.get_todays_vacancies()
        queryset = Vacancy.objects.filter(
            modified__year=self.current_date.year,
            modified__month=self.current_date.month,
            modified__day=self.current_date.day,
            status=Vacancy.ACTIVE
        )
        self.assertTrue(vacancies[0] == queryset[0])