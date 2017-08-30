from __future__ import unicode_literals

import django.utils.timezone as tz

from main import models
from rest_framework import serializers


class StationSerializer(serializers.ModelSerializer):
    marks = serializers.HyperlinkedIdentityField(view_name='api:station-marks', read_only=True)

    class Meta:
        model = models.Station
        fields = '__all__'


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Organization
        fields = '__all__'


class ApproachSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Approach
        fields = '__all__'


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Equipment
        fields = '__all__'


class CompleteStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CompleteStatus
        fields = '__all__'


class StageStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StageStatus
        fields = '__all__'


class JournalStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.JournalStatus
        fields = '__all__'


class EventsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EventsList
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = '__all__'


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Application
        fields = '__all__'


class ExperimentPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ExperimentPlan
        fields = '__all__'


class ExperimentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Experiment
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Event
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = '__all__'


class ApplicationCounterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ApplicationCounter
        fields = '__all__'


class StationMarkSerializer(serializers.ModelSerializer):
    values = serializers.HyperlinkedIdentityField(view_name='api:mark_values-detail',
                                                  lookup_field='pk', read_only=True)
    stats = serializers.HyperlinkedIdentityField(view_name='api:station_mark-stats', read_only=True)

    class Meta:
        model = models.StationMark
        fields = '__all__'


class StationMarkValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StationMarkValue
        fields = ('time', 'value')

    def create(self, validated_data):
        if 'mark' not in validated_data:
            validated_data['mark'] = self.context['mark']
        return super(StationMarkValueSerializer, self).create(validated_data)


class StatsSerializer(serializers.Serializer):
    time = serializers.DateTimeField(default=tz.now)
    value = serializers.FloatField()

    def create(self, validated_data):
        if 'mark' not in validated_data:
            validated_data['mark'] = self.context['mark']
        return models.StationMarkValue.objects.create(**validated_data)



