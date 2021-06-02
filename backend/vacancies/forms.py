from django import forms


class SearchForm(forms.Form):
    """
    Форма для поиска.
    """
    search_query = forms.CharField(max_length=255, required=False)
    date_from = forms.DateField(required=False)
    date_to = forms.DateField(required=False)


class CurrentDateForm(forms.Form):
    """
    Форма поиска по конкретной дате.
    """
    current_date = forms.DateField()
    