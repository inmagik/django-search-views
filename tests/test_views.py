from django.test import TestCase
from django.db import models
from django.conf import settings
from searchlist_views.views import SearchListView
from django.db.models import Q

from .models import SomeModel

# Create your tests here.
class TestViews(TestCase):

    @classmethod
    def setUpClass(cls):

        super(TestViews, cls).setUpClass()

        cls.test_model = SomeModel

        #prepopulating with predictable records
        contents  = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten']
        for i in range(100):
            idx = i % 10
            a_int = idx
            b_char = contents[idx]
            c_text = contents[9-idx]
            d_bool = bool(i < 50)
            instance = SomeModel.objects.create(a_int=a_int, b_char=b_char, c_text=c_text, d_bool=d_bool)
