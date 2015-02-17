from django.contrib import admin
from django.db.models.loading import get_app, get_models

app = get_app('dynamic_models')
admin.site.register(get_models(app))