from __future__ import unicode_literals

from main import models
from rest_framework import serializers


class StationSerializer(serializers.ModelSerializer):
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


class RightSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Right
        fields = '__all__'


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Role
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
