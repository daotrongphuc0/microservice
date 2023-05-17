from django.db import models

# Create your models here.

class Supplier(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
    def to_dict(self):
        return {
            'id':self.id,
            'name': self.name,
            'email': self.email,
            'address': self.address,
            'phone': self.phone
        }