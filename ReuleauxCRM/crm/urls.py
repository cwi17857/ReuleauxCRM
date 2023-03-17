"""
    Register API URLS under ecm app
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from crm import views

app_name = 'crm'

router = DefaultRouter()

router.register('project', views.ProjectViewSet)
router.register('estimate', views.EstimateViewSet)
router.register('session', views.SessionViewSet)
router.register('service', views.ServiceViewSet)
router.register('deliverable', views.DeliverableViewSet)
router.register('transection', views.TransactionViewSet)
router.register('generate_estimate', views.GenerateEstimateViewSet)



urlpatterns = [
    path('', include(router.urls)),
    # path('search/',views.ProjectListView.as_view(), name="project_search"),
]