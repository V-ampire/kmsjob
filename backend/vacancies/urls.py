from django.urls import path
from . import views


app_name = 'vacancies'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('by_date/', views.ByDateView.as_view(), name='by_date'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('detail/<int:pk>/', views.VacancyDetailView.as_view(), name='vacancy_detail'),
]
