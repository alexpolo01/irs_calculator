from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('compute_tax', views.compute_tax, name='compute_tax'),  
]
