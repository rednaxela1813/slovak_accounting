# documents/tests/test_models.py

import pytest
from documents.models import DocumentProperty
from accounting.models import Account

@pytest.mark.django_db
def test_document_property_creation():
    debit = Account.objects.create(number="504000", name="Nákup materiálu", account_type="expense")
    credit = Account.objects.create(number="321000", name="Dodávatelia", account_type="liability")

    prop = DocumentProperty.objects.create(
        name="Faktúra od dodávateľa",
        document_type="incoming",
        debit_account=debit,
        credit_account=credit
    )

    assert prop.name == "Faktúra od dodávateľa"
    assert prop.debit_account.number == "504000"
    assert prop.credit_account.number == "321000"
