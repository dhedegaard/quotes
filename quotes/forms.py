from django import forms


class RestForm(forms.Form):
    count = forms.IntegerField(required=True, min_value=1, max_value=200)
