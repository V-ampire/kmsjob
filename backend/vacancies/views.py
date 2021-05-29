from django.views.generic.list import ListView
from django.views.generic import FormView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.utils import timezone

from vacancies.models import Vacancy
from vacancies.pagination import PaginationMixin
from vacancies.forms import SearchForm, CurrentDateForm


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
        if form.is_valid():
            current_date = form.cleaned_data['current_date']
        else:
            current_date = timezone.now()
        queryset = Vacancy.objects.filter(
            modified__year=current_date.year,
            modified__month=current_date.month,
            modified__day=current_date.day,
            status=Vacancy.ACTIVE
        )
        return queryset


class SearchView(PaginationMixin, ListView):
    template_name = 'vacancies/search.html'
    context_object_name = 'vacancies'
    paginate_by = 12

    def get_queryset(self):
        form = SearchForm(self.request.GET)
        if form.is_valid():
            date_from = form.cleaned_data['date_from']
            date_to = form.cleaned_data['date_to']
            search_query = form.cleaned_data['search_query']
            vacancies = Vacancy.objects.filter(status=Vacancy.ACTIVE)
            if date_from:
                vacancies = vacancies.filter(modified__gte=date_from)
            if date_to:
                vacancies = vacancies.filter(modified__lte=date_to)
            if search_query:
                vacancies = vacancies.filter(name__search=search_query)
            return vacancies
        return []

    def get_context_data(self, *args, **kwargs):
        context = super(SearchView, self).get_context_data(*args, **kwargs)
        context['search_query'] = self.request.GET.get('search_query')
        context['date_from'] = self.request.GET.get('date_from')
        context['date_to'] = self.request.GET.get('date_to')
        return context


