from registrations.models import Registration
from events.models import Event


def user_events(request):
    """
    Context processor: returns a list of events that the logged in runner is
    registered for.

    Checks if the user is logged in and has the role 'R'. If so, retrieves all
    registrations for this user and returns their Event instances.

    Args:
        request: The original HTTP request.

    Returns:
        The 'user_registered_events' key contains a list of Event objects that
        the user is registered for. If the condition is not met,it returns an
        empty list.
    """

    if (request.user.is_authenticated and hasattr(request.user, 'role') and
            request.user.role == 'R'):
        registrations = (Registration.objects.filter(id_user=request.user)
                         .select_related('id_event'))
        user_events = [r.id_event for r in registrations]
    else:
        user_events = []
    return {'user_registered_events': user_events}


def organizer_events(request):
    """
    Context processor: returns a list of events managed by the logged in
    organizer.

    Checks if the user is logged in and has the 'O' role. If so, returns a
    QuerySet of all Event objects where the organizer is request.user, sorted
    by event date in descending order.

    Args:
        request: The original HTTP request.

    Returns:
        The 'organizer_events' key contains the QuerySet of Events for the
        given organizer, or None if the condition is not met.
    """

    if (request.user.is_authenticated and hasattr(request.user, 'role') and
            request.user.role == 'O'):
        return {
            'organizer_events': Event.objects.filter(organizer=request.user)
            .order_by('-date_event')
        }
    return {'organizer_events': None}
