# partners/views.py
from rest_framework import generics, filters
from rest_framework import viewsets
from .models import Partner, PartnerStatus
from .serializers import PartnerSerializer
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .filters import PartnerFilter
from rest_framework.response import Response
from rest_framework import status



class PartnerListCreateView(generics.ListCreateAPIView):
    
    def get_queryset(self):
        return Partner.objects.filter(partner_status=PartnerStatus.ACTIVE)

    serializer_class = PartnerSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = PartnerFilter
    
    
    

class PartnerRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'partner_id'
    
    def destroy(self, request, *args, **kwargs):
        partner = self.get_object()
        partner.partner_status = PartnerStatus.INACTIVE
        partner.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    