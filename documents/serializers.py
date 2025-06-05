from rest_framework import serializers
from .models import Document, DocumentProperty

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['document_id', 'title', 'document_type', 'file', 'date', 'created_at']
        
        
class DocumentPropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentProperty
        fields = ['property_id', 'name', 'document_type', 'debit_account', 'credit_account']
        read_only_fields = ['property_id']
        
    def validate(self, attrs):
        if attrs['debit_account'] == attrs['credit_account']:
            raise serializers.ValidationError("Debit and credit accounts cannot be the same.")
        return attrs
