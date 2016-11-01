from django.shortcuts import render
from search_views.views import SearchListView
from search_views.filters import BaseFilter
from .models import Actor
from .forms import SearchActorForm


class ActorsFilter(BaseFilter):
    search_fields = {
        "search_name" : ["name", "surname"],
        "search_age" : { "operator" : "__exact", "fields" : ["age"] },
        "search_age_min" : { "operator" : "__gte", "fields" : ["age"] },
        "search_age_max" : { "operator" : "__lte", "fields" : ["age"] },
    }


class ActorsView(SearchListView):
    model = Actor
    template_name = "actors_list.html"

    form_class = SearchActorForm
    filter_class = ActorsFilter
