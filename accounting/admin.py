from django.contrib import admin
from .models import Account, JournalEntry


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'name', 'account_type')
    search_fields = ('number', 'name')
    list_filter = ('account_type',)
    ordering = ('number',)
    
@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'description', 'document_number', 'debit_account', 'credit_account', 'amount')
    search_fields = ('description', 'document_number')
    list_filter = ('date', 'debit_account', 'credit_account')
    ordering = ('-date',)
    
    