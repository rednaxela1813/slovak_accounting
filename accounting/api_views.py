from rest_framework.views import APIView
from rest_framework.response import Response
from accounting.models import Account, JournalEntry
from accounting.serializers import AccountSerializer, JournalEntrySerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import filters
from accounting.filters import JournalEntryFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated





class AccountListAPIView(APIView):
    """
    API view to list all accounts.
    """
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated
    
    def get(self, request):
        accounts = Account.objects.all()
        serializer = AccountSerializer(accounts, many=True)
        return Response(serializer.data)
    
    

# class JournalEntryListCreateAPIView(ListCreateAPIView):
#     queryset = JournalEntry.objects.all()
#     serializer_class = JournalEntrySerializer

    

class JournalEntryListCreateAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated
    queryset = JournalEntry.objects.all().order_by('id')
    serializer_class = JournalEntrySerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = JournalEntryFilter
    ordering_fields = ['date', 'amount', 'document_number']
    ordering = ['-date']
    
    
    
    
# class JournalEntryDetailAPIView(RetrieveUpdateDestroyAPIView):
#     queryset = JournalEntry.objects.all()
#     serializer_class = JournalEntrySerializer
    
    
class JournalEntryDetailAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated
    queryset = JournalEntry.objects.filter(is_deleted=False)
    serializer_class = JournalEntrySerializer

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
