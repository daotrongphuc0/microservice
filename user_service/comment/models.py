from django.db import models
from user_regis.models import*
# Create your models here.
class Comment(models.Model):
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='child_comments')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    productId = models.IntegerField()
    conten = models.CharField(max_length=255)
    time = models.CharField(max_length=50)

    def to_dict(self):
        # parent_comment_dict = None
        # if self.parent_comment is not None:
        #     parent_comment_dict = self.parent_comment.to_dict()
        customer_dict = self.customer.to_dict() if self.customer is not None else None
        return {
            'id': self.id,
            'customer': customer_dict,
            'productId': self.productId,
            'conten': self.conten,
            'time': self.time,
            'chill_comment': self.get_chil(),
        }
    
    def to_detail_dict(self):
        parent_comment_dict = None
        if self.parent_comment is not None:
            parent_comment_dict = self.parent_comment.to_dict()
        customer_dict = self.customer.to_dict() if self.customer is not None else None
        return {
            'id': self.id,
            'parent_comment': parent_comment_dict,
            'customer': customer_dict,
            'productId': self.productId,
            'conten': self.conten,
            'time': self.time,
        }

    def __str__(self):
        return f"{self.customer.username} - {self.conten}"
    
    def get_chil(self):
        chil = Comment.objects.filter(parent_comment=self)
        if(chil):
            return [comment.to_dict() for comment in chil]
        return []
