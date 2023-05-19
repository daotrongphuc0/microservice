from django.db import models
from user_regis.models import *
# Create your models here.

class Rate(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    productId = models.IntegerField()
    rating = models.IntegerField()
    content = models.CharField(max_length=255)

    def to_dict(self):
        return {
            'id':self.id,
            'customer': self.customer.to_dict(),
            'productId': self.productId,
            'rating': self.rating,
            'content':self.content
        }

    def __str__(self):
        return f"{self.customer.username} - {self.rating}"