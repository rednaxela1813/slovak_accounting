import pytest
from accounting.tests.test_api_accounts import get_authenticated_client
from partners.models import Partner, PartnerType, PartnerStatus
from rest_framework_simplejwt.tokens import RefreshToken
from custom_user.models import CustomUser



@pytest.mark.django_db
def test_partner_list_api_returns_partners():
    client = get_authenticated_client()

    Partner.objects.create(partner_name="Partner A", partner_type=PartnerType.CLIENT)
    Partner.objects.create(partner_name="Partner B", partner_type=PartnerType.SUPPLIER)

    response = client.get('/api/partners/')

    assert response.status_code == 200
    assert len(response.data) == 2
    assert response.data[0]['partner_name'] == 'Partner A'
    assert response.data[1]['partner_name'] == 'Partner B'
    
    
    

    
@pytest.mark.django_db
def test_soft_delete_partner():
    client = get_authenticated_client()
    
    partner = Partner.objects.create(partner_name="Test Partner", partner_type=PartnerType.CLIENT, partner_status=PartnerStatus.ACTIVE)

    response = client.delete(f'/api/partners/{partner.partner_id}/')
    assert response.status_code == 204

    partner.refresh_from_db()
    assert partner.partner_status == PartnerStatus.INACTIVE

    # Убеждаемся, что он больше не отображается в списке
    response = client.get('/api/partners/')
    partner_names = [p['partner_name'] for p in response.data]
    assert "Test Partner" not in partner_names
    
    



