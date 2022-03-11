import os
from django.conf import settings
from django.db import models
from django.db.models.deletion import CASCADE
from easy_thumbnails.fields import ThumbnailerImageField
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

class CarModel(models.Model):
    make = models.CharField(max_length=255)
    model = models.CharField(max_length=255)

class Post(models.Model):
    title = models.CharField(max_length=255)
    type = models.IntegerField() #0 car, 1 bike
    description = models.TextField(null=True, blank=True)
    price = models.IntegerField()
    mileage = models.IntegerField(null=True)
    displacement = models.IntegerField(null=True) #bikes only
    color = models.CharField(max_length=255, null=True)
    body_type = models.CharField(max_length=255, null=True)
    location = models.CharField(max_length=255, null=True)
    registration_date = models.DateField(null=True,blank=True)
    fuel_type = models.CharField(max_length=255, null=True)
    transmission = models.CharField(max_length=255, null=True)
    owner_phone = models.CharField(max_length=255, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    carmodel = models.ForeignKey(CarModel, on_delete=models.PROTECT,related_name="carmodel", null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name="user")

class Favorites(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    class Meta:
        unique_together = [['post', 'user']]

class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = ThumbnailerImageField(upload_to='static/photos',null=True,blank=True)

def _delete_file(path):
    # Deletes file from filesystem.
    if os.path.isfile(path):
        os.remove(path)

@receiver(pre_delete, sender=PostImage)
def delete_img_pre_delete_post(sender, instance, *args, **kwargs):
    if instance.image:
        instance.image.delete_thumbnails()
        _delete_file(instance.image.path)