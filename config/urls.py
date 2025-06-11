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
from django.conf import settings
from django.urls import path, include

# importy pohledu pro  zobrazení událostí, registrace uživatelů a organizátorů

from events.views import EventListView,TerminovkaView,EventDetailView,EventRegisterView
from users.views import UserRegisterView, OrganizerRegisterView
from users.views import user_dashboard, organizer_dashboard, Myhomepage_view
from users.views import UserRegistrationSuccessView,RoleBasedLoginView
from users.views import OrganizerRegistrationSuccessView,UserLogoutView
from users.views import OrganizerEventListView,OrganizerEventCreateView
from users.views import OrganizerEventEditView,OrganizerEventDeleteView
from registrations.views import RegistrationListView




urlpatterns = [
    path("admin/", admin.site.urls),

    # Události
    path('', Myhomepage_view, name='home'),
    path('events/', EventListView.as_view(), name='events_list'),
    

    path('terminovka/', TerminovkaView.as_view(), name='events_search'),
    path('<int:pk>/', EventDetailView.as_view(), name='event_details'),
    path('<int:pk>/prihlasit/', EventRegisterView.as_view(), name='event_register'),


    # Uživatelské účty
    path('register/user/', UserRegisterView.as_view(), name='user_register'),
    path('registrace/uzivatel/uspesna/', UserRegistrationSuccessView.as_view(),
        name='user_registration_success'),

    path('login/user/', RoleBasedLoginView.as_view(
        template_name='user/user_login.html'),
        name='user_login'),

    path('user/dashboard/', user_dashboard, name='user_dashboard'),    
    path('user/logout/', UserLogoutView.as_view(), name='user_logout'),


    # Organizátoři
    path('register/organizer/', OrganizerRegisterView.as_view(),
        name='organizer_register'),

    path('login/organizer/', RoleBasedLoginView.as_view(
        template_name='organizer/organizer_login.html'),
        name='organizer_login'),

    path('registrace/organizator/uspesna/', 
        OrganizerRegistrationSuccessView.as_view(),
        name='organizer_registration_success'),

    path('organizer/dashboard/', organizer_dashboard,
        name='organizer_dashboard'),

    path('organizer/logout/', UserLogoutView.as_view(),
        name='organizer_logout'),

    # Udalosti organizátora
    path('organizer/events/',OrganizerEventListView.as_view(),
        name='organizer_event_list'),

    path('organizer/events/create/', 
        OrganizerEventCreateView.as_view(), name='organizer_event_create'),

    path('organizer/events/<int:pk>/update/', OrganizerEventEditView.as_view(),
        name='organizer_event_update'), 

    path('organizer/events/<int:pk>/delete/', 
        OrganizerEventDeleteView.as_view(), name='organizer_event_delete'),

    path('event/<int:event_id>/registrations/',
        RegistrationListView.as_view(), name='registration_list'),

]

