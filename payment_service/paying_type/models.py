from django.db import models

# Create your models here.
class Paying_type(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    enable = models.IntegerField()

    def __str__(self) :
        return self.name
    

    def to_dict(self):
        return{
            "id":self.id,
            "name":self.name,
            "description":self.description,
            "enable":self.enable
        }
    
    