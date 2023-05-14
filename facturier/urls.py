from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('',AccueilView.as_view(),name='accueil' ),
    path('addclient',AddClient.as_view(),name='addclient'),
    path('addfacture',AddFacture.as_view(),name='addfacture')
]
