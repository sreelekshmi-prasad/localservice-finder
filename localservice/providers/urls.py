from django.urls import path
from . import views

app_name = 'providers'

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("add-slot/", views.add_slot, name="add_slot"),
    path('edit-slot/<str:slot_id>/', views.edit_slot, name='edit_slot'),
    path('delete-slot/<str:slot_id>/', views.delete_slot, name='delete_slot'),
    path("add-service/", views.add_service_view, name="add_service"),
    path('booked-customers/', views.booked_customers, name='booked_customers'),
    path('logout/', views.logout_view, name='logout'),
]

