import django_filters 
from .models import JournalEntry


class JournalEntryFilter(django_filters.FilterSet):
    date__gte = django_filters.DateFilter(field_name='date', lookup_expr='gte')
    date_lte = django_filters.DateFilter(field_name='date', lookup_expr='lte')
    debit_account = django_filters.NumberFilter(field_name='debit_account__id')
    credit_account = django_filters.NumberFilter(field_name='credit_account__id')
    
    class Meta:
        model = JournalEntry
        fields = ['debit_account', 'credit_account', 'date']
