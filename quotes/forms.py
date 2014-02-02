from django import forms


class SearchForm(forms.Form):
    search = forms.CharField(
        required=True, max_length=100, min_length=3)


class RestForm(forms.Form):
    count = forms.IntegerField(required=True, min_value=1, max_value=200)