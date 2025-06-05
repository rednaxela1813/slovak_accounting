from rest_framework import serializers
from accounting.models import Account, JournalEntry
from rest_framework.exceptions import ValidationError as DRFValidationError
from django.core.exceptions import ValidationError as DjangoValidationError


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'number', 'name', 'account_type']
        
        
        
class JournalEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = JournalEntry
        fields = [
            'id',
            'date',
            'description',
            'document_number',
            'debit_account',
            'credit_account',
            'amount',
        ]
    def validate(self, data):
        # Если это обновление (partial=True), дополняем недостающие поля
        instance = getattr(self, 'instance', None)

        if instance:
            for field in ['debit_account', 'credit_account', 'amount', 'date', 'description', 'document_number']:
                if field not in data:
                    data[field] = getattr(instance, field)

        entry = JournalEntry(**data)

        try:
            entry.full_clean()
        except DjangoValidationError as e:
            raise DRFValidationError(e.message_dict)

        return data

        
        
