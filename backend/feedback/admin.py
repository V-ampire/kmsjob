from django.contrib import admin

from .models import FeedbackMessage, AddVacancyMessage
from vacancies.models import Vacancy


class AdminFeedbackMessage(admin.ModelAdmin):
    pass

admin.site.register(FeedbackMessage, AdminFeedbackMessage)


class AdminAddVacancyMessage(admin.ModelAdmin):

    def save_vacancy(self, request, data):
        vacancy = Vacancy.objects.create(
            name=data.get('name'),
            employer=data.get('employer'),
            description=data.get('description'),
        )
        self.message_user(request, 'Вакансия {} от {} сохранена!'.format(vacancy.name, vacancy.employer))

      
    def save_model(self, request, obj, form, change):
        if form.cleaned_data.get('save_vacancy'):
            self.save_vacancy(request, form.cleaned_data)
        super(AdminAddVacancyMessage, self).save_model(request, obj, form, change)


admin.site.register(AddVacancyMessage, AdminAddVacancyMessage)
