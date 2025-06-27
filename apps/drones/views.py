from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.throttling import ScopedRateThrottle

from .custompermission import IsCurrentUserOwnerOrReadOnly
from .filters import CompetitionsFilter
from .models import Competition
from .models import Drone
from .models import DroneCategory
from .models import Pilot
from .serializers import DroneCategorySerializer
from .serializers import DroneSerializer
from .serializers import PilotCompetitionSerializer
from .serializers import PilotSerializer

SEARCH_FIELDS = '^name'


class DroneCategoryList(generics.ListCreateAPIView):
    queryset = DroneCategory.objects.all()
    serializer_class = DroneCategorySerializer
    name = "dronecategory-list"
    filterset_fields = ('name',)
    # filter_fields - Устарело
    search_fields = (SEARCH_FIELDS,)
    # ^ - поиск по началу, не точное совпадение
    ordering_fields = ('name',)


class DroneCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DroneCategory.objects.all()
    serializer_class = DroneCategorySerializer
    name = "dronecategory-detail"


class DroneList(generics.ListCreateAPIView):
    throttle_scope = 'drones'
    throttle_classes = (ScopedRateThrottle,)
    queryset = Drone.objects.all()
    serializer_class = DroneSerializer
    name = "drone-list"
    filterset_fields = (
        'name',
        'drone_category',
        'manufacturing_date',
        'has_it_competed',
    )
    search_fields = (
        SEARCH_FIELDS,
    )
    ordering_fields = (
        'name',
        'manufacturing_date',
    )
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsCurrentUserOwnerOrReadOnly,
    )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class DroneDetail(generics.RetrieveUpdateDestroyAPIView):
    throttle_scope = 'drones'
    throttle_classes = (ScopedRateThrottle,)
    queryset = Drone.objects.all()
    serializer_class = DroneSerializer
    name = "drone-detail"
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsCurrentUserOwnerOrReadOnly,
    )


class PilotList(generics.ListCreateAPIView):
    throttle_scope = 'pilots'
    throttle_classes = (ScopedRateThrottle,)
    queryset = Pilot.objects.all()
    serializer_class = PilotSerializer
    name = "pilot-list"
    filterset_fields = (
        'name',
        'gender',
        'races_count',
    )
    search_fields = (
        SEARCH_FIELDS,
    )
    ordering_fields = (
        'name',
        'races_count',
    )
    authentication_classes = (
        TokenAuthentication,
    )
    permission_classes = (
        IsAuthenticated,
    )


class PilotDetail(generics.RetrieveUpdateDestroyAPIView):
    throttle_scope = 'pilots'
    throttle_classes = (ScopedRateThrottle,)
    queryset = Pilot.objects.all()
    serializer_class = PilotSerializer
    name = "pilot-detail"
    authentication_classes = (
        TokenAuthentication,
    )
    permission_classes = (
        IsAuthenticated,
    )


class CompetitionList(generics.ListCreateAPIView):
    queryset = Competition.objects.all()
    serializer_class = PilotCompetitionSerializer
    name = "competition-list"
    filterset_class = CompetitionsFilter
    ordering_fields = (
        'distance_in_feet',
        'distance_achievement_date',
    )


class CompetitionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Competition.objects.all()
    serializer_class = PilotCompetitionSerializer
    name = "competition-detail"


class ApiRoot(generics.GenericAPIView):
    name = "api-root"

    def get(self, request, *args, **kwargs):
        return Response({
            'drone-categories': reverse(DroneCategoryList.name, request=request),
            'drones': reverse(DroneList.name, request=request),
            'pilots': reverse(PilotList.name, request=request),
            'competitions': reverse(CompetitionList.name, request=request),
        })
