from django.db import models
from company.models import Company
# Create your models here.
class Shipping(models.Model):
    customerId= models.IntegerField()
    orderId= models.IntegerField()
    company = models.ForeignKey(Company,on_delete=models.CASCADE)
    intendTime = models.CharField(max_length=255,null=True)
    startTime = models.CharField(max_length=255)
    status = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.customerId} - {self.orderId}'
    
    def to_dict(self):
        stages = Stage.objects.filter(shipping=self).order_by('-time')
        shipping_dict = {
            'id':self.id,
            "customerId": self.customerId,
            "orderId": self.orderId,
            "company": self.company.to_dict(),  # Sử dụng phương thức to_dict() từ lớp Company
            "intendTime": self.intendTime,
            "startTime": self.startTime,
            "status": self.status,
            "stage":[stage.to_dict() for stage in stages]
        }
        return shipping_dict
    

class Stage(models.Model):
    time = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    comment  = models.CharField(max_length=255)
    shipping = models.ForeignKey(Shipping,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.shipping} - {self.time}'
    
    def to_dict(self):
        shipping_detail_dict = {
            "time": self.time,
            "location": self.location,
            "comment": self.comment,
        }
        return shipping_detail_dict

