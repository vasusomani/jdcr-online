import re
import uuid
from django.urls import reverse
from django.db import models
from core.utils import dnb
from django.utils.translation import gettext_lazy as _

class Payment(models.Model):
    name = models.CharField(max_length=255, **dnb)
    email = models.CharField(max_length=255, **dnb)
    phone = models.CharField(max_length=31, **dnb)
    country = models.CharField(max_length=31, **dnb)
    amount = models.PositiveBigIntegerField(**dnb)
    currency = models.CharField(max_length=255, **dnb)
    remarks = models.TextField(**dnb)
    rzp_order_id = models.CharField(max_length=255)
    rzp_payment_id = models.CharField(max_length=255)
    rzp_signature = models.CharField(max_length=255)
    payment_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.rzp_order_id}"
    
