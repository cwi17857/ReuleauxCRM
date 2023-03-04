from django.utils import timezone
from django.db import transaction
from rest_framework import serializers
from crm import models


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Session
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    """Serializer for Project"""
    session = SessionSerializer(many=True,read_only=True)
    # project_type = serializers.StringRelatedField(source = 'proj_type.name')
    # customer_fname = serializers.StringRelatedField(source = 'customer.first_name')
    # customer_lname = serializers.StringRelatedField(source = 'customer.last_name')
    # customer_id = serializers.IntegerField(source='customer.id')
    # lead_source = serializers.StringRelatedField(source='lead_source.name')
    

    class Meta:
        model = models.Project
        fields = ['id', 'proj_id', 'proj_title', 'proj_title','session']


