from rest_framework import viewsets

# Create your views here.
from rest_framework.permissions import IsAuthenticated

from bunnies.models import Bunny, RabbitHole
from bunnies.permissions import RabbitHolePermissions
from bunnies.serializers import BunnySerializer, RabbitHoleSerializer


class RabbitHoleViewSet(viewsets.ModelViewSet):
    serializer_class = RabbitHoleSerializer
    permission_classes = (IsAuthenticated, RabbitHolePermissions)
    queryset = RabbitHole.objects.all()

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def filter_queryset(self, queryset):
        hole_id = self.kwargs.get('pk')
        if hole_id:
            queryset = queryset.filter(pk=hole_id)

        user = self.request.user
        if user.is_superuser:
            return queryset
        else:
            return queryset.filter(owner=user)


class BunnyViewSet(viewsets.ModelViewSet):
    serializer_class = BunnySerializer
    permission_classes = (IsAuthenticated,)
    queryset = Bunny.objects.all()
