from django.urls import path
from . import views

app_name = 'customers'

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),  # <-- change customer_login to login_view
]
