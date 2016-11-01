# django-search-views

This package provides a Django class-based view used for showing a list of objects with a search form.

Think of it as an extension of django's [django.views.generic.list.ListView](https://docs.djangoproject.com/en/1.10/ref/class-based-views/generic-display/#django.views.generic.list.ListView) coupled with a [django form](https://docs.djangoproject.com/en/1.10/topics/forms/#the-django-form-class), where the values of the form build a filter on the base queryset.


## Features

- searching multiple fields
- pagination
- set filtering operators
- set fixed filters
- pass in lists as fiters


## A quick example.

Let's suppose we want to show a searchable list of actors.

We start with a django model in your `models.py`:

```
class Actor(models.Model):
    name = models.CharField(max_length=32)
    surname = models.CharField(max_length=32)
    age = models.IntegerField()
```

We now build a regular django form for letting our users search our actors with various criteria:
name *or* surname, the *exact* age, the *minimun* age and the *maximum* age.

```
from .models import Actor
from django import forms

class ActorSearchForm(forms.Form):
    search_text =  forms.CharField(
        required = False,
        label='Search name or surname!',
        widget=forms.TextInput(attrs={'placeholder': 'search here!'})
    )

    search_age_exact = forms.IntegerField(
        required = False,
        label='Search age (exact match)!'
    )

    search_age_min = forms.IntegerField(
        required = False,
        label='Min age'
    )

    search_age_max = forms.IntegerField(
      required = False,
      label='Max age'
    )
```

Now, using `django-searchlist-views` API we can:

- define the mapping between the form fields and the model fields, and the lookups
used for searching model instances. This is done by writing a subclass of `searchlist_views.filters.BaseFilter`
- define the actual view based on `searchlist_views.views.SearchListView` class.

```
from .models import Actor
from .forms import ActorSearchForm
from searchlist_views.search import SearchListView
from searchlist_views.filters import BaseFilter

class ActorsFilter(BaseFilter):
    search_fields = {
        'search_text' : ['name', 'surname'],
        'search_age_exact' : { 'operator' : '__exact', 'fields' : ['age'] },
        'search_age_min' : { 'operator' : '__gte', 'fields' : ['age'] },
        'search_age_max' : { 'operator' : '__lte', 'fields' : ['age'] },  
    }

class ActorsSearchList(SearchListView):
  # regular django.views.generic.list.ListView configuration
  model = Actor
  paginate_by = 30
  template_name = "actors/actors_list.html"

  # additional configuration for SearchListView
  form_class = ActorSearchForm
  filter_class = ActorsFilter
```

See all the details in the [usage](usage.md) section.


# License and development

This project is MIT licensed and maintained by [Inmagik](https://www.inmagik.com), suggestions and pull requests are welcome via the [Github project page](https://github.com/inmagik/django-search-views/issues).
