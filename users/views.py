# importy z Djanga
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, UpdateView
from django.views.generic.edit import FormView
from django.core.paginator import Paginator
from .mixins import OrganizerEventQuerysetMixin
from .forms import OrganizerEventForm 

# formuláře a modely v projektu vytvořené

from .forms import RegisterForm, LoginForm, OrganizerRegisterForm
from events.models import Event



class UserRegisterView(FormView):
    """
    Handles the user registration process.

    This view provides functionality for users to register an account using a
    form. Upon successful registration, the user is logged in automatically,
    and they are redirected to a success page.

    Attributes:
        template_name (str): Path to the HTML template used for rendering the
            user registration form.
        form_class (type): The form class used for user registration.
        success_url (str): The URL to which the user is redirected upon
            successful registration.
    """
    template_name = 'user/user_register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('user_registration_success')



    def form_valid(self, form):
        """
        Handles the logic required when a submitted form is valid. Saves the
        user, logs them in using the provided form details, and then redirects
        to a success URL.

        Args:
            form: The submitted and validated form instance containing user
                information.

        Returns:
            HttpResponseRedirect: A redirect response to the success URL
                defined by the parent class.Add commentMore actions
        """
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

    def form_invalid(self, form):
        """
        Handles the invalid form submission within a view by extending the
        behavior of the parent class.

        This method is called when the submitted form fails validation. It
        ensures that the functionality defined in the parent class is
        preserved for handling an invalid form scenario.

        Args:
            form: The form instance that failed validation and triggered this
            method.

        Returns:
            HttpResponse: The HTTP response returned by the parent class's
            form_invalid implementation.
        """
        return super().form_invalid(form)
    


class UserRegistrationSuccessView(TemplateView):
    """
    Handles the view for the user registration success page.

    This class-based view renders the template for the user registration
    success page and provides a context that includes a user-friendly message
    notifying the user about the successful registration. The view can be
    subclassed or customized further if needed.

    Attributes:
        template_name (str): The path to the template file used for the
            registration success page.
    """

    template_name = 'user/registration_success.html'

    def get_context_data(self, **kwargs):
        """
        Retrieves the context data for the view and adds a custom success
        message.

        This method extends the context data provided by the superclass and
        injects a custom message. The added message is intended to notify
        users of a successful registration and provide further instructions
        regarding the next steps.

        Args:
            **kwargs: Arbitrary keyword arguments passed to the method. These
                are typically used to customize the context data.

        Returns:
            dict: A dictionary containing the combined context data, includingAdd commentMore actions
                the custom success message.
        """
        context = super().get_context_data(**kwargs)
        context['message'] = \
            'Registrace byla úspěšná! Nyní se můžete přihlásit jako běžec.'
        return context



class RoleBasedLoginView(FormView):
    """
    Handles user login functionality.

    This class-based view is responsible for rendering the login form,
    processing the login request, and redirecting to the appropriate dashboard
    or page based on the user's role. It extends the FormView, using the
    LoginForm to authenticate users.

    Attributes:
        template_name (str): The template used to render the login page.
        form_class (type): The form class used for login functionality.
        success_url (str): The URL to which the user is redirected upon
            successful login.
    """
    template_name = 'user/user_login.html'
    form_class = LoginForm


    def form_valid(self, form):
        """
        Handles the form validation process and manages user redirection based
        on their role after successful login.

        This method validates the provided form, logs in the user, and
        redirects them to the appropriate dashboard or endpoint according to
        their specified role.

        Args:
            form: The form instance containing the user authentication and
            role data.

        Returns:
            HttpResponseRedirect: Redirects the user to an appropriate URL
            based on their role:

            - Redirects to 'user_dashboard' for users with role 'R'.
            - Redirects to 'organizer_dashboard' for users with role 'O'.
            - Redirects to 'events_list' for users with any other role.Add commentMore actions
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
    Renders the user dashboard page for users with a specific role. If the
    user does not have the required role, they are redirected to the events
    list page.

    Args:
        request: The HTTP request object containing metadata about the request.

    Returns:
        HttpResponse: The HTTP response object with the rendered dashboard
        page for authorized users, or a redirect to the events list for others.
    """

    if request.user.role != 'R':
        return redirect('events_list') 
    return render(
        request,
        'user/user_dashboard.html',
        {'user': request.user}
    )
    



class UserLogoutView(View):
    """
    Handles user logout functionality.

    This class defines the behavior for logging out a user from the system and
    redirecting them to a specified page afterward. It extends from the base
    View class and provides a specific implementation for the GET HTTP method.

    """
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('events_list')  # přesměrování po odhlášení
    



class OrganizerRegisterView(FormView):
    """
    Handles the registration process for organizers.Add commentMore actions

    This class represents a view that provides the registration functionality
    for organizers. It renders a registration form, processes form
    submissions, and logs in the newly registered user upon successful
    registration. This view inherits from Django's FormView, leveraging its
    built-in mechanics for form handling and redirection.

    Attributes:
        template_name (str): The template used to render the registration form.
        form_class (type): The form class used to handle organizer
            registration.
        success_url (str): The URL to redirect to upon successful form
            submission.
    """
    template_name = 'organizer/organizer_register.html'
    form_class = OrganizerRegisterForm
    success_url = reverse_lazy('organizer_registration_success')

    def form_valid(self, form):
        """
        Handles the validation and login process when a form submission is
        successful.

        The method saves the form, logs in the newly created user, and then
        proceeds with the default behavior of the parent class's form_valid
        method.

        Args:
            form: A valid form instance that has passed all validations.

        Returns:
            HttpResponse: The HTTP response indicating form submission was
            successful.
        """
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)
    


