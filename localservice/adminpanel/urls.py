# adminpanel/urls.py
from django.urls import path
from . import views

app_name = 'adminpanel'

urlpatterns = [
    path('login/', views.admin_login, name='login'),
    path('logout/', views.admin_logout, name='logout'),
    path('', views.dashboard, name='dashboard'),

    # categories
    path('categories/', views.list_categories, name='categories'),
    path('categories/add/', views.add_category, name='add_category'),
    path('categories/delete/<str:cat_id>/', views.delete_category, name='delete_category'),

    # providers
    path('providers/', views.list_providers, name='providers'),
    path('providers/delete/<str:prov_id>/', views.delete_provider, name='delete_provider'),

    # customers
    path('customers/', views.list_customers, name='customers'),
    path('customers/delete/<str:cust_id>/', views.delete_customer, name='delete_customer'),

    # services
    path('services/', views.list_services, name='services'),
    path('services/remove-duplicate/', views.remove_duplicate_services, name='remove_duplicate_services'),

    # reviews
    path('reviews/', views.list_reviews, name='reviews'),
]
