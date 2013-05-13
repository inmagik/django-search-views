# django-searchlist-views

This package provides a Django class-based view used for showing a list of objects with a text form.

Features:

* searching multiple fields
* set filtering operators
* set fixed filters
* pass in lists as fiters 


This is a work in progress!

## Installation

    python setup.py install

## Usage

### SearchListView
tbw


## Example

The following code sets up model, form and view for displaying an "Actors List".


Example models.py:


    class Actor(models.Model):
        name = models.CharField(max_length=32)
        surname = models.CharField(max_length=32)
        age = models.IntegerField()
        
        
        

Example forms.py
    
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
                      


Example views.py

    from .model import Actor
    from .forms import ActorSearchForm
    from search_views import SearchListView
    
    class ActorsSearchList(SearchListView):
        model = Actor
        paginate_by = 30
        template_name = "actors/actors_list.html"
        form_class = ActorSearchForm
        search_fields = {
            'search_text' : ['name', 'surname'],
            'search_age_exact' : { 'operator' : '__exact', 'fields' : ['age'] },
            'search_age_min' : { 'operator' : '__gte', 'fields' : ['age'] },
            'search_age_max' : { 'operator' : '__lte', 'fields' : ['age'] },            
    
        }
        
        
Example view template:
    
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
