from django import forms

class SearchActorForm(forms.Form):
    search_name = forms.CharField(required=False)
    search_age = forms.IntegerField(required=False)
    search_age_min = forms.IntegerField(required=False)
    search_age_max = forms.IntegerField(required=False)
