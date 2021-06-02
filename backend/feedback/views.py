from django.views.generic import CreateView
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect

from feedback.models import FeedbackMessage, AddVacancyMessage
from feedback.forms import FeedBackMessageForm, AddVacancyMessageForm

import logging


tg_logger = logging.getLogger('telegram')


class FeedbackKmsjobView(CreateView):
    form_class = FeedBackMessageForm
    success_url = reverse_lazy('vacancies:index')
    
    def form_valid(self, form):
        response = super(FeedbackKmsjobView, self).form_valid(form)
        messages.success(self.request, 'Ваше сообщение успешно отправлено!')
        tg_logger.info('Получено новое сообщение от пользователя.')
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Не удалось отправить сообщение! Проверьте введенные данные!')
        return redirect('vacancies:index')


class AddVacancyKmsjobView(CreateView):
    form_class = AddVacancyMessageForm
    success_url = reverse_lazy('vacancies:index')
    
    def form_valid(self, form):
        response = super(AddVacancyKmsjobView, self).form_valid(form)
        messages.success(self.request, 'Благодарим! Ваша вакансия будет добавлена после модерации!')
        tg_logger.info('Получено сообщение о новой вакансии.')
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Не удалось отправить сообщение! Проверьте введенные данные!')
        return redirect('vacancies:index')
