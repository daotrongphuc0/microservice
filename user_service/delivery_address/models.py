from django.db import models
from user_regis.models import *
# Create your models here.
class DeliveryAddres(models.Model):
    customer =  models.ForeignKey(Customer,on_delete=models.CASCADE)
    province = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    ward = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    def to_dict(self):
        return {
            'id':self.id,
            'customer': self.customer.to_dict(),
            'province': self.province,
            'district': self.district,
            'ward': self.ward,
            'address': self.address
        }

    def __str__(self):
        return f"Delovery: {self.customer.username}"