from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from .forms import RegisterForm,LoginForm, OrganizerRegisterForm
from django.contrib.auth import  login, logout
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views import View
from django.urls import reverse
from django.http import HttpResponseRedirect


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
        context['message'] = 'Registrace byla úspěšná! Nyní se můžete přihlásit jako běžec.'
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
        context['message'] = 'Registrace organizátora byla úspěšná! Nyní se můžete přihlásit.'
        return context
    
#============ Organizátor Login ============

class OrganizerLoginView(UserLoginView):
    template_name = 'organizer/organizer_login.html'
        
# =========== dashboard organizátora ==========

@login_required(login_url='/login/')
def organizer_dashboard(request):
    if request.user.role != 'O':  # pokud uživatel není organizátor, přesměrujeme ho
        return redirect('events_list')  
    return render(request, 'organizer/organizer_dashboard.html', {'user': request.user})


