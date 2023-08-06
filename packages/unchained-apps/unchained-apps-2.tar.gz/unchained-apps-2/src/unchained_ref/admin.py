from django.apps import apps
from django.contrib import admin
from .apps import DjAppConfig


models = apps.get_app_config(DjAppConfig.name).get_models()


# Keep this the last after all manual registeration
for model in models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
