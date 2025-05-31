from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from .forms import RegisterForm,LoginForm
from .models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin


class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = reverse_lazy('login_success')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(self.request, email=email, password=password)
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            form.add_error(None, 'Neplatné přihlašovací údaje')
            return self.form_invalid(form)

class PersonalView(LoginRequiredMixin, TemplateView):
    template_name = 'personal.html'
    login_url = '/login/'  # URL, kam bude uživatel přesměrován, pokud není přihlášen
    success_url = reverse_lazy('login_success')

class RegisterView(FormView):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('registration_success')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)  # automaticky přihlásí uživatele
        return super().form_valid(form)
