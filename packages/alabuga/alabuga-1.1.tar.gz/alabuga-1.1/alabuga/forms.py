from django import forms
from django.forms import (
	formset_factory, 
	inlineformset_factory, 
	modelform_factory, 
	)
from django.contrib.contenttypes.forms import generic_inlineformset_factory
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404

from .models import MODELS


# Model 1
class Model1Form(forms.Form):
	ind = forms.IntegerField(required=False)
	title = forms.CharField(max_length=128)

	ind.widget = forms.HiddenInput()

	def clean(self):
		data = self.cleaned_data
		ind = self.cleaned_data.get('ind', None)
		if ind is None:
			return self.cleaned_data
		try:
			ind = int(ind)
		except (TypeError, ValueError):
			raise ValidationError('Changed hidden input!')
		data['ind'] = ind
		return data

	def save(self):
		title = self.cleaned_data.get('title')
		ind = self.cleaned_data.get('ind', None)
		if not title:
			return None
		if ind is not None:
			obj = get_object_or_404(MODELS[0], pk=ind)
			obj.title = title
		else:
			obj = MODELS[0](title=title)
		obj.save()
		return obj


Model1FormSet = formset_factory(Model1Form, extra=3)


# Model 2

Model2Form = modelform_factory(MODELS[1], fields=('title', 'country', 'reg'))

Model2InlineFormSet = inlineformset_factory(
	MODELS[0], MODELS[1],
	fields=('title', 'country', 'reg'), extra=3
)


# Model 4

class Model4Form(forms.ModelForm): 
	info = forms.CharField(widget=forms.Textarea(), required=False)

	class Meta:
		model = MODELS[3]
		fields = ('title', 'region', 'sub_region', 'info')


Model4GenericInlineFormSet = generic_inlineformset_factory(
	MODELS[3],
	fields=('title', 'region', 'sub_region'),
	ct_field='c_type', fk_field='obj_id'
)


# Model 5

Model5Form = modelform_factory(MODELS[4], fields=('country', 'region', 'sub_region', 'brand'))
Model5Form.base_fields['country'].widget.attrs.update({'onchange': 'country_handle()'})
Model5Form.base_fields['region'].widget.attrs.update({'onchange': 'region_handle()'})
Model5Form.base_fields['sub_region'].widget.attrs.update({'onchange': 'sub_region_handle()'})
