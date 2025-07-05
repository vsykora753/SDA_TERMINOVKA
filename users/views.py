from datetime import date, datetime

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, UpdateView
from django.views.generic.edit import FormView
from django.core.paginator import Paginator

from .mixins import OrganizerEventQuerysetMixin
from .forms import (
    LoginForm,
    OrganizerEventForm,
    OrganizerRegisterForm,
    RegisterForm,
)
from events.models import Event
from registrations.models import Registration


def my_homepage_view(request):
    """
    Redirects the authenticated user to the appropriate dashboard or to the
    event list if not logged in.

    Args:
        request: HTTP request from the client.

    Returns:
        HttpResponseRedirect: Redirect to one of the URLs:

        - 'organizer_dashboard' for organizers (role='O')
        - 'user_dashboard' for runners (role='R')
        - 'events_list' for anonymous users
    """

    if request.user.is_authenticated:
        if request.user.role == 'O':
            return redirect('organizer_dashboard')
        elif request.user.role == 'R':
            return redirect('user_dashboard')
    return redirect('events_list')


class UserRegisterView(FormView):
    """
    Processes the registration of a new user (role 'R').

    Attributes:
        template_name: Path to the template with the registration form.
        form_class: Class of the RegisterForm form.
        success_url: URL after successful registration.
    """

    template_name = 'user/user_register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('user_registration_success')

    def form_valid(self, form):
        """
        Saves a new user and logs them in.

        Args:
            form: Valid form data.

        Returns:
            Standard FormView redirect.
        """

        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

    def form_invalid(self, form):
        """
        Returns a form with error messages back to the client.

        Args:
            form: Form with invalid data.

        Returns:
            Response with the form and errors.
        """

        return super().form_invalid(form)


class UserRegistrationSuccessView(TemplateView):
    """
    Displays a page confirming successful runner registration.
    """

    template_name = 'user/registration_success.html'

    def get_context_data(self, **kwargs):
        """
        Adds a message to the context about successful registration.

        Returns:
            Template context with key 'message' (dict).
        """

        context = super().get_context_data(**kwargs)
        context['message'] = \
            'Registrace byla úspěšná! Nyní se můžete přihlásit jako běžec.'
        return context


class RoleBasedLoginView(FormView):
    """
    Processes user login and redirects based on a role.

    Attributes:
        template_name: Path to the login form template.
        form_class: LoginForm class.
    """

    template_name = 'user/user_login.html'
    form_class = LoginForm

    def form_valid(self, form):
        """
        Logs in the user and redirects to the dashboard according to their
        role.

        Args:
            form: Form with valid login details.

        Returns:
            - 'user_dashboard' for runners
            - 'organizer_dashboard' for organizers
            - 'events_list' for unknown roles
        """

        user = form.user
        login(self.request, user)

        if user.role == 'R':
            return HttpResponseRedirect(reverse('user_dashboard'))
        elif user.role == 'O':
            return HttpResponseRedirect(reverse('organizer_dashboard'))
        else:
            return HttpResponseRedirect(reverse('events_list'))


@login_required(login_url='/login/')
def user_dashboard(request):
    """
    Displays the runner's dashboard with their registrations and allows
    filtering by region, name and date.

    Args:
        request: HTTP request with GET parameters region, name_event,
        date_from, date_to, page.

    Returns:
        Rendered HTML template 'user/user_dashboard.html' with context
        page_obj: paginated list of Registration and list of available regions.
    """

    if request.user.role != 'R':
        return redirect('events_list')
    registrations = Registration.objects.filter(
        id_user=request.user).select_related('id_event').order_by(
        'id_event__date_event', 'id_event__start_time')

    event_ids = registrations.values_list('id_event_id', flat=True)
    events = Event.objects.filter(id__in=event_ids)

    region = request.GET.get('region')
    name = request.GET.get('name_event')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')

    if region:
        events = events.filter(region__icontains=region)
    if name:
        events = events.filter(name_event__icontains=name)
    if date_from:
        try:
            parsed_date_from = datetime.strptime(
                date_from,
                "%Y-%m-%d"
            )
            events = events.filter(date_event__gte=parsed_date_from)
        except ValueError:
            pass
    if date_to:
        try:
            parsed_date_to = datetime.strptime(date_to, "%Y-%m-%d")
            events = events.filter(date_event__lte=parsed_date_to)
        except ValueError:
            pass

    regions = events.values_list(
        'region', flat=True).distinct().order_by('region')

    registrations = registrations.filter(
        id_event__in=events).order_by(
        'id_event__date_event', 'id_event__start_time')

    paginator = Paginator(registrations, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "user/user_dashboard.html",
        {
            "page_obj": page_obj,
            "regions": regions,
        }
    )


@login_required(login_url='/login/')
def unregister_from_event(request, event_id):
    """
    Unregisters a runner from a specific event and redirects back.

    Args:
        request: HTTP request from the organizer.
        event_id: Primary key of the Event to unregister from.

    Returns:
        Redirect to 'user_dashboard'.

    Raises:
        Http404: If registration does not exist.
    """

    if request.user.role != 'R':
        return redirect('events_list')

    registrations = get_object_or_404(
        Registration,
        id_event=event_id,
        id_user=request.user
    )
    registrations.delete()

    return redirect('user_dashboard')


