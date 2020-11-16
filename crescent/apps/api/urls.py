from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("learn", views.learn),
    path("generate", views.generate),
    path("unknown-words/pop", views.pop_unknown_words),
]
