from django.views.generic import FormView
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect

from .models import FeedbackMessage, AddVacancyMessage
from .forms import FeedBackMessageForm, AddVacancyMessageForm


class FeedbackKmsjobView(FormView):
    form_class = FeedBackMessageForm
    success_url = reverse_lazy('kmsjob:index')
    
    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Ваше сообщение успешно отправлено!')
        return super(FeedbackKmsjobView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Не удалось отправить сообщение! Проверьте введенные данные!')
        return redirect('kmsjob:index')


class AddVacancyKmsjobView(FormView):
    form_class = AddVacancyMessageForm
    success_url = reverse_lazy('kmsjob:index')
    
    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Благодарим! Ваша вакансия будет добавлена после модерации!')
        return super(AddVacancyKmsjobView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Не удалось отправить сообщение! Проверьте введенные данные!')
        return redirect('kmsjob:index')