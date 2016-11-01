django-search-views
===================

This package provides a Django class-based view used for showing a list
of objects with a search form. Full documentation at
(http://inmagik.github.io/django-search-views/).

Features:

-  allows searching multiple fields
-  supports pagination
-  set filtering operators for each field
-  set fixed filters
-  use lists of values for filters

Installation
------------

From pypi:

::

    pip install django-search-views

From source:

::

    python setup.py install

Usage
-----

**Important**: until v.1.0 API might be subject to changes. Please take
a look at the `changelog <#changelog>`__ and don't hesitate to mail us
or open an issue if you have troubles migration from an older version.
Sorry about this!.

SearchListView
~~~~~~~~~~~~~~

tbw

 Example
--------

The following code sets up model, form and view for displaying an
"Actors List".

models.py:

::

    class Actor(models.Model):
        name = models.CharField(max_length=32)
        surname = models.CharField(max_length=32)
        age = models.IntegerField()

forms.py

::

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

views.py

::

    from .model import Actor
    from .forms import ActorSearchForm
    from search_views.search import SearchListView
    from search_views.filters import BaseFilter

    class ActorsFilter(BaseFilter):
        search_fields = {
            'search_text' : ['name', 'surname'],
            'search_age_exact' : { 'operator' : '__exact', 'fields' : ['age'] },
            'search_age_min' : { 'operator' : '__gte', 'fields' : ['age'] },
            'search_age_max' : { 'operator' : '__lte', 'fields' : ['age'] },            

        }

    class ActorsSearchList(SearchListView):
        model = Actor
        paginate_by = 30
        template_name = "actors/actors_list.html"
        form_class = ActorSearchForm
        filter_class = ActorsFilter

view template "actors/actors\_list.html":

::

    {% extends "base.html" %}


    {% block content%}

    <div class="container">

        <h2>Actors list</h2>

        <form class="form-inline" action="" method="GET">
            {{ form }}
            <button class="btn" type="submit">Search</button>
            </fieldset>
        </form>

        <table class="table table-bordered table-condensed">
            <tr>
                <th>Name</th>
                <th>Surname</th>
                <th>Age</th>        
            </tr>
            {% for object in object_list %}
            <tr>
                <td>{{object.name}}</td>
                <td>{{object.surname}}</td>
                <td>{{object.age}}</td>  
            </tr>
            {% endfor %}
        </table>

        {% if is_paginated %}
            {% include "paginator.html" %}
        {% endif %}

    </div>

    {% endblock %}

Changelog
---------

0.2.0
~~~~~

-  filters are now configured in their own class derived from
   ``search_views.filters.BaseFilter``.

0.3.0
~~~~~

-  Renamed main package from ``searchlist_views`` to ``search_views``.

License and development
=======================

This project is MIT licensed and maintained by
`Inmagik <https://www.inmagik.com>`__, suggestions and pull requests are
welcome via the `Github project
page <https://github.com/inmagik/django-search-views/issues>`__
