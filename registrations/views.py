from django.shortcuts import render
from django.views.generic import ListView
from .models import Registration


class RegistrationListView(ListView):
    """
    View for displaying a list of registrations for a specific event.
    """ 

    model = Registration
    template_name = 'registration_list.html'
    context_object_name = 'registrations'

    def get_queryset(self):
        """
        Returns the queryset of registrations for the specific event.
        """
        event_id = self.kwargs.get('event_id')
        return Registration.objects.filter(id_event_id=event_id).select_related('id_user' ).order_by('id_user__last_name')

        