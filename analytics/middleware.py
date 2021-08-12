from django.db.models import F
from django.utils import timezone

from analytics.models import UserVisit


class UserVisitMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        if not user.is_anonymous:
            user, created = UserVisit.objects.get_or_create(user=user, visits=1)

            if not created:
                user.last_seen = timezone.now()
                user.visits = F('visits') + 1
                user.save()

        response = self.get_response(request)
        return response
