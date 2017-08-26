from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics, mixins, views

import django_filters
import numpy as np

from main import models
from main.api import serializers


class FilteredModelViewSet(viewsets.ModelViewSet):
    """
    The actions provided by the ModelViewSet class are:
        .list(), .retrieve(), .create(), .update(), .partial_update(), and .destroy().
    """
    NESTED_LIST_MAPPING = {
        'get': 'list',
        'post': 'create'
    }
    filter_kwargs = None  # required by ModelViewSet

    def __init__(self, queryset=None, filter_kwargs=None, **kwargs):
        super(FilteredModelViewSet, self).__init__(**kwargs)
        if queryset:
            self.queryset = queryset
        elif filter_kwargs:
            self.queryset = self.queryset.filter(**filter_kwargs)
            self.filter_kwargs = filter_kwargs

    @classmethod
    def as_filtered_view(cls, mapping=NESTED_LIST_MAPPING, queryset=None, **kwargs):
        return cls.as_view(mapping, queryset=queryset, filter_kwargs=kwargs)

    @classmethod
    def proceed_filtered(cls, request, mapping=NESTED_LIST_MAPPING, queryset=None, **kwargs):
        if request.method in ('POST', 'PUT', 'PATCH', 'DELETE'):
            """
            For some reason we can't directly redirect POST-like methods to cls.as_view because of
            csrf_excempt and other stuff so request body become touched.
            We need to construct the request handler ourselves.
            """
            viewset = cls(queryset=queryset, filter_kwargs=kwargs)
            viewset.request = request
            viewset.format_kwarg = None
            if str.lower(request.method) not in mapping:
                raise RuntimeError('Method %s can\'t be proceeded' % request.method)
            action = getattr(viewset, mapping[str.lower(request.method)])
            return action(request)
        return cls.as_view(mapping, queryset=queryset, filter_kwargs=kwargs)(request)


class StationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Station.objects.all()
    serializer_class = serializers.StationSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    search_fields = ['name', ]
    filter_backends = (filters.SearchFilter,)

    @detail_route(['GET'])
    def marks(self, request, pk=None):
        return StationMarkViewSet.proceed_filtered(request, station=self.get_object())


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


class StationMarkViewSet(FilteredModelViewSet):
    queryset = models.StationMark.objects.all()
    serializer_class = serializers.StationMarkSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    @detail_route(methods=['get', 'post'])
    def values(self, request, pk=None):
        return StationMarkValueViewSet.proceed_filtered(request, mark=self.get_object())
        if request.method == 'GET':

            values = mark.values.all()
            values_list = [(val.created, val.value) for val in values]
            return Response(values_list)
        elif request.method == 'POST':
            pass
        return Response(status=status.HTTP_404_NOT_FOUND)

    @detail_route(methods=['get'])
    def stats(self, request, pk=None):
        bins = int(request.GET.get('bins', 10))
        mark = self.get_object()
        values = mark.values.all()
        raw = [val.value for val in values]
        if len(raw) > 0:
            hist_values, hist_edges = np.histogram(raw, bins=bins)
            return Response({'min': np.min(raw),
                             'max': np.max(raw),
                             'mean': np.mean(raw),
                             'len': len(raw),
                             'histogram': {
                                 'values': hist_values,
                                 'edges': hist_edges
                             },
                             'std': np.std(raw)})
        return Response({'len': len(raw)})


class StationMarkValueViewSet(FilteredModelViewSet):
    queryset = models.StationMarkValue.objects.all()
    serializer_class = serializers.StationMarkValueSerializer
    permission_classes = [permissions.IsAuthenticated, ]


class StationMarkValuesViewSet(viewsets.ViewSet):
    def list(self, request):
        q = models.StationMarkValue.objects.all()
        serializer = serializers.StationMarkValueSerializer(q, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        q = models.StationMarkValue.objects.filter(mark=pk)
        s = serializers.StationMarkValueSerializer(q, many=True)
        return Response(s.data)

    def update(self, request, pk=None):
        mark = models.StationMark.objects.get(pk=int(pk))
        is_many = isinstance(request.data, list)
        s = serializers.StationMarkValueSerializer(data=request.data, many=is_many,
                                                   context={'request': request, 'mark': mark})
        if s.is_valid():
            s.save()
            return Response(s.data, status=status.HTTP_201_CREATED)
        return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)

