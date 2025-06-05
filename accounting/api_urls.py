from django.urls import path
from .api_views import AccountListAPIView, JournalEntryListCreateAPIView, JournalEntryDetailAPIView


urlpatterns = [
    path('accounts/', AccountListAPIView.as_view()),
    path('journal-entries/', JournalEntryListCreateAPIView.as_view()),
    path('journal-entries/<int:pk>/', JournalEntryDetailAPIView.as_view()),
]




