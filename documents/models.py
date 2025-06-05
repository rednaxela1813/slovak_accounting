import uuid
from django.db import models
from accounting.models import Account


class Document(models.Model):
    DOCUMENT_TYPES = [
        ('invoice', 'Faktúra'),
        ('contract', 'Zmluva'),
        ('receipt', 'Pokladničný doklad'),
        ('other', 'Iný'),
    ]

    document_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    file = models.FileField(upload_to='documents/')
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



class DocumentProperty(models.Model):
    property_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    document_type = models.CharField(max_length=20, choices=[('incoming', 'Incoming'), ('outgoing', 'Outgoing')])
    debit_account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='debit_properties')
    credit_account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='credit_properties')
    