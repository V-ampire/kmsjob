"""
Бизнес логика.
"""
from django.conf import settings
from django.utils import timezone

from vacancies.models import Vacancy


def clean_expired_vacancies():
    """
    Удалить вакансии с истекщим сроком актуальности.
    """
    expire_delta = settings.VACANCY_EXPIRE
    expire_date = timezone.now() - expire_delta
    return Vacancy.objects.filter(modified__lt=expire_date).delete()
    
    
    