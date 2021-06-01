from django.contrib import admin
from django.db import transaction

from .models import FeedbackMessage, AddVacancyMessage
from vacancies.models import Vacancy


class AdminFeedbackMessage(admin.ModelAdmin):
    pass

admin.site.register(FeedbackMessage, AdminFeedbackMessage)


class AdminAddVacancyMessage(admin.ModelAdmin):

    actions = ['save_vacancy']
    list_display = ('name', 'employer', 'contacts', 'saved_vacancy')
    readonly_fields = ('saved_vacancy',)
    list_filter = ('saved_vacancy', 'employer', 'name')

    @admin.action(description='Сохранить вакансию в базу данных')
    def save_vacancy(self, request, messages):
        created_count = 0
        for message in messages:
            with transaction.atomic():
                vacancy, created = Vacancy.objects.get_or_create(
                    name=message.name,
                    employer=message.employer,
                    description=message.description,
                    contacts=message.contacts,
                )
                message.saved_vacancy = True
                message.save()
                if created:
                    created_count += 1
        self.message_user(request, f'Сохранено {created_count} вакансий')


admin.site.register(AddVacancyMessage, AdminAddVacancyMessage)
