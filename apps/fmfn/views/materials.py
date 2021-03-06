# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from apps.fmfn.models import (
	Material,
	ActionLog,
	SchoolGrade,
	Type,
	Theme,
	Language,
	Comment,
	Download,
	Portfolio
)
from django.shortcuts import redirect, render_to_response, RequestContext
from apps.fmfn.decorators import role_required, ajax_required
from django.http import HttpResponseForbidden, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse_lazy
from apps.fmfn.forms import MaterialForm
from django.views.generic import View
from django.http import JsonResponse
from mimetypes import guess_type

__all__ = [
	'create',
	'edit',
	'view',
	'download'
]

class CreateMaterialView(View):

	@method_decorator(login_required)
	@method_decorator(role_required('content manager'))
	def get(self, request):

		form = MaterialForm(initial = { 'user': request.user })
		fields = {
			'suggested_ages': SchoolGrade,
			'types': Type,
			'themes': Theme,
			'languages': Language
		}

		for field, queryset in fields.iteritems():
			form.fields[field].queryset = queryset.objects.active()

		return render_to_response('materials/create.html', context = RequestContext(request, locals()))
	@method_decorator(login_required)
	@method_decorator(role_required('content manager'))
	@method_decorator(csrf_protect)
	def post(self, request):

		form = MaterialForm(request.POST, request.FILES, initial = { 'user': request.user })

		if form.is_valid():

			material = form.instance
			#TODO:set upload_to attribute to destination path
			form.save()

			ActionLog.objects.log_content('Registered new material entry (id: %s)' % material.id, user = request.user, status = 201)
			return redirect(reverse_lazy('content:view', kwargs = { 'content_id': material.id }))

		ActionLog.objects.log_content('Failed to register new material entry', user = request.user, status = 401)

		return render_to_response('materials/create.html',
			context = RequestContext(request, locals()),
			status = 401
		)

create = CreateMaterialView.as_view()

class EditMaterialView(View):

	@method_decorator(login_required)
	@method_decorator(role_required('content manager'))
	def get(self, request, content_id = 0):

		material = Material.objects.active().get(id = content_id)

		form = MaterialForm(instance = material, initial = {'user': request.user })
		fields = {
			'suggested_ages': SchoolGrade,
			'types': Type,
			'themes': Theme,
			'languages': Language
		}

		for field, queryset in fields.iteritems():
			form.fields[field].queryset = queryset.objects.active()

		return render_to_response('materials/edit.html', context = RequestContext(request, locals()))

	@method_decorator(login_required)
	@method_decorator(role_required('content manager'))
	@method_decorator(csrf_protect)
	def post(self, request, content_id = 0):

		material = Material.objects.active().get(id = content_id)
		form = MaterialForm(request.POST, request.FILES,
			instance = material,
			initial = { 'user': request.user }
		)

		#TODO: prepopulate form (checkboxes)
		if form.is_valid():

			material = form.instance
			form.save()
			ActionLog.objects.log_content('Edited material entry (id: %s)' % content_id, user = request.user, status = 200)

			return redirect(reverse_lazy('content:view', kwargs = { 'content_id': material.id }))

		ActionLog.objects.log_content('Attempted to edit material entry (id: %s)' % content_id, user = request.user, status = 401)
		return render_to_response('materials/edit.html', context = RequestContext(request, locals()))

	@method_decorator(login_required)
	@method_decorator(role_required('content manager'))
	@method_decorator(csrf_protect)
	def delete(self, request, content_id = 0):

		material = Material.objects.active().get(id = content_id)

		ActionLog.objects.log_content('Deleted material (id: %s)' % material.id, status = 200, user = request.user)
		material.delete()

		return JsonResponse(data = {
			'version': '1.0.0',
			'status': 200,
			'material': { 'id': material.id, 'status': 'delete' }
		}, content_type = 'application/json')

edit = EditMaterialView.as_view()

