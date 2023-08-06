from django.urls import path
from . import views

urlpatterns = [
    # A simple test page
    path('status', views.export_status, name='status'),
    path('models', views.export_models, name='models'),
]
