from rest_framework import viewsets, permissions, filters
from main import models
from main.api import serializers
import django_filters


class StationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Station.objects.all()
    serializer_class = serializers.StationSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    search_fields = ['name', ]
    filter_backends = (filters.SearchFilter,)


class OrganizationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Organization.objects.all()
    serializer_class = serializers.OrganizationSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    search_fields = ['name', ]
    filter_backends = (filters.SearchFilter,)


class ApproachViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Approach.objects.all()
    serializer_class = serializers.ApproachSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    search_fields = ['name', ]
    filter_backends = (filters.SearchFilter,)


class EquipmentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Equipment.objects.all()
    serializer_class = serializers.EquipmentSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    search_fields = ['name', ]
    filter_backends = (filters.SearchFilter,)


class CompleteStatusViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.CompleteStatus.objects.all()
    serializer_class = serializers.CompleteStatusSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    search_fields = ['name', ]
    filter_backends = (filters.SearchFilter,)


class StageStatusViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.StageStatus.objects.all()
    serializer_class = serializers.StageStatusSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    search_fields = ['name', ]
    filter_backends = (filters.SearchFilter,)


class JournalStatusViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.JournalStatus.objects.all()
    serializer_class = serializers.JournalStatusSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    search_fields = ['name', ]
    filter_backends = (filters.SearchFilter,)


class EventsListViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.EventsList.objects.all()
    serializer_class = serializers.EventsListSerializer
    permission_classes = [permissions.IsAuthenticated, ]


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    search_fields = ['name', ]
    filter_backends = (filters.SearchFilter,)


class ApplicationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Application.objects.all()
    serializer_class = serializers.ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated, ]


class ExperimentPlanViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.ExperimentPlan.objects.all()
    serializer_class = serializers.ExperimentPlanSerializer
    permission_classes = [permissions.IsAuthenticated, ]


class ExperimentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Experiment.objects.all()
    serializer_class = serializers.ExperimentSerializer
    permission_classes = [permissions.IsAuthenticated, ]


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Event.objects.all()
    serializer_class = serializers.EventSerializer
    permission_classes = [permissions.IsAuthenticated, ]


class CommentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = [permissions.IsAuthenticated, ]


class ApplicationCounterViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.ApplicationCounter.objects.all()
    serializer_class = serializers.ApplicationCounterSerializer
    permission_classes = [permissions.IsAuthenticated, ]


class StationMarkViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.StationMark.objects.all()
    serializer_class = serializers.StationMarkSerializer
    permission_classes = [permissions.IsAuthenticated, ]


class StationMarkValueViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.StationMarkValue.objects.all()
    serializer_class = serializers.StationMarkValueSerializer
    permission_classes = [permissions.IsAuthenticated, ]
