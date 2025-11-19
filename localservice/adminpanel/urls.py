# adminpanel/urls.py
from django.urls import path
from . import views

app_name = 'adminpanel'

urlpatterns = [
    path('login/', views.admin_login, name='login'),
    path('logout/', views.admin_logout, name='logout'),
    path('', views.dashboard, name='dashboard'),

    # providers
    path('providers/', views.list_providers, name='providers'),
    path('providers/approve/<str:provider_id>/', views.approve_provider, name='approve_provider'),
    path('providers/delete/<str:provider_id>/', views.delete_provider, name='delete_provider'),


    # customers
    path('customers/', views.list_customers, name='customers'),
    path('customers/delete/<str:cust_id>/', views.delete_customer, name='delete_customer'),

    # services
    path('services/', views.list_services, name='services'),
    path('services/remove-duplicate/', views.remove_duplicate_services, name='remove_duplicate_services'),

    # reviews
    path('reviews/', views.list_reviews, name='reviews'),
]
