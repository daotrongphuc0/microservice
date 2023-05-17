from django.db import models

# Create your models here.
class Payment(models.Model):
    customerId= models.IntegerField()
    orderId= models.IntegerField()
    status = models.CharField(max_length=255)
    time = models.CharField(max_length=255)
    amount = models.BigIntegerField()

    def __str__(self):
        return f'{self.customerId} - {self.amount}'
    
    