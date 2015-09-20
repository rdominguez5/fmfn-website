# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db.models import *
from django.conf import settings
from _base import Model

class Report(Model):

    user = ForeignKey(settings.AUTH_USER_MODEL,
        related_name = 'reports',
        verbose_name = _('reporting author')
    )
    description = CharField(
        max_length = 64,
	    verbose_name = _('description')
    )
    material = ForeignKey('fmfn.Material',
		related_name = '+',
		verbose_name = _('reported material')
	)
    date_created = DateTimeField(
	    auto_now_add = True,
	    verbose_name = _('date created')
    )

    class Meta(object):
        verbose_name = _('material report')
        verbose_name_plural = _('material reports')
        app_label = 'fmfn'