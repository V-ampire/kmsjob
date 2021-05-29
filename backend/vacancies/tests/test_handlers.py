from django.conf import settings
from django.utils import timezone

from vacancies.models import Vacancy
from vacancies import handlers

from datetime import timedelta
import pytest


@pytest.mark.django_db
def test_clean_expired_vacancies(avito_vacancies):
    for vacancy_data in avito_vacancies:
        Vacancy.objects.create(**vacancy_data)
    expired_sources = [v['source'] for v in avito_vacancies[:3]]
    Vacancy.objects.filter(source__in=expired_sources).update(
        modified=timezone.now() - settings.VACANCY_EXPIRE - timedelta(days=1)
    )
    count, result = handlers.clean_expired_vacancies()
    assert not Vacancy.objects.filter(source__in=expired_sources).exists()
    assert count == len(expired_sources)

