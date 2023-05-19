from django.db import models
from paying_type.models import Paying_type
# Create your models here.
class Payment(models.Model):
    customerId= models.IntegerField()
    orderId= models.IntegerField()
    status = models.CharField(max_length=255)
    time = models.CharField(max_length=255)
    paying_type= models.ForeignKey(Paying_type, on_delete=models.CASCADE)
    amount = models.BigIntegerField()

    def __str__(self):
        return f'{self.customerId} - {self.amount}'
    
    def to_dict(self):
        return {
            "id":self.id,
            "customerId":self.customerId,
            "orderId":self.orderId,
            "status":self.status,
            "time":self.time,
            "paying_type": self.paying_type.to_dict(),
            "amount":self.amount
        }
    


    