from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.create, name="create"),
    path("edit", views.edit, name="edit"),
    path("<str:title>", views.webpages, name="webpages"),
    path("", views.random, name="random")
]
