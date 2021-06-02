from django.db import models

from core.models import TimeStampedModel


class FeedbackMessage(TimeStampedModel):
    """
    Сообщение от пользователя.
    """
    name = models.CharField("Имя отправителя", max_length=125)
    contacts = models.CharField("Контакты", max_length=125)
    body = models.CharField("Сообщение", max_length=255)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Обратная связь'
        verbose_name_plural = 'Обратная связь'

    def __str__(self):
        return 'Сообщение от {}'.format(self.name)


class AddVacancyMessage(TimeStampedModel):
    """
    Сообщение о добавлении новой вакансии.
    """
    employer = models.CharField("Название организации", max_length=255)
    name = models.CharField("Название вакансии", max_length=255)
    contacts = models.CharField("Контакты", max_length=125)
    description = models.TextField("Описание вакансии")
    saved_vacancy = models.BooleanField("Вакансия сохранена", default=False)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Сообщение о вакансии'
        verbose_name_plural = 'Сообщения о вакансиях'
        

    def __str__(self):
        return 'Сообщение от {}'.format(self.employer)