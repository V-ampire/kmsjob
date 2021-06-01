from django.urls import path
from . import views


app_name = 'feedback'
urlpatterns = [
    path('feedback', views.FeedbackKmsjobView.as_view(), name='feedback'),
    path('add_vacancy', views.AddVacancyKmsjobView.as_view(), name='add_vacancy'),
]