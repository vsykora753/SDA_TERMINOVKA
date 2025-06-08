# importy z Djanga
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, UpdateView
from django.views.generic.edit import FormView
from .mixins import OrganizerEventQuerysetMixin
from .forms import OrganizerEventForm 

# formuláře a modely v projektu vytvořené

from .forms import RegisterForm, LoginForm, OrganizerRegisterForm
from events.models import Event

#==============================================================================
#===================== Část pro uživatele - registrace, přihlášení,============
#====================== dashboard a správa událostí organizátora ============== 
#==============================================================================

class UserRegisterView(FormView):
    template_name = 'user/user_register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('user_registration_success')



    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)
    
#============ úspěšná registrace uživatele ============

class UserRegistrationSuccessView(TemplateView):
    template_name = 'user/registration_success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'Registrace byla úspěšná! Nyní se můžete ' \
        'přihlásit jako běžec.'
        return context

#============ uživatel Login a úspěch ============

class UserLoginView(FormView):
    template_name = 'user/user_login.html'
    form_class = LoginForm
    success_url = reverse_lazy('user_dashboard')

    def form_valid(self, form):
        user = form.user  # získání autentizovaného uživatele z formuláře
        login(self.request, user)
        
        if user.role == 'R':
            return HttpResponseRedirect(reverse('user_dashboard'))
        elif user.role == 'O':
            return HttpResponseRedirect(reverse('organizer_dashboard'))
        else:
            return HttpResponseRedirect(reverse('events_list'))     

    
#============ dashboard uživatele ============

@login_required(login_url='/login/')
def user_dashboard(request):
    if request.user.role != 'R':
        return redirect('events_list') 
    return render(request, 'user/user_dashboard.html', {'user': request.user})
    


#============ odhlášení uživatele ============

class UserLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('events_list')  # přesměrování po odhlášení
    
#==============================================================================
#======================Části pro organizátora - registrace, přihlášení,======== 
#======================dashboard a správa událostí organizátora ===============


#============ Organizátor Registrace a Úspěch ============


class OrganizerRegisterView(FormView):
    template_name = 'organizer/organizer_register.html'
    form_class = OrganizerRegisterForm
    success_url = reverse_lazy('organizer_registration_success')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)
    
#============ úspěšná registrace organizátora ============

class OrganizerRegistrationSuccessView(TemplateView):
    template_name = 'organizer/registration_success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'Registrace organizátora byla úspěšná! ' \
'Nyní se můžete přihlásit.'
        return context
    
#============ Organizátor Login ============

class OrganizerLoginView(UserLoginView):
    template_name = 'organizer/organizer_login.html'
    form_class = LoginForm
    success_url = reverse_lazy('organizer_dashboard')

    def form_valid(self, form):
        user = form.user  # získání autentizovaného uživatele z formuláře
        login(self.request, user)
        
        if user.role == 'R':
            return HttpResponseRedirect(reverse('user_dashboard'))
        elif user.role == 'O':
            return HttpResponseRedirect(reverse('organizer_dashboard'))
        else:
            return HttpResponseRedirect(reverse('events_list'))   



# =========== dashboard organizátora ==========

@login_required(login_url='/login/')
def organizer_dashboard(request):
    if request.user.role != 'O':  # pokud uživatel není organizátor, přesměrujeme ho
        return redirect('events_list')  

    events = Event.objects.filter(organizer=request.user)

    return render(request, 'organizer/organizer_dashboard.html', {
        'user': request.user,
        'organizer': request.user,  # pokud šablona používá {{ organizer.company_name }}
        'events': events
    })
#============ Přehled  událostí organizátora ============
class OrganizerEventListView(OrganizerEventQuerysetMixin, ListView):
    model = Event
    template_name = 'organizer/include/organizer_event_list.html'
    context_object_name = 'events'

#============ Editace události organizátora ============

class OrganizerEventEditView(OrganizerEventQuerysetMixin, UpdateView):
    model = Event
    fields = '__all__'
    template_name = 'organizer/create_event.html'
    success_url = reverse_lazy('organizer_dashboard')

#============ Smazání události organizátora ============

class OrganizerEventDeleteView(OrganizerEventQuerysetMixin, View):
    def post(self, request, pk):
        event = Event.objects.get(pk=pk)
        if event.organizer == request.user:
            event.delete()
            return redirect('organizer_event_list')
        else:
            return redirect('organizer_event_list') 

#============ Vytvoření události organizátora ============      

class OrganizerEventCreateView(OrganizerEventQuerysetMixin, FormView):
    """View for creating a new event by the organizer. """
    
    template_name = 'organizer/create_event.html'
    form_class = OrganizerEventForm  # udělat formulář pro událost
    success_url = reverse_lazy('organizer_event_list')

    def form_valid(self, form):
        event = form.save(commit=False)
        event.organizer = self.request.user
        event.save()
        return super().form_valid(form)

    
# ? jak vyřešit aby se stejná akce nevložila 2x ?


