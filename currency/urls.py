from django.urls import path
from . import views

urlpatterns = [
    path("convert/", views.convert, name="convert"),
    path("currencies/", views.currencies, name="currencies"),
    path("latest/", views.latest, name="latest"),
]
