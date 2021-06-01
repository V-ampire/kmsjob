from django.views.generic import CreateView
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect

from .models import FeedbackMessage, AddVacancyMessage
from .forms import FeedBackMessageForm, AddVacancyMessageForm


class FeedbackKmsjobView(CreateView):
    form_class = FeedBackMessageForm
    success_url = reverse_lazy('vacancies:index')
    
    def form_valid(self, form):
        
        response = super(FeedbackKmsjobView, self).form_valid(form)
        messages.success(self.request, 'Ваше сообщение успешно отправлено!')
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
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Не удалось отправить сообщение! Проверьте введенные данные!')
        return redirect('vacancies:index')