"""
Тест работы парсеров по пополучению данных осуществляется через запуск функциональных тестов.
pytest vacancies/tests/test_jobparser/functional_tests.py -s
"""
from vacancies.jobparser.parsers import BaseVacancyParser
from vacancies.models import Vacancy

import pytest


@pytest.mark.django_db
def test_create_in_db(mocker, avito_vacancies):
    mocker.patch.object(BaseVacancyParser, 'get_vacancies')
    mock_data = mocker.patch.object(BaseVacancyParser, 'parse_data')
    mock_data.return_value = avito_vacancies
    parser = BaseVacancyParser({})
    parser.run()
    assert Vacancy.objects.all().count() == len(avito_vacancies)


@pytest.mark.django_db
def test_update_in_db(mocker, avito_vacancies, now):
    mocker.patch('vacancies.jobparser.parsers.timezone.now', return_value=now)
    expected_vacancy_data = avito_vacancies[0]
    Vacancy.objects.create(**expected_vacancy_data)
    mocker.patch.object(BaseVacancyParser, 'get_vacancies')
    mock_data = mocker.patch.object(BaseVacancyParser, 'parse_data')
    mock_data.return_value = avito_vacancies
    mock_update = mocker.patch('django.db.models.query.QuerySet.update')
    parser = BaseVacancyParser({})
    parser.run()
    mock_update.assert_called_with(**expected_vacancy_data, modified=now)

