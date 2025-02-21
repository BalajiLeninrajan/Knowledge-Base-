from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry_page, name="entry_page"),
    path("search", views.search, name="search"),
    path("random", views.random, name="random"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("new", views.new_entry, name="new")
]
