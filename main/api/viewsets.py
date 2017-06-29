from rest_framework import viewsets, permissions
from main import models
from main.api import serializers


class StationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Station.objects.all()
    serializer_class = serializers.StationSerializer
    permission_classes = [permissions.IsAuthenticated, ]

