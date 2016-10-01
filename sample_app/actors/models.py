from __future__ import unicode_literals
from django.db import models

class Actor(models.Model):
    name = models.CharField(max_length=32)
    surname = models.CharField(max_length=32)
    age = models.IntegerField()

    def __unicode__(self):
        return "%s %s" % (self.name, self.surname)
