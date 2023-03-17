from django.shortcuts import render, get_object_or_404
from crm import serializers, models



####
from django.core import exceptions
from django_filters import rest_framework as filters
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import  action
from rest_framework import generics,filters
from rest_framework.views import APIView

from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

class ProjectViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating Projects"""
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.ProjectSerializer
    queryset = models.Project.objects.all()


class EstimateViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating Estimates"""
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.EstimateSerializer
    queryset = models.Estimate.objects.all()    

class GenerateEstimateViewSet(viewsets.ModelViewSet):
    """Handles creating, Estimates"""
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.GenerateEstimateSerializer
    queryset = models.Estimate.objects.all()

    def get_queryset(self):
        queryset = models.Estimate.objects.all()
        return queryset.filter(id=self.kwargs.get('pk'))

    @action(detail=True, methods=['patch'])
    def approve(self,request, pk=None):
        queryset = self.queryset
        project= request.data.get('project','')
        estimate = get_object_or_404(queryset, pk=pk)
        if estimate and project==estimate.project.id:
            if not estimate.is_approved:
                estimate.is_approved = True
                estimate.save()
                project = models.Project.objects.get(pk = estimate.project.id)
                for session in estimate.es_sessions.all():
                    project.sessions.add(session)
                for dliverable in estimate.es_dliverables.all():
                    project.dliverables.add(dliverable)
                project.save()
        return Response({'message':'Esitimate Approved and added to project'}, status=status.HTTP_200_OK )

class SessionViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating Project items"""
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.SessionSerializer
    queryset = models.Session.objects.all()

class ServiceViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating Project items"""
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.ServiceSerializer
    queryset = models.Service.objects.all()

class DeliverableViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating Project items"""
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.DeliverableSerializer
    queryset = models.Deliverable.objects.all()

class TransactionViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating Project items"""
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.TransactionSerializer
    queryset = models.Transaction.objects.all()


    