class UserEventListView(OrganizerEventQuerysetMixin, ListView):
    """
    Displays a list of upcoming events available to the runner.

    Attributes:
        model: Event
        template_name: Template to be inserted into the runner's dashboard.
        context_object_name: Name in context ('events').
        paginate_by: Number of events per page.
    """

    model = Event
    template_name = 'user/include/user_event_list.html'
    context_object_name = 'events'
    ordering = ['-date_event', '-start_time']
    paginate_by = 6

    def get_queryset(self):
        """
        Returns:
            A queryset of events from today's date in ascending order.
        """

        queryset = super().get_queryset()
        return queryset.filter(
            date_event__gte=date.today()).order_by(
            'date_event', 'start_time')


class UserLogoutView(View):
    """
    Logs out the user and redirects to the event list.
    """

    def get(self, request, *args, **kwargs):
        """
        Processes a GET request for logout.

        Returns:
            Redirect to 'events_list'.
        """

        logout(request)
        return redirect('events_list')


class OrganizerRegisterView(FormView):
    """
    Processes the registration of a new organizer (role 'O').

    Attributes:
        template_name: Organizer registration form template.
        form_class: OrganizerRegisterForm class.
        success_url: URL after successful registration.
    """

    template_name = 'organizer/organizer_register.html'
    form_class = OrganizerRegisterForm
    success_url = reverse_lazy('organizer_registration_success')

    def form_valid(self, form):
        """
        Saves the organizer and logs them in.

        Returns:
            Redirect according to FormView logic.
        """

        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class OrganizerRegistrationSuccessView(TemplateView):
    """
    Displays confirmation of successful organizer registration.
    """

    template_name = 'organizer/registration_success.html'

    def get_context_data(self, **kwargs):
        """
        Adds a message to the context about successful registration.

        Returns:
            Context with key 'message'.
        """

        context = super().get_context_data(**kwargs)
        context['message'] = ('Registrace organizátora byla úspěšná! '
                              'Nyní se můžete přihlásit.')
        return context


@login_required(login_url='/login/')
def organizer_dashboard(request):
    """
    Displays the organizer dashboard, allowing them to track and filter their
    own events.

    Args:
        request: HTTP request with GET parameters for filtering.

    Returns:
        Template 'organizer/organizer_dashboard.html' with page_obj and
        regions context.
    """

    if request.user.role != 'O':
        return redirect('no_access')  # nebo 403

    events = Event.objects.filter(
        organizer=request.user).order_by(
        'date_event', 'start_time'
    )
    region = request.GET.get('region')
    name = request.GET.get('name_event')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')

    if region:
        events = events.filter(region__icontains=region)
    if name:
        events = events.filter(name_event__icontains=name)
    if date_from:
        try:
            parsed_date_from = datetime.strptime(date_from, "%Y-%m-%d")
            events = events.filter(date_event__gte=parsed_date_from)
        except ValueError:
            pass
    if date_to:
        try:
            parsed_date_to = datetime.strptime(date_to, "%Y-%m-%d")
            events = events.filter(date_event__lte=parsed_date_to)
        except ValueError:
            pass

    paginator = Paginator(events, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    regions = Event.objects.values_list(
        'region', flat=True).distinct().order_by('region')

    return render(
        request,
        "organizer/organizer_dashboard.html",
        {
            "page_obj": page_obj,
            "regions": regions,
        }
    )


class OrganizerEventListView(OrganizerEventQuerysetMixin, ListView):
    """
    Displays the organizer's events with pagination.

    Attributes:
        model: Event
        template_name: Organizer's event list template.
        context_object_name: 'events'
        paginate_by: Number of items per page.
    """

    model = Event
    template_name = 'organizer/include/organizer_event_list.html'
    context_object_name = 'events'
    ordering = ['-date_event', '-start_time']
    paginate_by = 6


class OrganizerEventEditView(OrganizerEventQuerysetMixin, UpdateView):
    """
    Allows the organizer to edit an existing event.

    Attributes:
        model: Event
        fields: Model fields to edit ('__all__').
        template_name: Template for editing the event.
        success_url: URL after saving changes.
    """

    model = Event
    fields = '__all__'
    template_name = 'organizer/create_event.html'
    success_url = reverse_lazy('organizer_dashboard')


class OrganizerEventDeleteView(OrganizerEventQuerysetMixin, View):
    """
    Confirms and deletes the selected event by the organizer.
    """

    template_name = 'organizer/event_confirm_delete.html'

    def get(self, request, pk):
        """
        Displays a confirmation page before deleting.

        Args:
            pk: The event ID to delete.

        Returns:
            A template with the event details.
        """

        event = get_object_or_404(self.get_queryset(), pk=pk)
        return render(request, self.template_name, {'event': event})

    def post(self, request, pk):
        """
        Deletes the event and displays a success message.

        Args:
            pk: The ID of the event to delete.

        Returns:
            Redirect to 'organizer_dashboard'.
        """

        event = get_object_or_404(self.get_queryset(), pk=pk)
        event.delete()
        messages.success(request, 'Událost byla smazána')
        return redirect('organizer_dashboard')


class OrganizerEventCreateView(OrganizerEventQuerysetMixin, FormView):
    """
    Handles the creation of a new event by the organizer.

    Attributes:
        template_name: Event creation form template.
        form_class: OrganizerEventForm class.
        success_url: URL after the event is successfully saved.
    """

    template_name = 'organizer/create_event.html'
    form_class = OrganizerEventForm  # udělat formulář pro událost
    success_url = reverse_lazy('organizer_dashboard')

    def form_valid(self, form):
        """
        With valid data, it assigns an organizer, saves the event, and
        redirects.

        Args:
            form: Valid event form.

        Returns:
            Standard FormView redirect.
        """

        event = form.save(commit=False)
        event.organizer = self.request.user
        event.save()
        print("Událost byla úspěšně vytvořena:", event)

        return super().form_valid(form)
