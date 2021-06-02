from django import forms
from feedback.models import FeedbackMessage, AddVacancyMessage


class FeedBackMessageForm(forms.ModelForm):
    class Meta:
        model = FeedbackMessage
        fields = ['name', 'contacts', 'body']


class AddVacancyMessageForm(forms.ModelForm):
    class Meta:
        model = AddVacancyMessage
        fields = ['name', 'employer', 'contacts', 'description']