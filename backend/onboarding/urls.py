"""URL patterns for onboarding API."""
from django.urls import path

from .views import FinishView, ReviewView, Step1View, Step2View, Step3View

app_name = 'onboarding'

urlpatterns = [
    path('step1/', Step1View.as_view(), name='step1'),
    path('step2/', Step2View.as_view(), name='step2'),
    path('step3/', Step3View.as_view(), name='step3'),
    path('review/', ReviewView.as_view(), name='review'),
    path('finish/', FinishView.as_view(), name='finish'),
]
