from .models import *
from rest_framework.serializers import ModelSerializer


class FacSerial(ModelSerializer):
    class Meta:
        model= Facture
        fields='__all__'
        