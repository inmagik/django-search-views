from django.shortcuts import render
from search_views.views import SearchListView
from search_views.actionslist import ActionsListMixin
from search_views.filters import BaseFilter
from .models import Actor
from .forms import SearchActorForm, ActionsForm


class ActorsFilter(BaseFilter):
    search_fields = {
        "search_name" : ["name", "surname"],
        "search_age" : { "operator" : "__exact", "fields" : ["age"] },
        "search_age_min" : { "operator" : "__gte", "fields" : ["age"] },
        "search_age_max" : { "operator" : "__lte", "fields" : ["age"] },
    }


class ActorsView(ActionsListMixin, SearchListView):
    model = Actor
    template_name = "actors_list.html"

    form_class = SearchActorForm
    filter_class = ActorsFilter

    actions = [
        ("set_actor_age", "Set age", ['age'])
    ]
    actions_form_class = ActionsForm
    actions_fields_wrapper = "p"

    def after_post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def set_actor_age(self, record, form_data):
        record.age = form_data['age']
        record.save()
