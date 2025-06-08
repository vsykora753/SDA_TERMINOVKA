
from events.models import Event

# Zdefinujeme funkce, které budou použity v rámci aplikace (organizátor)

class OrganizerEventQuerysetMixin:
    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated or user.role != 'O':
            return Event.objects.none()
        return Event.objects.filter(organizer=user)
    