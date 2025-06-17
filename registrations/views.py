
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from .models import Event, Registration 
from .forms import RegistrationForm
from django.shortcuts import render
import pandas as pd
from django.http import HttpResponse
from io import BytesIO



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
        return Registration.objects.filter(
            id_event_id=event_id).select_related(
            'id_user' ).order_by('id_user__last_name')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event'] = get_object_or_404(Event, id=self.kwargs['event_id']) 
        return context

@login_required
def register_for_event(request, event_id):
    """
    Handles the registration of a logged-in user for a specific event (race).

    - If the user is not logged in, they will be redirected to the login page.
    - If the user is already registered for the event, a message will be shown.
    - If the user is not registered:
        - On a GET request, a blank registration form is displayed.
        - On a POST request, the form is validated 
        and a new registration is created.

    Parameters:
    - request: The HttpRequest object.
    - event_id: The ID (primary key) of the Event 
        the user wants to register for.

    Returns:
    - HttpResponse: 
    Renders one of the templates (
    form, success message, or already registered message).

    """
    event = get_object_or_404(Event, pk=event_id)
    
    
    if Registration.objects.filter(
        id_user=request.user, id_event=event).exists():
        return render(request, 'already_registered.html', {'event': event})

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save(commit=False)
            registration.id_user = request.user
            registration.id_event = event
            registration.save()
            return render(request,
            'registration_success.html', {'event': event})
    else:
        form = RegistrationForm()

    return render(request, 'registration_form.html', {
        'form': form,
        'event': event
    })

def generate_results_template(request, event_id):
    """
    Generates an Excel file template for results of a specific event.   
    The template includes columns for user ID, event ID, and result time.
    """
    event = get_object_or_404(Event, id=event_id)
    
    registrations = Registration.objects.filter(
        id_event_id=event.id).select_related('id_user')
    
    data = []
    for reg in registrations:
        user = reg.id_user
        data.append({
            'id_user_id': user.id,
            'jméno': f"{user.first_name} {user.last_name}",
            'email': user.email,
            'kategorie': reg.category,
            'id_event_id': event.id,
            'result_time': ''
        })

    df = pd.DataFrame(data)
    
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Results' )
    output.seek(0)
    
    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    filename = f"Results_event_{event.id}.xlsx"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response
