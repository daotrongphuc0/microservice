from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    phone = models.CharField(max_length=25)
    email = models.CharField(max_length=55)
    role = models.IntegerField()
    isActive = models.IntegerField()

    def __str__(self):
        return self.username
    
    def to_dict(self):
        return {
            'id':self.id,
            'username': self.username,
            'password': self.password,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'phone': self.phone,
            'email': self.email,
            'role': self.role,
            'isActive': self.isActive
        }
    




class Admin(User):
    position = models.CharField(max_length=50)

    def __str__(self):
        return f"Admin: {self.username}"
    
    def to_dict(self):
        return {
            'id':self.id,
            'username': self.username,
            'password': self.password,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'phone': self.phone,
            'email': self.email,
            'role': self.role,
            'isActive': self.isActive,
            'position':self.position
        }


class Employee(User):
    position = models.CharField(max_length=50)


    def __str__(self):
        return f"Employee: {self.username}"
    
    def to_dict(self):
        return {
            'id':self.id,
            'username': self.username,
            'password': self.password,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'phone': self.phone,
            'email': self.email,
            'role': self.role,
            'isActive': self.isActive,
            'position':self.position
        }


class Customer(User): 
    isVip =  models.IntegerField()
    isNew = models.IntegerField()
    address = models.CharField(max_length=255)
    
    def __str__(self):
        return f"Customer: {self.username}"
    
    def to_dict(self):
        return {
            'id':self.id,
            'username': self.username,
            'password': self.password,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'phone': self.phone,
            'email': self.email,
            'role': self.role,
            'isActive': self.isActive,
            "isVip":self.isVip,
            "isNew":self.isNew,
            "address":self.address
        }






