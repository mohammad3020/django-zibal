from django.db import models
from django.contrib.auth import get_user_model
User=get_user_model()


class PurchaseHistory(models.Model):
    user = models.ForeignKey(User , on_delete =models.CASCADE , null=True , blank=True)
    amount = models.IntegerField(help_text="Rial")
    order = models.CharField(max_length=30 , null=True , blank=True)
    is_call_verify = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)

    trackId = models.CharField(max_length=255 , null=True , blank=True)
    result = models.CharField(max_length=255 , null=True , blank=True)
    message = models.CharField(max_length=255 , null=True , blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)
    paidAt = models.DateTimeField(null=True , blank=True)
    cardNumber = models.CharField(max_length=255 , null=True , blank=True)
    refNumber = models.CharField(max_length=255 , null=True , blank=True)

    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

