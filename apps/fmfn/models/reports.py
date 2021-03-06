# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db.models import *
from _base import Model, ActiveManager

class Report(Model):
	"""
	Represents a user's report on a particular material. Each report defines:

		* user (ForeignKey): A reference to the user that posted the report
		* description (CharField): A short message explaining the nature of the report
		* material (ForeignKey): A reference to the material that is being reported
		* date_created (ForeignKey): A timestamp of the date that the report was raised
	"""

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
	status = PositiveSmallIntegerField(
		choices = [
			(1, _('in progress')),
			(2, _('resolved')),
			(4, _('rejected'))
		],
		blank = True,
		default = 1,
		verbose_name = _('report status')
	)

	class Meta(object):
		verbose_name = _('material report')
		verbose_name_plural = _('material reports')
		app_label = 'fmfn'

class ActionLogManager(ActiveManager):

	def log_account(self, action, status = 200, user = None): return self._log(1, action, status, user)
	def log_content(self, action, status = 200, user = None): return self._log(2, action, status, user)
	def log_tags(self, action, status = 200, user = None): return self._log(4, action, status, user)
	def log_downloads(self, action, status = 200, user = None): return self._log(5, action, status, user)
	def log_reports(self, action, status = 200, user = None): return self._log(6, action, status, user)

	def _log(self, category, action, status, user):

		return self.create(
			category = category,
			user = user,
			status = status,
			action = action
		)
class ActionLog(Model):

	user = ForeignKey(settings.AUTH_USER_MODEL,
		null = True,
		related_name = '+',
		verbose_name = _('user')
	)
	category = PositiveSmallIntegerField(
		choices = [
			(0x01, _('account control')),
			(0x02, _('content management')),
			(0x04, _('tag management')),
		],
		verbose_name = _('performed action category')
	)
	action = CharField(
		max_length = 512,
		db_index = True,
		null = False,
		verbose_name = _('performed action')
	)
	status = PositiveSmallIntegerField(verbose_name = _('performed action status code'))
	action_date = DateTimeField(
		auto_now_add = True,
		db_index = True,
		verbose_name = _('performed action date')
	)

	objects = ActionLogManager()

	class Meta(object):

		verbose_name = _('action log')
		verbose_name_plural = _('action logs')
		app_label = 'fmfn'
