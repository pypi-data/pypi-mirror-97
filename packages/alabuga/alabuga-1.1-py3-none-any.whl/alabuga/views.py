from django.views import View
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import (
	render, 
	reverse, 
	redirect, 
	get_object_or_404
	)

from .forms import (
	Model1Form, 
	Model1FormSet, 
	Model2Form, 
	Model2InlineFormSet, 
	Model4Form, 
	Model4GenericInlineFormSet,
	Model5Form,
	)
from .models import MODELS

LOGIN_URL = '/admin/'


# Model1 Views
class Model1View(View):
	def get(self, request):
		data = MODELS[0].objects.order_by('-pk')
		return render(request, 'alabuga/model1_view.html', {'data': data})


class Model1AddView(LoginRequiredMixin, View):
	login_url = LOGIN_URL
	redirect_field_name = 'redirect_to'

	def get(self, request):
		form = Model1Form()
		return render(request, 'alabuga/model1_add.html', {'form': form})

	def post(self, request):
		form = Model1Form(request.POST)
		if form.is_valid():
			form.save()
			return redirect(reverse('model1-view'))
		return render(request, 'alabuga/model1_add.html', {'form': form})


class Model1ChangeView(LoginRequiredMixin, View):
	login_url = LOGIN_URL
	redirect_field_name = 'redirect_to'	

	def get(self, request, pk):
		obj = get_object_or_404(MODELS[0], pk=pk)
		form = Model1Form({'ind': pk, 'title': obj.title})
		return render(request, 'alabuga/model1_change.html', {'form': form, 'pk': pk})

	def post(self, request, pk):
		form = Model1Form({'ind': pk, 'title': request.POST.get('title')})
		if form.is_valid():
			form.save()
			return redirect(reverse('model1-view'))
		return render(request, 'alabuga/model1_change.html', {'form': form, 'pk': pk})


class Model1DeleteView(LoginRequiredMixin, View):
	login_url = LOGIN_URL
	redirect_field_name = 'redirect_to'

	def get(self, request, pk):
		obj = get_object_or_404(MODELS[0], pk=pk)
		obj.delete()
		return redirect(reverse('model1-view'))


class Model1FormSetView(LoginRequiredMixin, View):
	login_url = LOGIN_URL
	redirect_field_name = 'redirect_to'

	def get(self, request):
		formset = Model1FormSet()
		return render(request, 'alabuga/model1_formset.html', {'formset': formset})

	def post(self, request):
		formset = Model1FormSet(request.POST)

		if formset.is_valid():
			for form in formset:
				form.save()
			return redirect(reverse('model1-view'))
		return render(request, 'alabuga/model1_formset', {'formset': formset})


# Model 2 Views


class Model2View(View):
	def get(self, request):
		countries = MODELS[0].objects.all()
		regions = MODELS[1].objects.all()
		return render(request, 'alabuga/model2_view.html', 
			{'countries': countries, 'regions': regions})


class Model2AddView(LoginRequiredMixin, View):
	login_url = LOGIN_URL
	redirect_field_name = 'redirect_to'

	def get(self, request):
		form = Model2Form()
		return render(request, 'alabuga/model2_add.html', {'form': form})

	def post(self, request):
		form = Model2Form(request.POST)
		if form.is_valid():
			form.save()
			return redirect(reverse('model2-view'))
		return render(request, 'alabuga/model2_add.html', {'form': form})


class Model2ChangeView(LoginRequiredMixin, View):
	login_url = LOGIN_URL
	redirect_field_name = 'redirect_to'

	def get(self, request, pk):
		obj = get_object_or_404(MODELS[1], pk=pk)
		form = Model2Form(instance=obj)
		return render(request, 'alabuga/model2_change.html', {'form': form, 'pk': pk})

	def post(self, request, pk):
		obj = get_object_or_404(MODELS[1], pk=pk)
		form = Model2Form(request.POST, instance=obj)

		if form.is_valid():
			form.save()
			return redirect(reverse('model2-view'))
		return render(request, 'alabuga/model2_change.html', {'form': form, 'pk': pk})


class Model2DeleteView(LoginRequiredMixin, View):
	login_url = LOGIN_URL
	redirect_field_name = 'redirect_to'

	def get(self, request, pk):
		obj = get_object_or_404(MODELS[1], pk=pk)
		obj.delete()
		return redirect(reverse('model2-view'))


