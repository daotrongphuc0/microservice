from django.db import models

# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=50)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
    def to_dict(self):
        company_dict = {
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "address": self.address,
        }
        return company_dict
    