class MaterialDetailView(View):

	@method_decorator(login_required)
	@method_decorator(role_required('parent'))
	def get(self, request, content_id = 0):

		try: material = Material.objects.active().get(id = content_id)
		except Material.DoesNotExist:

			ActionLog.objects.log_content('Attempted to load nonexistent material (id: %s)' % content_id, user = request.user, status = 403)
			return HttpResponseForbidden()

		else:

			in_portfolio = Portfolio.objects.user(request.user).items.filter(material = material,active= True).exists()
			has_commented = Comment.objects.active().filter(user=request.user,material=material).exists()
			comments = Comment.objects.active().filter(material=material)
			types = material.types.active()
			languages = material.themes.active()
			themes = material.languages.active()
			ages = material.suggested_ages.active()
			ActionLog.objects.log_content('Viewed material (id: %s)' % content_id, user = request.user)
			return render_to_response('materials/detail.html', context = RequestContext(request, locals()))
	@method_decorator(login_required)
	@method_decorator(ajax_required)
	@method_decorator(role_required('teacher'))
	def post(self,request, content_id = 0):
		""" This method is called when the user posts a comment on a material detail view.
			It validates that the user has already rated such material and that the comment's length is lower than 500 chars
		"""

		try: material = Material.objects.active().get(id = content_id)
		except Material.DoesNotExist:

			ActionLog.objects.log_content('Attempted to recover nonexistent material (id: %s)' % content_id, user = request.user, status = 403)
			return HttpResponseForbidden()
		else:

			if Comment.objects.active().filter(user = request.user, material = material).exists():

				ActionLog.objects.log_content('User has already issued comment for this material (id: %s)' % content_id, user = request.user, status = 403)
				return HttpResponseForbidden()

			content, rating = request.POST.get('content', None), request.POST.get('rating_value', None)
			if content is None or rating is None:

				ActionLog.objects.log_content('Comment data was missing or is invalid', user = request.user, status = 403)
				return HttpResponseForbidden()

			comment = Comment.objects.create(
				user = request.user,
				material = material,
				content = content,
				rating_value = rating
			)

			ActionLog.objects.log_content('Added comment for material (id: %s)' % content_id, user = request.user, status = 201)
			return JsonResponse({
				'version': '1.0.0',
				'status': 201,
				'data': {
					'content': comment.content,
					'user': request.user.id,
					'material': material.id,
					'rating': int(comment.rating_value)
				}
			}, status = 201)

view = MaterialDetailView.as_view()

class MaterialDownloadView(View):
	"""
		This view handles the logic for downloading material
	"""
	@method_decorator(login_required)
	@method_decorator(role_required('parent'))
	def get(self, request, content_id = 0):
		""" This method is called when the user requests to download a material
			It validates the material exists and is active, registers the download and serves the file
			Returns forbidden response if unsuccessful and HttpResponse with the material if successful
		"""

		# Attempt to load the material
		try: material = Material.objects.active().get(id = content_id)
		except Material.DoesNotExist:

			# If not exists, write in Action Log and return forbidden
			ActionLog.objects.log_content('Attempted to load nonexistent material (id: %s)' % content_id, user = request.user, status = 403)
			return HttpResponseForbidden()

		else:

			# Check if the material has a content attached
			if bool(material.content.name) is False:

				# If no content, write in Action Log and return forbidden
				ActionLog.objects.log_content('Attempted to download material without attached content (id: %s)' % content_id, user = request.user, status = 403)
				return HttpResponseForbidden()

			# Register the download
			Download.objects.create(
				user = request.user,
				material = material,
			)

			# Get the material content type we'll use it later
			content_type, _ = guess_type(material.content.name, strict = True)

			# Write in Action Log
			ActionLog.objects.log_content('Downloaded material (id: %s)' % content_id, user = request.user, status = 200)

			# Read the file into the output stream and send it to the user
			return HttpResponse(material.content.read(), content_type = content_type)

download = MaterialDownloadView.as_view()
