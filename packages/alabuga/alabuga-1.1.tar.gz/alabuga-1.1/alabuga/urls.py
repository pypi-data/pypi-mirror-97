from django.urls import path

from .views import (
	Model1View, 
	Model1AddView, 
	Model1ChangeView, 
	Model1DeleteView, 
	Model1FormSetView,
	#
	Model2View,
	Model2AddView,
	Model2ChangeView,
	Model2DeleteView,
	Model2FormSetView,
	#
	Model4View,
	Model4AddView,
	Model4ChangeView,
	Model4DeleteView,
	Model4FormSetView,
	Model5View,
	Model5AddView,
	region_to_json,
	sub_region_to_json,
	brand_to_json,
	)

urlpatterns = [
	path('model1-view/', Model1View.as_view(), name='model1-view'),
	path('model1-add/', Model1AddView.as_view(), name='model1-add'),
	path('model1-formset/', Model1FormSetView.as_view(), name='model1-formset'),
	path('model1-change/<int:pk>/', Model1ChangeView.as_view(), name='model1-change'),
	path('model1-delete/<int:pk>/', Model1DeleteView.as_view(), name='model1-delete'),
	#
	path('model2-view/', Model2View.as_view(), name='model2-view'),
	path('model2-add/', Model2AddView.as_view(), name='model2-add'),
	path('model2-change/<int:pk>/', Model2ChangeView.as_view(), name='model2-change'),
	path('model2-delete/<int:pk>/', Model2DeleteView.as_view(), name='model2-delete'),
	path('model2-formset/<int:pk>/', Model2FormSetView.as_view(), name='model2-formset'),
	#
	path('model4-view/', Model4View.as_view(), name='model4-view'),
	path('model4-add/', Model4AddView.as_view(), name='model4-add'),
	path('model4-change/<int:pk>/', Model4ChangeView.as_view(), name='model4-change'),
	path('model4-delete/<int:pk>/', Model4DeleteView.as_view(), name='model4-delete'),
	path('model4-formset/<int:pk>/', Model4FormSetView.as_view(), name='model4-formset'),
	#
	path('model5-view/', Model5View.as_view(), name='model5-view'),
	path('model5-add/', Model5AddView.as_view(), name='model5-add'),
	#
	path('regions/<int:pk>/', region_to_json, name='regions'),
	path('sub-regions/<int:pk>/', sub_region_to_json, name='sub-regions'),
	path('brands/', brand_to_json, name='brands'),
]
