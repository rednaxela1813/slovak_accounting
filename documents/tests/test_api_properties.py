# documents/tests/test_api_properties.py

import pytest
from rest_framework.test import APIClient
from custom_user.models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken
from accounting.models import Account
from documents.models import DocumentProperty


@pytest.mark.django_db
def test_document_property_list_api():
    debit = Account.objects.create(number="504000", name="Nákup materiálu", account_type="expense")
    credit = Account.objects.create(number="321000", name="Dodávatelia", account_type="liability")

    DocumentProperty.objects.create(
        name="Faktúra od dodávateľa",
        document_type="incoming",
        debit_account=debit,
        credit_account=credit
    )

    user = CustomUser.objects.create_user(email="test@example.com", password="12345678")
    refresh = RefreshToken.for_user(user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

    response = client.get("/api/documents/properties/")
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["name"] == "Faktúra od dodávateľa"

