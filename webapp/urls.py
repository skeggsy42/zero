from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('quotes/', views.quotes, name='quotes'),
]
