from django.db import models

from user.models    import Address, User
from product.models import MainCategory

class NearbyCategory(models.Model):
    name          = models.CharField(max_length=100)
    main_category = models.ForeignKey('product.MainCategory', on_delete = models.SET_NULL, null=True)
    created_at    = models.DateTimeField(auto_now_add = True) 
    deleted_at    = models.DateTimeField(null = True) 

    class Meta:
        db_table = 'nearbycategories'

class Nearby(models.Model):
    name            = models.CharField(max_length=100)
    price           = models.DecimalField(max_digits= 7, decimal_places=2)
    nearby_category = models.ForeignKey('NearbyCategory', on_delete = models.SET_NULL, null=True)
    uploader        = models.ForeignKey('user.User', on_delete = models.SET_NULL, null=True, related_name='uploader_nearby')
    viewed          = models.IntegerField(null=True)
    address         = models.ForeignKey('user.Address', on_delete = models.SET_NULL, null=True, related_name='address_nearby')
    description     = models.CharField(max_length=2000)
    created_at      = models.DateTimeField(auto_now_add = True) 
    updated_at      = models.DateTimeField(auto_now = True)
    comment         = models.ManyToManyField('user.User', through = 'NearbyComment')
    created_at      = models.DateTimeField(auto_now_add = True) 
    deleted_at      = models.DateTimeField(null = True) 

    class Meta:
        db_table = 'nearbys'

class NearbyImage(models.Model):
    nearby     = models.ForeignKey('Nearby', on_delete = models.SET_NULL, null=True)
    image_url  = models.URLField(max_length = 2000, null=True)
    created_at = models.DateTimeField(auto_now_add = True) 
    deleted_at = models.DateTimeField(null = True) 

    class Meta:
        db_table = 'nearbyimages'

class NearbyComment(models.Model):
    uploader    = models.ForeignKey('user.User', on_delete = models.SET_NULL, null=True)
    nearby     = models.ForeignKey('Nearby', on_delete = models.SET_NULL, null=True)
    content    = models.CharField(max_length=2000)
    created_at = models.DateTimeField(auto_now = True)
    deleted_at = models.DateTimeField(null = True) 
    
    class Meta:
        db_table='nearbycomments'