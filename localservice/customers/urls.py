from django.urls import path
from . import views

app_name = 'customers'

urlpatterns = [
    path("signup/", views.customer_signup, name="signup"),
    path("login/", views.customer_login, name="login"),
    path("dashboard/", views.customer_dashboard, name="dashboard"),
    path("service/<service_id>/slots/", views.view_slots, name="view_slots"),
    path("book/<slot_id>/", views.book_slot, name="book_slot"),
    path("my-bookings/", views.my_bookings, name="my_bookings"),
    path("logout/", views.customer_logout, name="logout"),
]
