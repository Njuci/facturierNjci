from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('',AccueilView.as_view(),name='accueil' ),
    path('addclient',AddClient.as_view(),name='addclient'),
    path('addfacture',AddFacture.as_view(),name='addfacture'),
    path('invoice_visualization/<int:pk>',voirArticleHtm.as_view(),name='invoice_visualization'),
    path('generate/<int:pk>',get_fac,name='generate')
    
]
