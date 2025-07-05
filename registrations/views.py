from io import BytesIO
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
import pandas as pd

from .models import Event, Registration
from .forms import RegistrationForm


class RegistrationListView(ListView):
    """
    Displays a list of registrations for a specific event.

    Retrieves all Registration objects for the specified event_id, sorts them
    by user last name, and displays them in the template.
    """

    model = Registration
    template_name = 'registration_list.html'
    context_object_name = 'registrations'

    def get_queryset(self):
        """
        Returns a queryset of registrations for the given event.

        Read:
            self.kwargs['event_id']: Event ID from URL.

        Returns:
            Registrations sorted by id_user__last_name.
        """

        event_id = self.kwargs.get('event_id')
        return Registration.objects.filter(
            id_event_id=event_id).select_related('id_user').order_by(
            'id_user__last_name'
        )

    def get_context_data(self, **kwargs):
        """
        Adds an Event instance to the context.

        Args:
            **kwargs: Other keys passed to ListView.

        Returns:
            Template context with keys 'registrations' and 'event'.
        """

        context = super().get_context_data(**kwargs)
        context['event'] = get_object_or_404(Event, id=self.kwargs['event_id'])
        return context


@login_required
def register_for_event(request, event_id):
    """
    Processes the registration of a logged-in user for an event.

    If the user is already registered for the event, it will render the page
    'already_registered.html'. On POST, it will validate the form, save the
    registration and display 'registration_success.html'. Otherwise, it will
    render the form.

    Args:
        request: HTTP request from the client.
        event_id: ID of the event to register for.

    Returns:
        Different template depending on the registration status.
    """

    event = get_object_or_404(Event, pk=event_id)

    if Registration.objects.filter(
            id_user=request.user, id_event=event).exists():
        return render(
            request,
            'already_registered.html',
            {'event': event}
        )
    if request.method == 'POST':
        form = RegistrationForm(request.POST, user=request.user)
        if form.is_valid():
            registration = form.save(commit=False)
            registration.id_user = request.user
            registration.id_event = event
            registration.save()
            return render(
                request,
                'registration_success.html',
                {'event': event}
            )
    else:
        form = RegistrationForm(user=request.user)

    return render(
        request,
        'registration_form.html',
        {'form': form, 'event': event}
    )


def generate_results_template(request, event_id):
    """
    Generates an Excel template for evaluating event results.

    Builds a DataFrame from all registrations for the given event,adds empty
    columns for the resulting times and offers it for download.

    Args:
        request: HTTP request from the client.
        event_id: ID of the event for which the template is being created.

    Returns:
        An Excel file as an attachment named 'Results_event_<event_id>.xlsx'.
    """

    event = get_object_or_404(Event, id=event_id)
    registrations = Registration.objects.filter(
        id_event_id=event.id).select_related('id_user')

    data = []
    for reg in registrations:
        user = reg.id_user
        data.append(
            {
                'id_user_id': user.id,
                'jméno': f"{user.first_name} {user.last_name}",
                'email': user.email,
                'kategorie': reg.category,
                'year': datetime.now().year,
                'id_event_id': event.id,
                'result_time': ''
            }
        )

    df = pd.DataFrame(data)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Results')
    output.seek(0)

    response = HttpResponse(
        output,
        content_type=
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    filename = f"Results_event_{event.id}.xlsx"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response
