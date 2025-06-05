import pytest
from accounting.models import Account


@pytest.mark.django_db
def test_account_creation():
    account = Account.objects.create(
        number = '311000',
        name = 'Odberatelia',
        account_type = 'asset'
                
    )
    
    assert account.number == '311000'
    assert account.name == 'Odberatelia'
    assert account.account_type == 'asset'