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


@pytest.mark.django_db
def test_get_vacancies_by_date(avito_vacancies, hh_vacancies):
    for vacancy_data in avito_vacancies:
        Vacancy.objects.create(**vacancy_data)
    for vacancy_data in hh_vacancies:
        Vacancy.objects.create(**vacancy_data)
    expected_date = timezone.now() - timedelta(days=1)
    Vacancy.objects.filter(source_name='hh').update(modified=expected_date)
    result = handlers.get_vacancies_by_date(expected_date)
    expected = Vacancy.objects.filter(source_name='hh')
    assert set(result) == set(expected)


@pytest.mark.django_db
def test_get_vacancies_by_date_with_unactive(hh_vacancies):
    for vacancy_data in hh_vacancies:
        Vacancy.objects.create(**vacancy_data)
    expected_date = timezone.now() - timedelta(days=1)
    unactive_vcacncy = hh_vacancies[0]
    Vacancy.objects.all().update(modified=expected_date)
    Vacancy.objects.filter(source=unactive_vcacncy['source']).update(status=Vacancy.UNACTIVE)
    result = handlers.get_vacancies_by_date(expected_date)
    expected = Vacancy.objects.exclude(source=unactive_vcacncy['source'])
    assert set(result) == set(expected)


@pytest.mark.django_db
def test_search_vacancies_by_search_query(hh_vacancies, vk_vacancies):
    for vacancy_data in hh_vacancies:
        Vacancy.objects.create(**vacancy_data)
    for vacancy_data in vk_vacancies:
        Vacancy.objects.create(**vacancy_data)

    expected_vacancy_name = hh_vacancies[0]['name']
    expected_vacancy_employer = hh_vacancies[0]['employer']
    expected_vacancy_description = vk_vacancies[0]['description']

    result_by_name = handlers.search_vacancies(search_query=expected_vacancy_name)
    result_by_employer = handlers.search_vacancies(search_query=expected_vacancy_employer)
    result_by_description = handlers.search_vacancies(search_query=expected_vacancy_description)

    expected_by_name = Vacancy.objects.filter(name=expected_vacancy_name)
    expected_by_employer = Vacancy.objects.filter(employer=expected_vacancy_employer)
    expected_by_description = Vacancy.objects.filter(description=expected_vacancy_description)
    
    assert set(result_by_name) == set(expected_by_name)
    assert set(result_by_employer) == set(expected_by_employer)
    assert set(result_by_description) == set(expected_by_description)
    