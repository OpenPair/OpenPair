from rest_framework import serializers
from .models import LatestCount

class CurrentCountSerializer(serializers.ModelSerializer):

    class Meta:
        model = LatestCount
        fields = ['id', 'current_count', 'author']
        extra_kwargs = {'author': {'read_only': True}}