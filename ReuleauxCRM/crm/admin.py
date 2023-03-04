from django.contrib import admin
from . import models
from django.apps import apps

app = apps.get_app_config('crm')

for model_name, model in app.models.items():
    admin.site.register(model)
