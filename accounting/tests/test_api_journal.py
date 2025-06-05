import pytest
from accounting.models import Account, JournalEntry
from rest_framework.test import APIClient
from accounting.tests.test_api_accounts import get_authenticated_client
from custom_user.models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken





@pytest.mark.django_db
def test_journal_entry_api_validation_errors():
    account = Account.objects.create(number='221000', name='Banka', account_type='asset')
    another = Account.objects.create(number='602000', name='Tržby', account_type='income')

    client = get_authenticated_client()


    # тест: одинаковые счета
    response = client.post('/api/journal-entries/', {
        "date": "2024-01-01",
        "description": "Неверная проводка",
        "amount": 100,
        "document_number": "2024/X",
        "debit_account": account.id,
        "credit_account": account.id,  # ⛔️ одинаковый
    }, format='json')

    assert response.status_code == 400
    assert "__all__" in response.json()


    # тест: сумма = 0
    response = client.post('/api/journal-entries/', {
        "date": "2024-01-01",
        "description": "Сумма ноль",
        "amount": 0,  # ⛔️ недопустимая сумма
        "document_number": "2024/Y",
        "debit_account": account.id,
        "credit_account": another.id,
    }, format='json')

    assert response.status_code == 400
    assert "__all__" in response.json()
    
    
    
@pytest.mark.django_db
def test_journal_entry_update_and_delete():
    debit = Account.objects.create(number='221000', name='Banka', account_type='asset')
    credit = Account.objects.create(number='602000', name='Tržby', account_type='income')

    entry = JournalEntry.objects.create(
        date="2024-01-01",
        description="Original description",
        amount=200,
        document_number="INV-1",
        debit_account=debit,
        credit_account=credit,
    )

    client = get_authenticated_client()


    # PATCH (обновление описания)
    patch_response = client.patch(f'/api/journal-entries/{entry.id}/', {
        "description": "Updated description"
    }, format='json')

    assert patch_response.status_code == 200
    assert patch_response.json()['description'] == "Updated description"

    # DELETE
    delete_response = client.delete(f'/api/journal-entries/{entry.id}/')
    assert delete_response.status_code == 204
    # Убедимся, что объект помечен как удалённый
    assert JournalEntry.objects.count() == 1
    assert JournalEntry.objects.filter(is_deleted=False).count() == 0
    assert JournalEntry.objects.filter(is_deleted=True).count() == 1




@pytest.mark.django_db
def test_journal_entry_put_updates_all_fields():
    debit = Account.objects.create(number='221000', name='Banka', account_type='asset')
    credit = Account.objects.create(number='602000', name='Tržby', account_type='income')
    new_credit = Account.objects.create(number='311000', name='Odberatelia', account_type='asset')

    entry = JournalEntry.objects.create(
        date="2024-01-01",
        description="Original",
        amount=100,
        document_number="INV-1",
        debit_account=debit,
        credit_account=credit,
    )

    client = get_authenticated_client()


    response = client.put(f'/api/journal-entries/{entry.id}/', {
        "date": "2024-01-02",
        "description": "Updated all fields",
        "amount": 200,
        "document_number": "INV-999",
        "debit_account": debit.id,
        "credit_account": new_credit.id
    }, format='json')

    assert response.status_code == 200
    data = response.json()
    assert data['description'] == "Updated all fields"
    assert data['amount'] == '200.00'
    assert data['document_number'] == "INV-999"




