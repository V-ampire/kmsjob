from django.urls import path
from . import views


app_name = 'feedback'
urlpatterns = [
    path('kmsjob_feedback/', views.FeedbackKmsjobView.as_view(), name='kmsjob_feedback'),
    path('kmsjob_add_vacancy/', views.AddVacancyKmsjobView.as_view(), name='kmsjob_add_vacancy'),
]