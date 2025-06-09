from django.db import models
import uuid




class PartnerType(models.TextChoices):
    CLIENT = 'client', 'Client'
    SUPPLIER = 'supplier', 'Supplier'
    VENDOR = 'vendor', 'Vendor'
    OTHER = 'other', 'Other'
    
    

class PartnerStatus(models.TextChoices):
    ACTIVE = 'active', 'Active'
    INACTIVE = 'inactive', 'Inactive'
    
    
    
class Partner(models.Model):
    partner_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    partner_name = models.CharField(max_length=255, unique=True)
    ico = models.CharField(max_length=20, blank=True, null=True)
    dic = models.CharField(max_length=20, blank=True, null=True)
    ic_dph = models.CharField(max_length=20, blank=True, null=True)
    street = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    website = models.URLField(max_length=255, blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    partner_type = models.CharField(max_length=50, choices=PartnerType.choices, default=PartnerType.OTHER)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    partner_status = models.CharField(max_length=50, choices=PartnerStatus.choices, default=PartnerStatus.ACTIVE)

    def __str__(self):
        return self.partner_name


