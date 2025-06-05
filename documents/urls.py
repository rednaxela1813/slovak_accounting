from django.urls import path
from .api_views import DocumentCreateListView, DocumentDetailView, DocumentPropertyListView



urlpatterns = [
    path('', DocumentCreateListView.as_view(), name='document-list-create'),
    path('<uuid:document_id>/', DocumentDetailView.as_view(), name='document-detail'),
    path('properties/', DocumentPropertyListView.as_view(), name='document-property-list'),
]



