from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from .forms import RegisterForm, LoginForm, OrganizerRegisterForm


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
                defined by the parent class.
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
            dict: A dictionary containing the combined context data, including
                the custom success message.
        """

        context = super().get_context_data(**kwargs)
        context['message'] = \
            'Registrace byla úspěšná! Nyní se můžete přihlásit jako běžec.'
        return context


class UserLoginView(FormView):
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
    success_url = reverse_lazy('user_dashboard')

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
            - Redirects to 'events_list' for users with any other role.
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
        """
        Handles user logout and redirects them to the events list page.

        This method is responsible for ending a user session by invoking the
        logout function. After successfully logging out the user, it redirects
        them to the 'events_list' page, providing a clean user experience and
        ensuring proper session management.

        Args:
            request: The HTTP request object containing metadata about the
                current request.
            *args: Additional positional arguments passed to the method.
            **kwargs: Additional keyword arguments passed to the method.

        Returns:
            HttpResponse: A redirect response that navigates the user to the
                'events_list' page after logout.
        """

        logout(request)
        return redirect('events_list')  # přesměrování po odhlášení


class OrganizerRegisterView(FormView):
    """
    Handles the registration process for organizers.

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
    """View for displaying a success message after an organizer's registration.

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


class OrganizerLoginView(UserLoginView):
    """
    Handles the login view for organized users.

    This class provides a custom login view specifically tailored for
    organized users, inheriting from a generic user login view. It applies a
    specific template for the login functionality of organizers.

    Attributes:
        template_name (str): Path to the HTML template used to render the
            login page for organizers.
    """

    template_name = 'organizer/organizer_login.html'


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
        return redirect('events_list')  
    return render(
        request,
        'organizer/organizer_dashboard.html',
        {'user': request.user}
    )


