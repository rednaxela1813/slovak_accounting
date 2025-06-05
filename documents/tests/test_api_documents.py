import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from custom_user.models import CustomUser
from django.core.files.uploadedfile import SimpleUploadedFile
from documents.models import Document


@pytest.mark.django_db
def test_upload_incoming_document():
    # create user & client
    user = CustomUser.objects.create_user(email="docuser@example.com", password="strongpass")
    refresh = RefreshToken.for_user(user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    
    
    #create test file    
    test_file = SimpleUploadedFile("test_invoice.pdf", b"dummy content", content_type="application/pdf")
    
    # POST request to upload document
    response = client.post('/api/documents/', {
        "title": "Faktúra 2024/05",
        "document_type": "invoice",
        "file": test_file,
        "date": "2024-05-01"
    }, format='multipart')
    
    assert response.status_code == 201
    assert 'document_id' in response.data
    assert response.data['title'] == "Faktúra 2024/05"
    
        
        
@pytest.fixture
def authenticated_client():
    user = CustomUser.objects.create_user(email="test@example.com", password="password")
    token = RefreshToken.for_user(user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token.access_token}")
    return client

@pytest.mark.django_db
def test_create_and_get_document(authenticated_client):
    file = SimpleUploadedFile("test.pdf", b"file_content", content_type="application/pdf")
    response = authenticated_client.post("/api/documents/", {
        "title": "Test Invoice",
        "document_type": "invoice",
        "file": file,
        "date": "2024-01-01"
    }, format='multipart')

    assert response.status_code == 201
    doc_id = response.data["document_id"]

    # Получение по ID
    response = authenticated_client.get(f"/api/documents/{doc_id}/")
    assert response.status_code == 200
    assert response.data["title"] == "Test Invoice"

@pytest.mark.django_db
def test_filter_documents(authenticated_client):
    # Создаём два документа
    Document.objects.create(title="Zmluva", document_type="contract", file="dummy.pdf", date="2024-01-01")
    Document.objects.create(title="Faktúra", document_type="invoice", file="dummy.pdf", date="2024-02-01")

    response = authenticated_client.get("/api/documents/?document_type=invoice")
    assert response.status_code == 200
    assert all(doc['document_type'] == 'invoice' for doc in response.json())