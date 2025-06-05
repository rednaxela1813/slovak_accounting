from django.db import models
from django.core.exceptions import ValidationError
import uuid



class Account(models.Model):
    ACCOUNT_TYPES = [
        ('asset', 'Актив / Majetok'),
    ('liability', 'Пассив / Záväzky'),
    ('income', 'Доход / Výnos'),
    ('expense', 'Расход / Náklad'),
    ('equity', 'Капитал / Vlastné imanie'),
    ]
    account_id = models.UUIDField(
        default=uuid.uuid4, 
        editable=False, 
        unique=True
    )
    
    number = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)
    account_type = models.CharField(
        max_length=10,
        choices=ACCOUNT_TYPES)
        
    
    def __str__(self):
        return f"{self.number} - { self.name}"
    
    
class JournalEntry(models.Model):
    
    journal_entry_id = models.UUIDField(
        default=uuid.uuid4, 
        editable=False, 
        unique=True
    )
    
    date = models.DateField()
    description = models.TextField()
    document_number = models.CharField(max_length=50)
    
    debit_account = models.ForeignKey(
        Account, 
        related_name='debits', 
        on_delete=models.CASCADE
    )
    credit_account = models.ForeignKey(
        Account, 
        related_name='credits', 
        on_delete=models.CASCADE
    )
    
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2
    )
    
    is_deleted = models.BooleanField(default=False)
    
    def clean(self):
        if self.debit_account == self.credit_account:
            raise ValidationError("Debetový a kreditný účet nemôžu byť rovnaké.")

        if self.amount <= 0:
            raise ValidationError("Suma zápisu musí byť väčšia ako 0.")
    
    def __str__(self):
        return f"{self.date} | {self.description} | {self.debit_account.number} → {self.credit_account.number} | {self.amount} €"