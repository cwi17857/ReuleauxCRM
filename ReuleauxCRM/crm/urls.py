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
router.register('transection', views.TransactionViewSet)



urlpatterns = [
    path('', include(router.urls)),
    path('search/',views.ProjectListView.as_view(), name="project_search"),

]