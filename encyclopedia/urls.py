from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>", views.webpages, name="webpages"),
    path("<str:search>", views.index, name="search")
]
