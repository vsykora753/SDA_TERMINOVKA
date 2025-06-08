from django.views.generic import ListView, DetailView
from .models import Event
from datetime import datetime

# Create your views here.

class EventListView(ListView):
    model = Event
    template_name = 'events_list.html'  
    context_object_name = 'events'
    ordering = ['date_event']
    paginate_by = 6 #zobrazí na stránce 6 událostí


    def get_queryset(self):
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
        context = super().get_context_data(**kwargs)
        context['regions'] = Event.objects.values_list(
        'region', flat=True
        ).distinct().order_by('region')
        return context

    
class TerminovkaView(EventListView):
    template_name = "terminovka.html" 

class EventDetailView(DetailView):
    model = Event
    template_name = 'event_details.html'
    context_object_name = 'event'    