class OrganizerRegistrationSuccessView(TemplateView):
    """
    View for displaying a success message after an organizer's registration.

    This class-based view is intended to provide feedback to users upon the
    successful registration of an organizer. It renders a specific template
    with a context that includes a success message.

    Attributes:
        template_name (str): Path to the template used for rendering the view.
    """
    template_name = 'organizer/registration_success.html'

    def get_context_data(self, **kwargs):
        """
        Retrieves the context data for a template, enhancing it with
        additional information specific to the view.

        This method extends the default context data with a custom message
        that indicates successful registration of the organizer.

        Args:
            **kwargs: Arbitrary keyword arguments passed to the view to help
                in generating the context data.

        Returns:
            dict: A dictionary containing the context data, including a
            custom message for successful registration.
        """
        context = super().get_context_data(**kwargs)
        context['message'] = ('Registrace organizátora byla úspěšná! '
                            'Nyní se můžete přihlásit.')
        return context
    




@login_required(login_url='/login/')
def organizer_dashboard(request):
    """
    Renders the organizer dashboard view if the requesting user has the role
    of an organizer ('O'). If the user is not an organizer, they are
    redirected to the events list page instead.

    Args:
        request: The HTTP request object containing metadata about the request.

    Returns:
        HttpResponse: Rendered HTML response for the organizer dashboard if
        the user is an organizer or a redirect response to the events list
        page otherwise.
    """
    if request.user.role != 'O':
        return redirect('no_access')  # nebo 403

    events = Event.objects.filter(organizer=request.user).order_by('-date_event')
    paginator = Paginator(events, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "organizer/dashboard_organizer.html", {
        "page_obj": page_obj,
    })


class OrganizerEventListView(OrganizerEventQuerysetMixin, ListView):
    """
    Displays a list of events organized by the logged-in user.
    This view inherits from OrganizerEventQuerysetMixin to filter events
    based on the organizer (the logged-in user). It uses Django's ListView
    to handle the display of events in a paginated format.
    Attributes:
        model (Model): The model class for the events to be listed.
        template_name (str): The template used to render the event list.
        context_object_name (str): The name of the context variable that
            contains the list of events.
        ordering (list): The order in which events are displayed, sorted by
            start date.
        paginate_by (int): The number of events to display per page.
    """
    model = Event
    template_name = 'organizer/include/organizer_event_list.html'
    context_object_name = 'events'
    ordering = ['start_date']  
    paginate_by = 6
    



class OrganizerEventEditView(OrganizerEventQuerysetMixin, UpdateView):
    """
    View for editing an existing event by the organizer.
    This class-based view allows the organizer to modify the details of an
    existing event. It inherits from OrganizerEventQuerysetMixin to ensure
    that only events created by the logged-in organizer are accessible for
    editing. The view uses Django's UpdateView to handle the form submission
    and validation process.
    Attributes:
        
        model (Model): The model class for the event being edited.
        fields (list): The fields of the event model that can be edited.
        template_name (str): The template used to render the event edit form.
        success_url (str): The URL to redirect to upon successful form
    """
    model = Event
    fields = '__all__'
    template_name = 'organizer/create_event.html'
    success_url = reverse_lazy('organizer_dashboard')


class OrganizerEventDeleteView(OrganizerEventQuerysetMixin, View):
    """
    View for deleting an event created by the organizer.
    This class-based view handles the deletion of an event that was created
    by the organizer. It ensures that only the organizer who created the event
    can delete it. The view uses Django's generic View class to implement the
    deletion logic.
    Attributes:
        model (Model): The model class for the event being deleted.
        template_name (str): The template used to confirm the deletion.
    """
    def post(self, request, pk):
        """
        Handles the POST request to delete an event.
        This method retrieves the event by its primary key (pk) and checks if
        the event exists and belongs to the logged-in organizer. If the event
        is found, it is deleted, and the user is redirected to the event list
        page. If the event does not exist or does not belong to the organizer,
        a 404 error is raised.
        Args:
            request: The HTTP request object containing metadata about the
                request.
            pk (int): The primary key of the event to be deleted.
        Returns:
            HttpResponseRedirect: Redirects to the organizer event list page
            after successful deletion of the event.
        """
        event = Event.objects.get(pk=pk)
        event = get_object_or_404(Event, pk=pk, organizer=request.user)
        event.delete()
        return redirect('organizer_event_list')

#============ Vytvoření události organizátora ============      

class OrganizerEventCreateView(OrganizerEventQuerysetMixin, FormView):
    """
    View for creating a new event by the organizer. 
    This class-based view allows the organizer to create a new event using a
    form. It inherits from OrganizerEventQuerysetMixin to ensure that only
    events created by the logged-in organizer are accessible. The view uses
    Django's FormView to handle the form submission and validation process.
    Attributes:
        template_name (str): The template used to render the event creation
            form.
        form_class (type): The form class used for creating the event.
        success_url (str): The URL to redirect to upon successful form
            submission.
    """
    
    template_name = 'organizer/create_event.html'
    form_class = OrganizerEventForm  # udělat formulář pro událost
    success_url = reverse_lazy('organizer_event_list')

    def form_valid(self, form):
        """
        Handles the logic when a submitted form is valid. Saves the event  
        instance, associates it with the logged-in organizer.
        
        """
        event = form.save(commit=False)
        event.organizer = self.request.user
        event.save()
        return super().form_valid(form)
    



