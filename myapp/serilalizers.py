from rest_framework import serializers
from .models import popup

class popup_serilalizer(serializers.ModelSerializer):
    class Meta:
        model = popup
        fields = '__all__'