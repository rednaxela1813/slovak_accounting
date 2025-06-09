import pytest
from accounting.tests.test_api_accounts import get_authenticated_client
from partners.models import Partner, PartnerType
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
def test_partner_list_all_fields():
    client = get_authenticated_client()

    Partner.objects.create(
        partner_name="Test Company",
        ico="12345678",
        dic="1234567890",
        ic_dph="SK1234567890",
        street="Main Street 1",
        city="Bratislava",
        postal_code="81101",
        country="Slovakia",
        email="info@example.com",
        phone="+421900123456",
        website="https://example.com",
        note="VIP customer",
        partner_type="client",
        partner_status = 'ACTIVE'
    )

    response = client.get('/api/partners/')
    assert response.status_code == 200
    assert len(response.data) == 1

    data = response.data[0]
    assert data['partner_name'] == "Test Company"
    assert data['ico'] == "12345678"
    assert data['dic'] == "1234567890"
    assert data['ic_dph'] == "SK1234567890"
    assert data['street'] == "Main Street 1"
    assert data['city'] == "Bratislava"
    assert data['postal_code'] == "81101"
    assert data['country'] == "Slovakia"
    assert data['email'] == "info@example.com"
    assert data['phone'] == "+421900123456"
    assert data['website'] == "https://example.com"
    assert data['note'] == "VIP customer"
    assert data['partner_type'] == "client"
    assert data['partner_status'] == 'ACTIVE'
    assert 'created_at' in data
    assert 'updated_at' in data




@pytest.mark.django_db
def test_partner_filter_by_type_and_status():
    client = get_authenticated_client()
    
    #Create partners with different types and statuses
    Partner.objects.create(partner_name="Active Client", partner_type=PartnerType.CLIENT, partner_status='active')
    Partner.objects.create(partner_name="Inactive Client", partner_type=PartnerType.CLIENT, partner_status='inactive')
    Partner.objects.create(partner_name="Active Supplier", partner_type=PartnerType.SUPPLIER, partner_status='active')
    Partner.objects.create(partner_name="Inactive Supplier", partner_type=PartnerType.SUPPLIER, partner_status='inactive')
    Partner.objects.create(partner_name="Active Vendor", partner_type=PartnerType.VENDOR, partner_status='active')
    Partner.objects.create(partner_name="Inactive Vendor", partner_type=PartnerType.VENDOR, partner_status='inactive')
    Partner.objects.create(partner_name="Other Partner", partner_type=PartnerType.OTHER, partner_status='active')
    Partner.objects.create(partner_name="Inactive Other", partner_type=PartnerType.OTHER, partner_status='inactive')
    
    # Filter by type and status
    response = client.get('/api/partners/', {'partner_type': PartnerType.CLIENT, 'partner_status': 'active'})
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['partner_name'] == "Active Client"
    assert response.data[0]['partner_type'] == PartnerType.CLIENT
    assert response.data[0]['partner_status'] == 'active'
    assert 'created_at' in response.data[0]
    assert 'updated_at' in response.data[0]
    
    response = client.get('/api/partners/', {'partner_type': PartnerType.SUPPLIER, 'partner_status': 'inactive'})
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['partner_name'] == "Inactive Supplier"
    assert response.data[0]['partner_type'] == PartnerType.SUPPLIER
    assert response.data[0]['partner_status'] == 'inactive'
    assert 'created_at' in response.data[0]
    assert 'updated_at' in response.data[0]
    
    response = client.get('/api/partners/', {'partner_type': PartnerType.VENDOR, 'partner_status': 'active'})
    assert response.status_code == 200
    assert len(response.data) == 1      
    assert response.data[0]['partner_name'] == "Active Vendor"
    assert response.data[0]['partner_type'] == PartnerType.VENDOR
    assert response.data[0]['partner_status'] == 'active'
    assert 'created_at' in response.data[0]
    assert 'updated_at' in response.data[0]
    response = client.get('/api/partners/', {'partner_type': PartnerType.OTHER, 'partner_status': 'active'})
    
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['partner_name'] == "Other Partner"
    assert response.data[0]['partner_type'] == PartnerType.OTHER
    assert response.data[0]['partner_status'] == 'active'
    assert 'created_at' in response.data[0]
    assert 'updated_at' in response.data[0]
    # Test with no matching partner
    
    response = client.get('/api/partners/', {'partner_type': PartnerType.CLIENT, 'partner_status': 'inactive'})
    assert response.status_code == 200
    assert len(response.data) == 1
    response = client.get('/api/partners/', {'partner_type': PartnerType.SUPPLIER, 'partner_status': 'active'})
    assert response.status_code == 200
    assert len(response.data) == 1
    response = client.get('/api/partners/', {'partner_type': PartnerType.VENDOR, 'partner_status': 'inactive'})
    assert response.status_code == 200
    assert len(response.data) == 1
    response = client.get('/api/partners/', {'partner_type': PartnerType.OTHER, 'partner_status': 'inactive'})
    assert response.status_code == 200
    assert len(response.data) == 1
    
    
    



