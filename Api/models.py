from django.db import models
import time
import uuid
# Create your models here.
class User(models.Model):
    user_name = models.CharField(max_length=200)
    user_id =  models.CharField(max_length=200,default=uuid.uuid1,unique=True)
    user_address = models.CharField(max_length=100)
    user_image = models.ImageField(upload_to ='Api/Faces/{}'.format(time.strftime("%Y-%m-%d-%H-%M-%S")))

    

    def __str__(self):
        return self.user_name

# class Product(models.Model):
#     title = models.CharField(max_length=1000)
#     price = models.IntegerField(default=0) 
#     logo = models.ImageField(upload_to ='upload/{}'.format(time.strftime("%Y-%m-%d-%H-%M-%S")))
#     description = models.CharField(max_length=10000)

#     def __str__(self):
#         return self.titles