class Model2FormSetView(LoginRequiredMixin, View):
	login_url = LOGIN_URL
	redirect_field_name = 'redirect_to'

	def get(self, request, pk):
		obj = get_object_or_404(MODELS[0], pk=pk)
		formset = Model2InlineFormSet()
		return render(request, 'alabuga/model2_formset.html', {'formset': formset, 'pk': pk})

	def post(self, request, pk):
		obj = get_object_or_404(MODELS[0], pk=pk)
		formset = Model2InlineFormSet(request.POST, instance=obj)

		if formset.is_valid():
			formset.save()
			return redirect(reverse('model2-view'))
		return render(request, 'alabuga/model2_formset', {'formset': formset})


# Model 4 Views

class Model4View(View):
	def get(self, request):
		countries = MODELS[0].objects.all()
		brands = MODELS[3].objects.all()
		return render(request, 'alabuga/model4_view.html', 
			{'countries': countries, 'brands': brands})


class Model4AddView(LoginRequiredMixin, View):
	login_url = LOGIN_URL
	redirect_field_name = 'redirect_to'

	def get(self, request):
		form = Model4Form()
		return render(request, 'alabuga/model4_add.html', {'form': form})

	def post(self, request):
		form = Model4Form(request.POST)
		if form.is_valid():
			form.save()
			return redirect(reverse('model4-view'))
		return render(request, 'alabuga/model4_add.html', {'form': form})


class Model4ChangeView(LoginRequiredMixin, View):
	login_url = LOGIN_URL
	redirect_field_name = 'redirect_to'

	def get(self, request, pk):
		obj = get_object_or_404(MODELS[3], pk=pk)
		form = Model4Form(instance=obj)
		return render(request, 'alabuga/model4_change.html', {'form': form, 'pk': pk})

	def post(self, request, pk):
		obj = get_object_or_404(MODELS[3], pk=pk)
		form = Model4Form(request.POST, instance=obj)

		if form.is_valid():
			form.save()
			return redirect(reverse('model4-view'))
		return render(request, 'alabuga/model4_change.html', {'form': form, 'pk': pk})


class Model4DeleteView(LoginRequiredMixin, View):
	login_url = LOGIN_URL
	redirect_field_name = 'redirect_to'

	def get(self, request, pk):
		obj = get_object_or_404(MODELS[3], pk=pk)
		obj.delete()
		return redirect(reverse('model4-view'))


class Model4FormSetView(LoginRequiredMixin, View):
	login_url = LOGIN_URL
	redirect_field_name = 'redirect_to'

	def get(self, request, pk):
		obj = get_object_or_404(MODELS[0], pk=pk)
		formset = Model4GenericInlineFormSet()
		return render(request, 'alabuga/model4_formset.html', {'formset': formset, 'pk': pk})

	def post(self, request, pk):
		obj = get_object_or_404(MODELS[0], pk=pk)
		formset = Model4GenericInlineFormSet(request.POST, instance=obj)

		if formset.is_valid():
			formset.save()
			return redirect(reverse('model4-view'))
		return render(request, 'alabuga/model4_formset', {'formset': formset})


# Model 5
class Model5View(LoginRequiredMixin, View):
	login_url = LOGIN_URL
	redirect_field_name = 'redirect_to'

	def get(self, request):
		objs = MODELS[4].objects.all()
		return render(request, 'alabuga/model5_view.html', {'objs': objs})


class Model5AddView(LoginRequiredMixin, View):
	login_url = LOGIN_URL
	redirect_field_name = 'redirect_to'

	def get(self, request):
		form = Model5Form()
		return render(request, 'alabuga/model5_add.html', {'form': form})

	def post(self, request):
		form = Model5Form(request.POST)
		if form.is_valid():
			form.save()
			return redirect(reverse('model5-view'))
		return render(request, 'alabuga/model5_add.html', {'form': form})


def region_to_json(request, pk):
	country = get_object_or_404(MODELS[0], pk=pk)
	regions = MODELS[1].objects.filter(country=country).order_by('-pk')
	data = [{"id": region.pk, "title": region.title} for region in regions]
	return JsonResponse({'data': data}, safe=True)


def sub_region_to_json(request, pk):
	region = get_object_or_404(MODELS[1], pk=pk)
	sub_regions = MODELS[1].objects.filter(reg=region)
	data = [{"id": region.pk, "title": region.title} for region in sub_regions]
	return JsonResponse({'data': data}, safe=True)


def brand_to_json(request):
	reg = request.GET.get('reg')
	sub_reg = request.GET.get('sub-reg')
	try:
		reg = int(reg)
		sub_reg = int(sub_reg)
	except (TypeError, ValueError):
		return JsonResponse({'data': []})

	brands = MODELS[3].objects.filter(Q(region__pk=reg) | Q(sub_region__pk=sub_reg))
	data = [{"id": brand.pk, "title": brand.title} for brand in brands]
	return JsonResponse({'data': data}, safe=True)
