from __future__ import unicode_literals

from main import models
from rest_framework import serializers


class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Station
        fields = '__all__'
