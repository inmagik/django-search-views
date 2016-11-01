from django.test import TestCase
from django.db import models
from django.conf import settings
from search_views.filters import build_q, BaseFilter
from django.db.models import Q

from .models import SomeModel

# Create your tests here.
class TestFilter(TestCase):

    @classmethod
    def setUpClass(cls):

        super(TestFilter, cls).setUpClass()

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


    def test_build_q_simple_field(self):

        filters_config = {
            "search_b" : ['b_char']
        }
        params  = {
            "search_b" : "one"
        }

        q = build_q(filters_config, params)
        objs = self.test_model.objects.filter(q)
        self.assertEquals(objs.count(), 10)


    def test_build_q_simple_singlefield(self):

        filters_config = {
            "search_b" : ["b_char", "c_text"]
        }
        params  = {
            "search_b" : "one"
        }

        q = build_q(filters_config, params)
        objs = self.test_model.objects.filter(q)
        self.assertEquals(objs.count(), 20)


    def test_build_q_singlefield(self):

        filters_config = {
            "search" : {
                "operator" : "__lte",
                "fields" : ["a_int"]
            }
        }

        params  = {
            "search" : 5
        }

        q = build_q(filters_config, params)
        objs = self.test_model.objects.filter(q)
        self.assertEquals(objs.count(), 60)


    def test_build_q_multifield(self):

        filters_config = {
            "search_a" : {
                "operator" : "__lte",
                "fields" : ["a_int"]
            },
            "search_b" : {
                "operator" : "__in",
                "fields" : ["b_char"],
                "multiple" : True
            }
        }

        params  = {
            "search_a" : 5,
            "search_b" : ["one", "two", "three"]
        }


        q = build_q(filters_config, params)
        objs = self.test_model.objects.filter(q)
        self.assertEquals(objs.count(), 30)

    def test_custom_query(self):

        def custom(field, value, params):
            return Q(a_int=value)

        filters_config = {
            "search_a" : {
                "custom_query" : custom,
                "fields" : ["a_int"]
            }
        }

        params  = { "search_a": 2 }

        q = build_q(filters_config, params)
        objs = self.test_model.objects.filter(q)
        self.assertEquals(objs.count(), 10)

    def test_custom_query_multi(self):

        def custom(field, value, params):
            return Q(a_int=value)

        filters_config = {
            "search_a" : {
                "custom_query" : custom,
                "fields" : ["a_int"]
            },
            "search_b" : {
                "fields" : ["b_char", "c_text"],
                "operator" : "__iexact"
            }
        }

        params  = { "search_a": 2, "search_b" : "one" }

        q = build_q(filters_config, params)
        objs = self.test_model.objects.filter(q)
        self.assertEquals(objs.count(), 0)


    def test_build_q_ignore(self):
        #TODO: not very informative right now
        #... should be tested in association with a form to ensure that params
        #... are ignored BUT passed to the form

        filters_config = {
            "search_b" : {"ignore":True}
        }
        params  = {
            "search_b" : "one"
        }

        q = build_q(filters_config, params)
        objs = self.test_model.objects.filter(q)
        self.assertEquals(objs.count(), 100)


    def test_fixed_filters(self):

        filters_config = {
            "search_a" : {
                "fields" : ["a_int"],
                "operator" : "__lt",
                "fixed_filters" : { "b_char" : "one"}
            }
        }
        params  = {
            "search_a" : 5
        }

        q = build_q(filters_config, params)
        objs = self.test_model.objects.filter(q)
        self.assertEquals(objs.count(), 10)

    def test_fixed_filters_callable(self):
        def fixed(params):
            return Q(b_char__in=["one", "two"])

        filters_config = {
            "search_a" : {
                "fields" : ["a_int"],
                "operator" : "__lt",
                "fixed_filters" : fixed
            }
        }
        params  = {
            "search_a" : 5
        }

        q = build_q(filters_config, params)
        objs = self.test_model.objects.filter(q)
        self.assertEquals(objs.count(), 20)



    def test_base_filter(self):
        class B(BaseFilter):
            search_fields = {
                "search" : {
                    "operator" : "__lte",
                    "fields" : ["a_int"]
                }
            }

        params  = { "search" : 5 }
        q = B.build_q(params)
        objs = self.test_model.objects.filter(q)
        self.assertEquals(objs.count(), 60)
