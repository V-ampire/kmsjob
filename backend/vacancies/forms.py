from django import forms


class SearchForm(forms.Form):
    search_query = forms.CharField(max_length=255, required=False)
    date_from = forms.DateField(required=False)
    date_to = forms.DateField(required=False)


class CurrentDateForm(forms.Form):

    current_date = forms.DateField()
    