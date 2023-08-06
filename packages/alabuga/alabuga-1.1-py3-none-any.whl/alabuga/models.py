from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.shortcuts import reverse
from django.db.models.base import ModelBase


MODELS = []


class SelfMeta(ModelBase):
	def __new__(mcs, name, bases, data):
		klass = super().__new__(mcs, name, bases, data)
		MODELS.append(klass)
		return klass


# Model 1
class Country(models.Model, metaclass=SelfMeta):
	title = models.CharField(max_length=128)
	marks = GenericRelation(
		'Brand',
		related_name='country',
		content_type_field='c_type',
		object_id_field='obj_id',
		)

	def get_absolute_url(self):
		return reverse('model1-change', kwargs={'pk': self.pk})

	def __str__(self):
		return self.title


# Model 2
class Region(models.Model, metaclass=SelfMeta):
	title = models.CharField(max_length=128)
	country = models.ForeignKey(
		MODELS[0],
		on_delete=models.CASCADE,
		related_name='country',
		blank=True,
		null=True,
		)
	reg = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('model2-change', kwargs={'pk': self.pk})


# Model 3
class SubRegion(Region):
	def something(self):
		return self.title

	class Meta:
		proxy = True


# Model 4
class Brand(models.Model, metaclass=SelfMeta):
	title = models.CharField('brand name', max_length=128)
	region = models.ManyToManyField(MODELS[1], related_name='region_quality_mark')
	sub_region = models.ManyToManyField(MODELS[2], related_name='sub_region_quality_mark')
	c_type = models.ForeignKey(
		ContentType,
		on_delete=models.CASCADE,
		blank=True,
		null=True,
		)
	obj_id = models.CharField(
		max_length=64,
		blank=True,
		null=True,
		)
	content_object = GenericForeignKey('c_type', 'obj_id')

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('model4-change', kwargs={'pk': self.pk})


class Main(models.Model, metaclass=SelfMeta):
	country = models.ForeignKey(MODELS[0], on_delete=models.CASCADE, related_name='main_country')
	region = models.ForeignKey(MODELS[1], on_delete=models.CASCADE, related_name='main_region')
	sub_region = models.ForeignKey(MODELS[2], on_delete=models.CASCADE, related_name='main_sub_region')
	brand = models.ForeignKey(MODELS[3], on_delete=models.CASCADE, related_name='main_brand')

	def __str__(self):
		return f'{self.country} * {self.region} * {self.sub_region} * {self.brand}'
