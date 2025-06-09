import django_filters as filters

from .models import Partner


class PartnerFilter(filters.FilterSet):
    class Meta:
        model = Partner
        fields = {
            'partner_name': ['exact', 'icontains'],
            'partner_type': ['exact'],
            'ico': ['exact', 'icontains'],
            'dic': ['exact', 'icontains'],
            'ic_dph': ['exact', 'icontains'],
            'street': ['exact', 'icontains'],
            'city': ['exact', 'icontains'],
            'postal_code': ['exact', 'icontains'],
            'country': ['exact', 'icontains'],
            'email': ['exact', 'icontains'],
            'phone': ['exact', 'icontains'],
            'website': ['exact', 'icontains'],
            'partner_status': ['exact'],
        }
        