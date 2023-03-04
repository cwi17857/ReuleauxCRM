"""
    Register API URLS under ecm app
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from crm import views

app_name = 'ecm'

router = DefaultRouter()

router.register('project', views.ProjectViewSet)
router.register('session', views.SessionViewSet)


urlpatterns = [
    path('', include(router.urls)),
]