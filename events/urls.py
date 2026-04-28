from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('certificate/<int:reg_id>/', views.generate_certificate, name='certificate'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
]
