from django.utils import timezone
from django.db import transaction
from rest_framework import serializers
from crm import models



class SessionsServicesMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SessionsServicesMap
        fields = '__all__'

class SessionSerializer(serializers.ModelSerializer):
    services = SessionsServicesMapSerializer(many=True)
    event_location = serializers.StringRelatedField(source = 'location')
    class Meta:
        model = models.Session
        fields = ['session_name','sess_id', 'date','start_time', 'end_time','event_location', 'services']


class ProjectSerializer(serializers.ModelSerializer):
    """Serializer for Project"""
    session = SessionSerializer(many=True)
    customer_fname = serializers.StringRelatedField(source = 'customer.first_name',read_only = True)
    customer_lname = serializers.StringRelatedField(source = 'customer.last_name',read_only = True)
    class Meta:
        model = models.Project
        fields = ['id','proj_title', 'proj_id','proj_type','project_status','customer_fname','customer_lname','customer', 'lead_source','session']
    def create(self, validated_data):
        ## Creating Project
        sessions = validated_data.pop('session')
        project = models.Project.objects.create(**validated_data)
        project.proj_id = "TS"+str(project.id).zfill(6)
        project.save()
        for session in sessions:
            #Creating Sessions
            services = session.pop('services')
            project = project
            session_name = session.get('session_name','')
            location = session.get('location','')
            date = session.get('date')
            start_time = session.get('start_time')
            end_time = session.get('end_time')
            sess = models.Session.objects.create(services=services,project=project,session_name=session_name,location=location,date=date,start_time=start_time,end_time=end_time)
            sess_id = "SS"+str(sess.id).zfill(7)
            sess(sess_id=sess_id)
            sess.save()
            for srv in services:
                session = sess
                service = srv.get('service','')
                qty = srv.get('qty',1)
                unit_cost = srv.get('qty',1)
                srv_sess = models.SessionsServicesMap(session=session,service=service,qty=qty,unit_cost=unit_cost,total_cost=unit_cost*qty)
                srv_sess.save()
        return project
        #ToDo Update Function
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)



class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Transaction
        fields = '__all__'

class ProjectSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Project
        fields = ['id', 'proj_id', 'proj_title']
