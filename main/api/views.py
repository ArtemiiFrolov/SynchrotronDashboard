import numpy as np
import datetime

from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework import authentication, permissions
from django.contrib.auth.models import User

from main import models
from main.api import serializers

STATS_BINS = 50


def fit_to_size(a, l):
    w = np.zeros((l, *(a.shape[1:])))
    window_size = len(a) // (l + 1)
    for i in range(l):
        w[i] = a[window_size * i: window_size * (i + 1)].mean(axis=0)
    return w


def rebin_by_time(data, l):
    a = np.array(list(data.values_list('time', 'value')))
    min_time = a[:, 0].min()
    max_time = a[:, 0].max()
    delta = (max_time - min_time) / l

    res = []
    time = min_time + delta
    count = 0
    total = 0.0
    for i in a:
        if i[0] < time:
            count += 1
            total += i[1]
        elif count > 0:
            res.append({'time': time, 'value': total / count})
            total = 0.0
            count = 0
            time += delta

    return res


def rebin_by_array(data, l):
    a = np.array(list(data.values_list('time', 'value')))
    window = len(a) // l
    res = []
    for i in range(l):
        bin = a[i * window: (i + 1) * window]
        min_time = bin[:, 0].min()
        max_time = bin[:, 0].max()
        val = bin[:, 1].mean()
        res.append({'time': min_time + (max_time - min_time) / 2, 'value': val})
    return res


@api_view(['GET', 'POST'])
def stats(request, mark_pk):
    try:
        mark = models.StationMark.objects.get(pk=mark_pk)
    except models.ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        time_from = request.GET.get('from', None)
        time_to = request.GET.get('to', None)
        bins = int(request.GET.get('bins', STATS_BINS))
        data = models.StationMarkValue.objects.filter(mark=mark)
        if time_from is not None:
            data = data.filter(time__gte=time_from)
        if time_to is not None:
            data = data.filter(time__lte=time_to)
        if len(data) > bins:
            data = rebin_by_array(data, bins)
        serializer = serializers.StatsSerializer(data, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        is_many = isinstance(request.data, list)
        s = serializers.StatsSerializer(data=request.data, many=is_many,
                                                   context={'request': request, 'mark': mark})
        if s.is_valid():
            s.save()
            return Response(s.data, status=status.HTTP_201_CREATED)
        return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)
