from django.utils import timezone
from django.db import transaction
from rest_framework import serializers
from crm import models
from crm.constants import *


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Transaction
        fields = '__all__'

class DeliverableSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Deliverable
        fields = '__all__'

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Service
        fields = '__all__'

class SessionSerializer(serializers.ModelSerializer):
    services = ServiceSerializer(many=True)
    session_cost = serializers.CharField(read_only=True)
    class Meta:
        model = models.Session
        fields = '__all__'
        read_only_fields = ('sess_id','session_cost')

class ProjectSerializer(serializers.ModelSerializer):
    sessions = SessionSerializer(many=True,read_only=True)
    dliverables = DeliverableSerializer(many=True, read_only=True)
    class Meta:
        model = models.Project
        fields = '__all__'
        read_only_fields = ('proj_id', )
    
    def create(self, validated_data):
        project_new = models.Project.objects.create(**validated_data)
        project_new.proj_id = PROJECT_CODE_PREFIX+ str(project_new.id).zfill(PROJECT_CODE_LEN)
        project_new.save()
        return project_new

class DeliverableSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Deliverable
        fields = '__all__'

class EstimateSerializer(serializers.ModelSerializer):
    es_dliverables = DeliverableSerializer(many=True,)
    es_sessions = SessionSerializer(many=True,)
    total_cost = serializers.CharField()
    class Meta:
        model = models.Estimate
        fields = '__all__'
        read_only_fields = ('es_id', )

class GenerateEstimateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=50, write_only=True)
    last_name = serializers.CharField(max_length=50, write_only=True)
    email = serializers.EmailField(required=False, write_only=True)
    phone = serializers.CharField(max_length=13, write_only=True)
    proj_type = serializers.IntegerField(write_only=True)
    proj_title= serializers.CharField(max_length=50, write_only=True)
    lead_source = serializers.IntegerField(write_only=True)
    shipping_address= serializers.CharField(max_length=100, write_only=True) 
    es_dliverables = DeliverableSerializer(many=True,)
    es_sessions = SessionSerializer(many=True, )
    class Meta:
        model = models.Estimate
        fields = '__all__'
        read_only_fields = ('es_id','project', 'is_approved' )

    
    def create_user(self, user_details):
        try:
            user = models.User.objects.get(phone=user_details.get('phone'))
            return user
        except:
            user = models.User.objects.create(**user_details)
        return user
    
    def get_project_type(self, id):
        return models.ProjectType.objects.get(id=id)
 
    def get_lead_source(self, id):
        return models.LeadSource.objects.get(id=id)

    def create(self, validated_data):
        first_name = validated_data.get('first_name','')
        last_name = validated_data.get('last_name','')
        phone = validated_data.get('phone','')
        email = validated_data.get('email','')
        user_details = {'phone':phone,'first_name':first_name, 'last_name':last_name, 'email':email}
        user = self.create_user(user_details)

        proj_type = self.get_project_type(validated_data.get('proj_type',1))
        proj_title = validated_data.get('proj_title',DEFAULT_TEXT)
        lead_source = self.get_lead_source(validated_data.get('lead_source',1))
        shipping_address = validated_data.get('shipping_address',DEFAULT_TEXT)

        project = models.Project.objects.create(proj_type=proj_type, proj_title=proj_title,lead_source=lead_source, shipping_address=shipping_address, customer=user )
        project.proj_id = PROJECT_CODE_PREFIX + str(project.id).zfill(PROJECT_CODE_LEN)
        project.save()

        estimate = models.Estimate.objects.create(project=project)
        estimate.es_id = ESTIMATE_CODE_PREFIX + str(estimate.id).zfill(ESTIMATE_CODE_LEN)
        estimate.save()

        es_dliverables = validated_data.pop('es_dliverables')
        es_sessions = validated_data.pop('es_sessions')

        for dliverable in es_dliverables:
            dliverable_new = models.Deliverable.objects.create(**dliverable)
            estimate.es_dliverables.add(dliverable_new)
        for session in es_sessions:
            services = session.pop('services')
            session_new = models.Session.objects.create(**session)
            session_new.sess_id = SESSION_CODE_PREFIX + str(session_new.id).zfill(SESSION_CODE_LEN)
            session_new.save()
            for service in services:
                service_new = models.Service.objects.create(**service)
                session_new.services.add(service_new)
            estimate.es_sessions.add(session_new)        
        return estimate