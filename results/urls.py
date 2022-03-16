from django.urls import path, re_path
from results import views

app_name = 'results'

urlpatterns = [
    path('declare/', views.declare_result_view, name='declare_result'),
    path('update/<int:pk>/', views.result_update_view, name='update_result'),
    path('delete/<int:pk>/', views.result_delete_view, name='delete_result'),
    # path('declare/class_based/', views.DeclareResultCreateView.as_view(), name='declare_result'),
    path('list/', views.DeclareResultListView.as_view(), name='result_list'),
    path('declare/validate/', views.validate_data, name='validate_data'),
    path('declare/setup/', views.setup_update_view, name='setup'),
    path('pdf/', views.venue_pdf, name='setup1'),
     path('pdf1/', views.venue_pdf1, name='setup2'),
]
