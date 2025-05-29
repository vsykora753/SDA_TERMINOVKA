"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from events.views import EventListView,TerminovkaView,EventDetailView
from users.views import RegisterView,  LoginView as UserLoginView


urlpatterns = [
    path("admin/", admin.site.urls),

    # Události
    path('', EventListView.as_view(), name='events_list'),
    path('terminovka/', TerminovkaView.as_view(), name='events_search'),
    path('<int:pk>/', EventDetailView.as_view(), name='event_details'),


    # Uživatelské účty
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    
    
]
