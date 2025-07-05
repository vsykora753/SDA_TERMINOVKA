from events.models import Event


class OrganizerEventQuerysetMixin:
    """
    A mixin for class-based views that limits the queryset of Events to those
    belonging to the currently logged in organizer.

    If the user is not logged in or does not have the 'O' role, it returns an empty queryset.
    """

    def get_queryset(self):
        """
        Returns:
            A list of events managed by the current user, or an empty queryset
            if the user is not authorized as an organizer.
        """

        user = self.request.user
        if not user.is_authenticated or user.role != 'O':
            return Event.objects.none()
        return Event.objects.filter(organizer=user)
