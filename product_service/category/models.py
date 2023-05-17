from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    picture = models.CharField(max_length=255)

    def __str__(self):
        return self.code
    
    def to_dict(self):
        return {
            'id':self.id,
            'name': self.name,
            'code': self.code,
            'picture': self.picture
        }