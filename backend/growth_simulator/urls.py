from django.urls import path
from .views import SimulationProjectView

urlpatterns = [
    path('project/', SimulationProjectView.as_view(), name='simulator-project'),
]
