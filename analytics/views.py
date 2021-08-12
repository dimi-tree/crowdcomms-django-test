from datetime import datetime, timedelta

from django.db.models import Sum
from django.utils import timezone

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from analytics.models import UserVisit


class HelloWorld(APIView):
    """
    Basic 'Hello World' view. Show our current API version, the current time, the number of recent visitors
    in the last 1 hour, and the total number of visitors and page visits
    """

    def get(self, request, format=None):
        hour_ago = timezone.now() - timedelta(hours=1)
        data = {
            'version': 1.0,
            'time': timezone.now(),
            'recent_visitors': UserVisit.objects.filter(last_seen__gte=hour_ago).count(),
            'all_visitors': UserVisit.objects.count(),
            'all_visits': UserVisit.objects.all().aggregate(Sum('visits')).get('visits__sum', 0),
        }
        return Response(data)

