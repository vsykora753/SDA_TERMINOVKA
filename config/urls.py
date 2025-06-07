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

import debug_toolbar
from django.contrib import admin
from django.conf import settings
from django.urls import path,include
from events.views import EventListView,TerminovkaView,EventDetailView
from users.views import UserRegisterView, OrganizerRegisterView, user_dashboard, organizer_dashboard, UserLoginView, OrganizerLoginView
from users.views import UserRegistrationSuccessView, OrganizerRegistrationSuccessView,UserLogoutView,OrganizerEventListView,OrganizerEventCreateView,OrganizerEventEditView,OrganizerEventDeleteView

if settings.DEBUG:
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] 


urlpatterns = [
    path("admin/", admin.site.urls),

    # Události
    path('', EventListView.as_view(), name='events_list'),
    path('terminovka/', TerminovkaView.as_view(), name='events_search'),
    path('<int:pk>/', EventDetailView.as_view(), name='event_details'),


    # Uživatelské účty
    path('register/user/', UserRegisterView.as_view(), name='user_register'),
    path('registrace/uzivatel/uspesna/', UserRegistrationSuccessView.as_view(), name='user_registration_success'),
    path('login/user/', UserLoginView.as_view(), name='user_login'),
    path('user/dashboard/', user_dashboard, name='user_dashboard'),    
    path('user/logout/', UserLogoutView.as_view(), name='user_logout'),


    # Organizátoři
    path('register/organizer/', OrganizerRegisterView.as_view(), name='organizer_register'),
    path('login/organizer/', OrganizerLoginView.as_view(), name='organizer_login'), 
    path('registrace/organizator/uspesna/', OrganizerRegistrationSuccessView.as_view(), name='organizer_registration_success'),
    path('organizer/dashboard/', organizer_dashboard, name='organizer_dashboard'),

    # Udalosti organizátora
    path('organizer/events/',OrganizerEventListView.as_view(), name='organizer_event_list'),
    path('organizer/events/create/', OrganizerEventCreateView.as_view(), name='organizer_event_create'),
    path('organizer/events/<int:pk>/update/', OrganizerEventEditView.as_view(), name='organizer_event_update'), 
    path('organizer/events/<int:pk>/delete/', OrganizerEventDeleteView.as_view(), name='organizer_event_delete'),

]

