from rest_framework import generics, permissions, filters
from documents.models import Document, DocumentProperty
from .serializers import DocumentSerializer, DocumentPropertySerializer

from django_filters.rest_framework import DjangoFilterBackend





# class DocumentCreateView(generics.ListCreateAPIView):
#     """
#     API view to create a new document.
#     """
#     queryset = Document.objects.all()
#     serializer_class = DocumentSerializer
#     permission_classes = [permissions.IsAuthenticated]  # Ensure the user is authenticated
    
    
    


class DocumentCreateListView(generics.ListCreateAPIView):
    queryset = Document.objects.all().order_by('-date')
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['document_type', 'date']
    ordering_fields = ['date', 'created_at']
    

class DocumentDetailView(generics.RetrieveAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'document_id'


class DocumentPropertyListView(generics.ListAPIView):
    queryset = DocumentProperty.objects.all()
    serializer_class = DocumentPropertySerializer
    permission_classes = [permissions.IsAuthenticated]