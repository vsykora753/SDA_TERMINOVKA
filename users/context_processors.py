
from registrations.models import Registration
from events.models import Event

# Pro přihlášeného uživatele (běžce)
def user_events(request):
    if request.user.is_authenticated and hasattr(request.user, 'role') and request.user.role == 'R':
        registrations = Registration.objects.filter(id_user=request.user).select_related('id_event')
        user_events = [r.id_event for r in registrations]
    else:
        user_events = []
    return {'user_registered_events': user_events}

# Pro přihlášeného organizátora
def organizer_events(request):
    if request.user.is_authenticated and hasattr(request.user, 'role') and request.user.role == 'O':
        return {
            'organizer_events': Event.objects.filter(organizer=request.user).order_by('-date_event')
        }
    return {'organizer_events': None}