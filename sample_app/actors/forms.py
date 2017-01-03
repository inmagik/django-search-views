from django import forms
from search_views.actionslist import BaseActionForm

class SearchActorForm(forms.Form):
    search_name = forms.CharField(required=False)
    search_age = forms.IntegerField(required=False)
    search_age_min = forms.IntegerField(required=False)
    search_age_max = forms.IntegerField(required=False)


class ActionsForm(BaseActionForm):
    age = forms.IntegerField(required=False)
