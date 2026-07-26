from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile_overview, name='profile-overview'),
    path('update/', views.update_profile_view, name='profile-update'),
    path('goals/', views.goals_list_create, name='profile-goals-list-create'),
    path('goals/<uuid:id>/', views.goal_detail, name='profile-goal-detail'),
    path('goals/<uuid:id>/contribute/', views.goal_contribute, name='profile-goal-contribute'),
    path('goals/<uuid:id>/set-active/', views.set_active_goal_view, name='profile-goal-set-active'),
    path('services/', views.connected_services_view, name='profile-connected-services'),
    path('services/<str:service_type>/', views.add_service_view, name='profile-add-service'),
    path('services/<str:service_type>/<uuid:id>/', views.remove_service_view, name='profile-remove-service'),
    path('timeline/', views.timeline_view, name='profile-timeline'),
    path('explainability/', views.explainability_view, name='profile-explainability'),
    path('export/', views.export_data_view, name='profile-export'),
]
