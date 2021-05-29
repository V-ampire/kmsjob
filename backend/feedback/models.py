from django.db import models

from core.models import TimeStampedModel


class FeedbackMessage(TimeStampedModel):
    name = models.CharField("Имя отправителя", max_length=125)
    contacts = models.CharField("Контакты", max_length=125)
    body = models.CharField("Сообщение", max_length=255)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Сообщение от {}'.format(self.name)


class AddVacancyMessage(TimeStampedModel):
    employer = models.CharField("Название организации", max_length=255)
    name = models.CharField("Название вакансии", max_length=255)
    contacts = models.CharField("Контакты", max_length=125)
    description = models.TextField("Описание вакансии")
    save_vacancy = models.BooleanField("Сохранить вакансию", default=False)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Сообщение от {}'.format(self.employer)