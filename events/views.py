from django.shortcuts import redirect
from django.views import View
from django.views.generic import ListView, DetailView
from .models import Event
from registrations.models import Registration
from datetime import datetime,date

# Create your views here.

class EventListView(ListView):
    """
    Displays a paginated list of upcoming races with optional filtering
    by city, region, event name, and date range.
    """
    model = Event
    template_name = 'events_list.html'  
    context_object_name = 'events'
    ordering = ['date_event','start_time']
    paginate_by = 6 #zobrazí na stránce 6 událostí


    def get_queryset(self):
        """
        Returns the filtered queryset of events based on GET parameters.
        If no date range is specified, only future events are shown.
        """
        queryset= super().get_queryset()

        city = self.request.GET.get('city')
        region = self.request.GET.get('region')
        name = self.request.GET.get('name_event')
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')
        
        if not date_from and not date_to:
            queryset=queryset.filter(date_event__gte=date.today()).order_by(
            'date_event', 'start_time')  
            
        if city:
            queryset=queryset.filter(city__icontains=city)
        if region:
            queryset=queryset.filter(region__icontains=region)
        if name:
            queryset=queryset.filter(name_event__icontains=name)
        if date_from:
            try:
                date_from_parsed = datetime.strptime(date_from, "%Y-%m-%d")
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
        Adds a list of available regions to the context
        for use in the filtering form.
        """
        context = super().get_context_data(**kwargs)
        context['regions'] = Event.objects.values_list(
        'region', flat=True
        ).distinct().order_by('region')
        return context

    
class TerminovkaView(EventListView):
    """
    Alternate event list view using the 'terminovka' template layout.
    Inherits all filtering and pagination logic from EventListView.
    """
    template_name = "terminovka.html" 

class EventDetailView(DetailView):
    """
    Displays the details of a specific race (event).
    """
    model = Event
    template_name = 'event_details.html'
    context_object_name = 'event'    


class EventRegisterView(View):
    """
    Handles user registration for a selected race.
    If the user isn't already registered, a new entry is created.
    """
    def post(self, request, pk):
        event = Event.objects.get(pk=pk)
        if not Registration.objects.filter(
            user=request.user, 
            event=event).exists():
            Registration.objects.create(user=request.user, event=event)
        return redirect('event_details', pk=pk)
        