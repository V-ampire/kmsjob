"""
Бизнес логика.
"""
from django.conf import settings
from django.utils import timezone
from django.contrib.postgres.search import SearchVector

from vacancies.models import Vacancy

from datetime import datetime
from typing import Optional


def clean_expired_vacancies():
    """
    Удалить вакансии с истекщим сроком актуальности.

    :return: Вощзвращает QuerySet вакансий.
    """
    expire_delta = settings.VACANCY_EXPIRE
    expire_date = timezone.now() - expire_delta
    return Vacancy.objects.filter(modified__lt=expire_date).delete()


def get_vacancies_by_date(date: datetime):
    """
    Возвращает активные вакансии на запрашиваемую дату.
    :param date: Объект даты, на которую нужно найти вакансии.

    :return: Вощзвращает QuerySet вакансий.
    """
    return Vacancy.objects.filter(
        modified__year=date.year,
        modified__month=date.month,
        modified__day=date.day,
        status=Vacancy.ACTIVE
    )    


def search_vacancies(**search_params):
    """
    Поиск активных вакансий по диапозону дат и/или тексту в описании в названии вакансии.
    :param date_from: Найти вакансии опубликованные не раньше этой даты.
    :param date_to: Найти вакансии опубликованные не позже этой даты.
    :param search_query: Найти вакансии по данному запросу. 
    Поиск проводится в названиях, работодателях и описании вакансии.

    :return: Вощзвращает QuerySet вакансий.
    """
    date_from = search_params.get('date_from', None)
    date_to = search_params.get('date_to', None)
    search_query = search_params.get('search_query', None)
    vacancies = Vacancy.objects.filter(status=Vacancy.ACTIVE)
    if date_from is not None:
        vacancies = vacancies.filter(modified__gte=date_from)
    if date_to is not None:
        vacancies = vacancies.filter(modified__lte=date_to)
    if search_query is not None:
        vacancies = vacancies.annotate(
            search=SearchVector('name', 'employer', 'description'),
        ).filter(search=search_query)
    return vacancies
