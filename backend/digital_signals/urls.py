from django.urls import path
from . import views

urlpatterns = [
    path('', views.digital_signals_view, name='digital-signals'),
    path('features/', views.derived_features_view, name='digital-signals-features'),
]
