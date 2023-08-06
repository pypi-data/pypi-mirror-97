from django.contrib.auth.models import User, Group
from django.views.generic import View, ListView, DetailView
from tables.models import Table, Leg, Foot
from rest_framework import generics
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import UserSerializer, GroupSerializer, TableSerializer, LegSerializer, FootSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class TablesViewAllApi(generics.ListAPIView):
    queryset = Table.objects.all()
    serializer_class = TableSerializer

class TableViewByIdApi(generics.RetrieveUpdateDestroyAPIView):
    queryset = Table.objects.all()
    serializer_class = TableSerializer

class TableCreateApi(generics.CreateAPIView):
    queryset = Table.objects.all()
    serializer_class = TableSerializer

class TableUpdateApi(generics.RetrieveUpdateAPIView):
    queryset = Table.objects.all()
    serializer_class = TableSerializer

class TableDeleteApi(generics.DestroyAPIView):
    queryset = Table.objects.all()
    serializer_class = TableSerializer


class LegsViewAllApi(generics.ListAPIView):
    queryset = Leg.objects.all()
    serializer_class = LegSerializer

class LegViewByIdApi(generics.RetrieveUpdateDestroyAPIView):
    queryset = Leg.objects.all()
    serializer_class = LegSerializer

class LegCreateApi(generics.CreateAPIView):
    queryset = Leg.objects.all()
    serializer_class = LegSerializer

class LegUpdateApi(generics.RetrieveUpdateAPIView):
    queryset = Leg.objects.all()
    serializer_class = LegSerializer

class LegDeleteApi(generics.DestroyAPIView):
    queryset = Leg.objects.all()
    serializer_class = LegSerializer


class FeetViewAllApi(generics.ListAPIView):
    queryset = Foot.objects.all()
    serializer_class = FootSerializer

class FootViewByIdApi(generics.RetrieveUpdateDestroyAPIView):
    queryset = Foot.objects.all()
    serializer_class = FootSerializer

class FootCreateApi(generics.CreateAPIView):
    queryset = Foot.objects.all()
    serializer_class = FootSerializer

class FootUpdateApi(generics.RetrieveUpdateAPIView):
    queryset = Foot.objects.all()
    serializer_class = FootSerializer

class FootDeleteApi(generics.DestroyAPIView):
    queryset = Foot.objects.all()
    serializer_class = FootSerializer