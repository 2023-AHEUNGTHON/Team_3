from rest_framework import serializers
from .models import Popup

class popup_serilalizer(serializers.ModelSerializer):
    class Meta:
        model = Popup
        fields = '__all__'