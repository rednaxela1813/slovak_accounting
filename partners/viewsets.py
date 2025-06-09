# partners/views.py
from rest_framework import generics, filters
from rest_framework import viewsets
from .models import Partner, PartnerStatus
from .serializers import PartnerSerializer
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .filters import PartnerFilter


class PartnerListCreateView(generics.ListCreateAPIView):
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = PartnerFilter
    
    
    

    