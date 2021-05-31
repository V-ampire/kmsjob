from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.shortcuts import render

from vacancies.models import Vacancy
from vacancies.pagination import PaginationMixin
from vacancies.forms import SearchForm, CurrentDateForm
from vacancies import handlers


import logging
logger = logging.getLogger('telegram_logger')

# Error handlers
def e_handler404(request, exception):
    return render(request, 'vacancies/error404.html', status=404)
 
 
def e_handler500(request):
    return render(request, 'vacancies/error500.html', status=500)


# Views
class IndexView(PaginationMixin, ListView):
    template_name = 'vacancies/vacancies.html'
    context_object_name = 'vacancies'
    paginate_by = 12

    def get_queryset(self):
        return Vacancy.get_todays_vacancies()


class VacancyDetailView(DetailView):
    model = Vacancy
    template_name = 'vacancies/vacancy_detail.html'
    context_object_name = 'vacancy'


class ByDateView(PaginationMixin, ListView):
    template_name = 'vacancies/vacancies.html'
    context_object_name = 'vacancies'
    paginate_by = 12

    def get_queryset(self):
        form = CurrentDateForm(self.request.GET)
        if not form.is_valid():
            return Vacancy.get_todays_vacancies()
        current_date = form.cleaned_data['current_date']
        return handlers.get_vacancies_by_date(current_date)
        

class SearchView(PaginationMixin, ListView):
    template_name = 'vacancies/search.html'
    context_object_name = 'vacancies'
    paginate_by = 12

    def get_queryset(self):
        form = SearchForm(self.request.GET)
        if not form.is_valid():
            return []
        search_data = form.cleaned_data
        return handlers.search_vacancies(**search_data)

    def get_context_data(self, *args, **kwargs):
        context = super(SearchView, self).get_context_data(*args, **kwargs)
        context['search_query'] = self.request.GET.get('search_query')
        context['date_from'] = self.request.GET.get('date_from')
        context['date_to'] = self.request.GET.get('date_to')
        return context


