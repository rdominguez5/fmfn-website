# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db.models import *
from django.conf import settings
from _base import Model


class Material(Model):

	"""
		Represents the model for each material on the server,
		*title(CharField): The name for the material
		*description(CharField): A brief abstract of the material
		*suggested_grades(ManyToManyField): The grades this material has proven to be effective
		*user(ForeignKey): The user that uploaded this material
	"""

	title = CharField(
		max_length = 128,
		null = False,
		blank = False
	)
	description = CharField(
		max_length = 1024,
		null = False,
		blank = False,
		verbose_name = _('description')
	)
	suggested_grades = ManyToManyField('fmfn.Grade',
		related_name = 'ages',
		verbose_name = _('suggested grade')
	)
	user = ForeignKey(settings.AUTH_USER_MODEL,
		related_name = 'materials',
		on_delete = CASCADE,
		verbose_name = _('uploading user')
	)

	class Meta(object):

		verbose_name = _('material')
		verbose_name_plural = _('materials')
		app_label = 'fmfn'
