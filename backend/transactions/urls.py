from django.urls import path
from . import views

urlpatterns = [
    path('', views.transaction_list_view, name='transaction-list'),
    path('import-csv/', views.import_csv_view, name='transaction-import-csv'),
    path('demo/', views.demo_data_view, name='transaction-demo'),
    path('<uuid:tx_id>/correct/', views.correct_category_view, name='transaction-correct'),
    path('<uuid:tx_id>/delete/', views.delete_transaction_view, name='transaction-delete'),
    path('analytics/', views.analytics_view, name='transaction-analytics'),
]
