from django.shortcuts import redirect
from django.views import View
from django.views.generic import ListView, DetailView
from .models import Event,Registration
from datetime import datetime


class EventListView(ListView):
    """
    Representation of a paginated list view for events with customizable query
    filtering.

    The EventListView class extends Django's ListView to provide a paginated
    view of events. It includes functionality for filtering the displayed
    events based on city, region, name, and a date range provided through GET
    parameters. The class also customizes the context data to include a list
    of distinct regions for additional utility in templates.

    Attributes:
        model (Model): The Django model associated with the view, in this
            case, Event.
        template_name (str): The path to the HTML template used to render the
            view.
        context_object_name (str): The context variable name for accessing the
            event list in templates.
        ordering (list[str]): The default field(s) to order the queryset by,
            represented as a list of string field names.
        paginate_by (int): The number of items to display per page in the
            paginated list.
    """

    model = Event
    template_name = 'events_list.html'  
    context_object_name = 'events'
    ordering = ['date_event']
    paginate_by = 6 #zobrazí na stránce 6 událostí

    def get_queryset(self):
        """
        Filters a queryset based on query parameters from a request. The
        method allows filtering by city, region, event name, and an event date
        range. Query parameters are extracted from the request object and
        applied to the queryset if provided.

        Args:
            self: Instance of the class calling the method.

        Returns:
            QuerySet: The filtered queryset based on the provided query
            parameters.

        Raises:
            ValueError: Raised if 'date_from' or 'date_to' query parameters
            are provided but cannot be parsed into a valid date.
        """

        queryset= super().get_queryset()
        city = self.request.GET.get('city')
        region = self.request.GET.get('region')
        name = self.request.GET.get('name_event')
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')
        
        if city:
            queryset=queryset.filter(city__icontains=city)
        if region:
            queryset=queryset.filter(region__icontains=region)
        if name:
            queryset=queryset.filter(name_event__icontains=name)
        if date_from:
            try:
                date_from_parsed = datetime.strptime(
                    date_from,
                    "%Y-%m-%d"
                )
                queryset = queryset.filter(date_event__gte=date_from_parsed)
            except ValueError:
                pass
        if date_to:
            try:
                date_to_parsed = datetime.strptime(date_to, "%Y-%m-%d")
                queryset = queryset.filter(date_event__lte=date_to_parsed)
            except ValueError:
                pass
        return queryset

    def get_context_data(self, **kwargs):
        """
        Retrieves the context data for the view and adds additional
        information related to distinct event regions ordered by the region.
        The function appends this information under the 'regions' key of the
        context dictionary.

        Args:
            **kwargs: Arbitrary keyword arguments passed to the method.

        Returns:
            dict: A context dictionary containing the original context data
            and a list of distinct and ordered event regions under the
            'regions' key.
        """

        context = super().get_context_data(**kwargs)
        context['regions'] = Event.objects.values_list(
            'region',
            flat=True).distinct().order_by('region')
        return context


class TerminovkaView(EventListView):
    """
    Represents a specialized view for handling event lists with a specific
    template.

    This class is intended to display and manage a list of events using a
    predefined HTML template. It inherits from 'EventListView' and customizes
    the behavior by overriding specific attributes.

    Attributes:
        template_name (str): Name of the template file used to render the view.
    """

    template_name = "terminovka.html" 


class EventDetailView(DetailView):
    """
    Handles the detailed view of a specific event.

    This class provides a detailed representation of a single event based on
    the specified model. It defines the template to be used for rendering the
    detailed event view and names the context object for template usage.

    Attributes:
        model (Model): The model that this view will operate on. It represents
            the `Event` model in this case.
        template_name (str): The name of the template used to render this view.
            This is set to 'event_details.html'.
        context_object_name (str): The name of the object to be used in the
            template context. It is defined as 'event'.
    """

    model = Event
    template_name = 'event_details.html'
    context_object_name = 'event'


class EventRegisterView(View):
    """
    Handles event registration requests.

    This class-based view is responsible for processing user registration for
    a specific event. It allows a user to register for an event if the user
    hasn't already registered. Upon successful registration, the user is
    redirected to the event details page.

    Attributes:
        template_name (str): The template used for rendering the view
        (inherited from View, if applicable).
    """

    def post(self, request, pk):
        """
        Handles the POST request to register a user for a specific event.
        If the user is not already registered for the given event, this
        method creates a new registration entry and redirects to the event
        details page.

        Args:
            request: The HTTP request object containing metadata about the
                request, including user's session, method, and any submitted
                data.
            pk: Primary key identifying the specific event to register for.

        Returns:
            HTTPResponse: A redirect response to the event details page for
            the given event.
        """

        event = Event.objects.get(pk=pk)
        if not Registration.objects.filter(
                user=request.user,
                event=event).exists():
            Registration.objects.create(user=request.user, event=event)
        return redirect('event_details', pk=pk)
