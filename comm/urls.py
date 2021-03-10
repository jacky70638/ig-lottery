from django.urls import path
from . import views

urlpatterns = [
    path('', views.comm),
    path('comm',views.ig),
]