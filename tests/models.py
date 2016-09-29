from __future__ import unicode_literals

from django.db import models

class SomeModel(models.Model):
    a_int = models.IntegerField(null=True, blank=True)
    b_char = models.CharField(max_length=200, null=True, blank=True)
    c_text = models.TextField(null=True, blank=True)
    d_bool = models.NullBooleanField(null=True, blank=True)

    def __unicode__(self):
        return u'%d-%s' %( self.a_int, self.b_char)


    class Meta:
        app_label = "tests"
