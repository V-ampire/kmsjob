from django.db import models
from django.utils import timezone
from django.urls import reverse

from core.models import TimeStampedModel


class Vacancy(TimeStampedModel):

    ACTIVE = 'on'
    UNACTIVE = 'off'
    STATUS_CHOICES = (
        (ACTIVE, 'Показывать'),
        (UNACTIVE, 'Не показывать')
    )

    name = models.CharField("Вакансия", max_length=255)
    employer = models.CharField("Работодатель", max_length=255, blank=True)
    source = models.URLField("Ссылка на вакансию", blank=True)
    source_name = models.CharField("Название источника", max_length=50, default='kmsjob')
    description = models.TextField("Описание вакансии", blank=True)
    contacts = models.CharField("Контакты", max_length=125, blank=True)
    status = models.CharField("Статус вакансии", max_length=3, choices=STATUS_CHOICES, default=ACTIVE)


    class Meta:
        db_table = 'vacancy'
        ordering = ('source', '-modified')
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'

    def __str__(self):
        return '{} / {}: {}'.format(self.source_name, self.employer, self.name)

    def get_absolute_url(self):
        return reverse('vacancies:vacancy_detail', kwargs={'pk': self.pk})

    @classmethod
    def get_todays_vacancies(cls, active=True):
        """
        Возвращает вакансии на текущую дату.
        """
        status = cls.ACTIVE if active else cls.UNACTIVE
        current_date = timezone.now()
        return cls.objects.filter(
            modified__year=current_date.year,
            modified__month=current_date.month,
            modified__day=current_date.day,
            status=status
        )
