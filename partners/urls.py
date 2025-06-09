from django.urls import path
from partners.viewsets import PartnerListCreateView



urlpatterns = [
    path('', PartnerListCreateView.as_view(), name='partner-list'),
   # path('<uuid:partner_id>/', PartnerDetailView.as_view(), name='partner-detail'),
]