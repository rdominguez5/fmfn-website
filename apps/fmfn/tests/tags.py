# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import reverse_lazy
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from apps.fmfn.models import (
	Type,
	Theme,
	Language,
	Role,
	Campus,
	ActionLog
)

__all__ = [
	'TypeTagTest',
	'ThemeTagTest',
	'LanguageTagTest'
]
User = get_user_model()

class _TagTest(TestCase):

	tag_class = Type
	fixtures = [ 'grades', 'roles', 'campus' ]

	@property
	def tag_name(self): return self.tag_class.__name__.lower()

	def setUp(self):

		self.client = Client(
			enforce_csrf_checks = False,
			HTTP_X_REQUESTED_WITH = 'XMLHttpRequest'
		)

		self.user = User.objects.create_user(
			email_address = 'test1@example.com',
			password = 'asdfgh',
			role = Role.objects.get(id = 4),
			campus = Campus.objects.get(id = 1)
		)

	def test_create_tag(self):

		tag_count = len(self.tag_class.objects.active())
		self.assertEqual(tag_count, 0)

		# Test case: a tag creation request arrives
		self.client.login(email_address = 'test1@example.com', password = 'asdfgh')
		response = self.client.post(reverse_lazy('tags:create'), data = {
			'type': self.tag_name,
			'name': 'philosophy'
		}, follow = True)

		# Check status code
		self.assertEqual(response.status_code, 201)

		# Check material count
		self.assertEqual(len(self.tag_class.objects.active()), (tag_count + 1))
	def test_list_tags(self):

		self.client.login(email_address = 'test1@example.com', password = 'asdfgh')
		response = self.client.get(reverse_lazy('tags:list'), data = {
			'type': self.tag_name,
		}, follow = True)

		# Check status code
		self.assertEqual(response.status_code, 200)
	def test_list_filtered_tags(self):

		self.client.login(email_address = 'test1@example.com', password = 'asdfgh')
		response = self.client.get(reverse_lazy('tags:list'), data = {
			'type': self.tag_name,
			'filter': 'tag'
		}, follow = True)

		# Check status code
		self.assertEqual(response.status_code, 200)
	def test_edit_tag(self):

		tag = self.tag_class.objects.create(name = 'test')

		self.client.login(email_address = 'test1@example.com', password = 'asdfgh')
		response = self.client.post(reverse_lazy('tags:edit', kwargs = { 'tag_type': self.tag_name, 'tag_id': tag.id }), data = {
			'name': 'test1',
		}, follow = True)

		# Check status code
		self.assertEqual(response.status_code, 200)

		# Check tag changes
		self.assertEqual(len(self.tag_class.objects.filter(name = 'test1')), 1)
	def test_delete_tag(self):

		tag = self.tag_class.objects.create(name = 'test')
		tag_count = len(self.tag_class.objects.active())

		# Test case: a tag creation request arrives
		self.client.login(email_address = 'test1@example.com', password = 'asdfgh')
		response = self.client.delete(reverse_lazy('tags:edit', kwargs = { 'tag_type': self.tag_name, 'tag_id': tag.id }), follow = True)

		# Check status code
		self.assertEqual(response.status_code, 200)

		# Check material count
		self.assertEqual(len(self.tag_class.objects.active()), (tag_count - 1))
class TypeTagTest(_TagTest):
	tag_class = Type
class ThemeTagTest(_TagTest):
	tag_class = Theme
class LanguageTagTest(_TagTest):
	tag_class = Language