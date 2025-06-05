import pytest
from accounting.models import JournalEntry, Account
from django.core.exceptions import ValidationError



@pytest.mark.django_db
def test_journal_entry_creation():
    # создаём два счёта
    debit_account = Account.objects.create(number="311000", name="Odberatelia", account_type="asset")
    credit_account = Account.objects.create(number="602000", name="Tržby za tovar", account_type="income")

    # создаём проводку
    entry = JournalEntry.objects.create(
        date='2024-01-01',
        description='Predaj tovaru',
        debit_account=debit_account,
        credit_account=credit_account,
        amount=100.00,
        document_number='2024/001'
    )
    
    assert entry.debit_account.number == '311000'
    assert entry.credit_account.number == '602000'
    assert entry.amount == 100.00
    assert entry.description == 'Predaj tovaru'
    assert entry.document_number == '2024/001'
    
    
@pytest.mark.django_db
def test_journal_entry_same_account_invalid():
    account = Account.objects.create(number="221000", name='Bankový účet', account_type='asset')
    
    entry = JournalEntry(
        date="2025-01-01",
        description='Ошибка: одинаковые счета',
        debit_account=account,
        credit_account=account,
        amount=50.00,
        document_number='2024/001'
    )
    
    with pytest.raises(ValidationError):
        entry.full_clean()
        
        
@pytest.mark.django_db
def test_journal_entry_with_negative_amount_invalid():
    debit_account = Account.objects.create(number='221000', name='Banka', account_type='asset')
    credit_account = Account.objects.create(number='602000', name='Tržby', account_type='income')

    entry = JournalEntry(
        date='2024-01-01',
        description='Neplatná zápis s nulou alebo mínusom',
        debit_account=debit_account,
        credit_account=credit_account,
        amount=0,  # тестируем 0 — и можно потом проверить -100
        document_number='2024/002'
    )

    with pytest.raises(ValidationError):
        entry.full_clean()