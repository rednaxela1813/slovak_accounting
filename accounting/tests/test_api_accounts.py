import pytest
from accounting.models import Account, JournalEntry
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from custom_user.models import CustomUser
from decimal import Decimal





def get_authenticated_client():
    user = CustomUser.objects.create_user(email="test@example.com", password="strongpass")
    refresh = RefreshToken.for_user(user)
    
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    return client


@pytest.mark.django_db
def test_account_list_api_returns_accounts():
    client = get_authenticated_client()

    Account.objects.create(number="221000", name="Bankový účet", account_type="asset")
    Account.objects.create(number="602000", name="Tržby za tovar", account_type="income")

    response = client.get('/api/accounts/')

    assert response.status_code == 200
    assert len(response.data) == 2
    assert response.data[0]['number'] == '221000'
    assert response.data[1]['number'] == '602000'


@pytest.mark.django_db
def test_journal_entry_list_and_create():
    client = get_authenticated_client()
    debit = Account.objects.create(number='221000', name='Banka', account_type='asset')
    credit = Account.objects.create(number='602000', name='Tržby', account_type='income')

    response = client.post('/api/journal-entries/', {
        "date": "2024-01-01",
        "description": "Predaj",
        "amount": 100,
        "document_number": "2024/INV-01",
        "debit_account": debit.id,
        "credit_account": credit.id,
    }, format='json')

    assert response.status_code == 201
    assert JournalEntry.objects.count() == 1

    response = client.get('/api/journal-entries/')
    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.django_db
def test_journal_entry_retrieve_api():
    client = get_authenticated_client()
    debit = Account.objects.create(number='221000', name='Banka', account_type='asset')
    credit = Account.objects.create(number='602000', name='Tržby', account_type='income')

    entry = JournalEntry.objects.create(
        date="2024-01-01",
        description="Test Detail",
        amount=Decimal('123.45'),
        document_number="2024/INV-999",
        debit_account=debit,
        credit_account=credit,
    )

    response = client.get(f'/api/journal-entries/{entry.id}/')

    assert response.status_code == 200
    data = response.json()
    assert data['id'] == entry.id
    assert Decimal(data['amount']) == Decimal('123.45')
    assert data['description'] == "Test Detail"
