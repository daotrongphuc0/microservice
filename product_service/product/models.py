from django.db import models
from brand.models import Brand
from category.models import Category
from supplier.models import Supplier

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)
    picture = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    price = models.BigIntegerField()
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier,on_delete=models.CASCADE)
    isActive = models.IntegerField()

    def __str__(self):
        return self.name
    
    def to_dict(self):
        return {
            'id':self.id,
            'name':self.name,
            "picture":self.picture,
            'description':self.description,
            'price':self.price,
            'brand': self.brand.to_dict(),
            'category': self.category.to_dict(),
            'supplier': self.supplier.to_dict(),
            'isActive':self.isActive
        }
    

class  Inventory(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"
    
    def to_dict(self):
        return {
            'id':self.id,
            'name':self.product.name,
            "picture":self.product.picture,
            'description':self.product.description,
            'price':self.product.price,
            'quantity':self.quantity,
            'brand': self.product.brand.to_dict(),
            'category': self.product.category.to_dict(),
            'supplier': self.product.supplier.to_dict(),
            'isActive':self.product.isActive,
            'quantity':self.quantity
        }