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
from drf_spectacular.utils import extend_schema, OpenApiExample





@extend_schema(
    tags=["Accounting - Accounts"],
    summary="List all accounts",
    description="Returns all available accounting accounts in the system."
)
class AccountListAPIView(APIView):
    """
    Returns a list of all accounting accounts.

    Example response:
    [
        {
            "id": 1,
            "number": "221000",
            "name": "Bank Account",
            "account_type": "asset"
        }
    ]
    """
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated
    
    def get(self, request):
        accounts = Account.objects.all()
        serializer = AccountSerializer(accounts, many=True)
        return Response(serializer.data)
    
    

# class JournalEntryListCreateAPIView(ListCreateAPIView):
#     queryset = JournalEntry.objects.all()
#     serializer_class = JournalEntrySerializer


    
@extend_schema(
    tags=["Accounting - Journal Entries"],
    summary="List or create journal entries",
    description="Returns a list of journal entries or creates a new entry.",
    examples=[
        OpenApiExample(
            name="Sample Journal Entry",
            value={
                "date": "2025-06-01",
                "description": "Purchase of goods",
                "document_number": "PUR-2025-001",
                "debit_account": 101,
                "credit_account": 321,
                "amount": "500.00"
            },
            request_only=True
        )
    ]
)
class JournalEntryListCreateAPIView(ListCreateAPIView):
    """
    Retrieve or create accounting journal entries.

    Supports filters:
    - `date__gte`
    - `date__lte`
    - `debit_account`
    - `credit_account`

    Example POST body:
    {
        "date": "2025-06-01",
        "description": "Invoice payment",
        "document_number": "INV-2025-001",
        "debit_account": 1,
        "credit_account": 2,
        "amount": "1000.00"
    }
    """
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
