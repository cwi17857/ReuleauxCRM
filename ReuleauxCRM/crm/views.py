from django.shortcuts import render
from crm import serializers, models
# Create your views here.


####
from django.core import exceptions
from django_filters import rest_framework as filters
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import  action
from rest_framework import generics,filters

from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

####

class ProjectViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating Project items"""
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.ProjectSerializer
    queryset = models.Project.objects.all()

class SessionViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating Project items"""
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.SessionSerializer
    queryset = models.Session.objects.all()

class TransactionViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating Project items"""
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.TransactionSerializer
    queryset = models.Transaction.objects.all()

class ProjectListView(generics.ListAPIView):
    queryset = models.Project.objects.all()
    serializer_class = serializers.ProjectSearchSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['proj_id', 'proj_title', 'customer__first_name','customer__last_name']
    