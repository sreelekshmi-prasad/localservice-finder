from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  # Homepage with both options
    path('customers/', include('customers.urls')),  # Customer login/signup
    path('providers/', include('providers.urls')),  # Provider login/signup
    path('adminpanel/', include('adminpanel.urls')),
]
