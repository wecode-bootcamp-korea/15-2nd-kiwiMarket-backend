from phonenumber_field.modelfields import PhoneNumberField
from django.db import models

#from product.models import Product

class User(models.Model):
    phone_number    = PhoneNumberField(null=False, blank=False, unique=True)
    nickname        = models.CharField(max_length=20, null=False, unique=True)
    profile_picture = models.URLField(max_length = 2000, null=True)
    email           = models.EmailField(max_length=100, unique=True)
    random_token    = models.IntegerField(null=True)
    anonymous       = models.BooleanField(default=False)
    address         = models.ManyToManyField('Address', through='FullAddress') 
    wish_category   = models.ManyToManyField('product.ProductCategory', through = 'WishCategory')
    wishlist        = models.ManyToManyField('product.Product', through ='Wishlist', related_name='wishlist_user')
    manner_temp     = models.ManyToManyField('MannerTemperatureCategory', through = 'MannerTemperature')
    my_review       = models.ManyToManyField('product.Product', through = 'Review', related_name='my_review_user')
    liked_uploader  = models.ManyToManyField('self', through = 'UploaderLike', symmetrical = False)
    created_at      = models.DateTimeField(auto_now_add = True) 
    deleted_at      = models.DateTimeField(null = True) 

    class Meta:
        db_table = 'users'

class AuthSms(models.Model):
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)
    auth_number  = models.IntegerField()
    created_at   = models.DateTimeField(auto_now_add = True) 
    deleted_at   = models.DateTimeField(null = True) 

    class Meta:
        db_table = 'authsms'

class Address(models.Model):
    neighborhood = models.CharField(max_length=20, null=False, default='')
    region       = models.CharField(max_length=20, null=False, default='')
    district     = models.CharField(max_length=20, null=False, default='')
    code         = models.IntegerField()
    longitude    = models.DecimalField(max_digits= 9, decimal_places=6) 
    latitude     = models.DecimalField(max_digits= 9, decimal_places=6)
    created_at   = models.DateTimeField(auto_now_add = True, null = True) 
    deleted_at   = models.DateTimeField(null = True) 

    class Meta:
        db_table = "addresses"

class FullAddress(models.Model):
    full_address = models.ForeignKey('Address', on_delete = models.SET_NULL, null=True)
    user         = models.ForeignKey('User', on_delete = models.SET_NULL, null=True)
    created_at   = models.DateTimeField(auto_now_add = True) 
    deleted_at   = models.DateTimeField(null = True) 

    class Meta:
        db_table = 'fulladdresses'

class WishCategory(models.Model):
    product_category    = models.ForeignKey('product.ProductCategory', on_delete = models.SET_NULL, null=True)
    user                = models.ForeignKey('User', on_delete = models.SET_NULL, null=True)
    is_liked            = models.BooleanField()
    created_at          = models.DateTimeField(auto_now_add = True) 
    deleted_at          = models.DateTimeField(null = True) 

    class Meta:
        db_table = 'wishcategories'

class Wishlist(models.Model):
    product     = models.ForeignKey('product.Product', on_delete = models.SET_NULL, null=True)
    user        = models.ForeignKey('User', on_delete = models.SET_NULL, null=True, related_name='user_wishlist')
    is_liked    = models.BooleanField()
    created_at  = models.DateTimeField(auto_now_add = True)
    deleted_at  = models.DateTimeField(null = True) 

    class Meta:
        db_table = 'wishlists'
    
class KeywordAlarm(models.Model):
    keyword    = models.CharField(max_length=100)
    user       = models.ForeignKey('User', on_delete = models.SET_NULL, null=True)
    address    = models.ManyToManyField('Address', through='KeywordAddress')
    created_at = models.DateTimeField(auto_now_add = True) 
    deleted_at = models.DateTimeField(null = True) 

    class Meta:
        db_table = 'keywordalarms'

class KeywordAddress(models.Model):
    keyword_alarm = models.ForeignKey('KeywordAlarm',on_delete = models.SET_NULL, null=True)
    address       = models.ForeignKey('Address',on_delete = models.SET_NULL, null=True)
    created_at    = models.DateTimeField(auto_now_add = True) 
    deleted_at    = models.DateTimeField(null = True) 

    class Meta:
        db_table = 'keywordaddresses'

class OftenUsedDescription(models.Model):
    user        = models.ForeignKey('User', on_delete = models.SET_NULL, null=True)
    description = models.CharField(max_length=2000)
    created_at  = models.DateTimeField(auto_now_add = True) 
    deleted_at  = models.DateTimeField(null = True) 

    class Meta:
        db_table = 'oftenuseddescription'

class UploaderLike(models.Model):
    uploader   = models.ForeignKey('User', on_delete = models.SET_NULL, null=True, related_name='uploader_uploaderlike')
    user       = models.ForeignKey('User', on_delete = models.SET_NULL, null=True, related_name='user_uploaderlike')    
    is_liked   = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add = True) 
    deleted_at = models.DateTimeField(null = True) 

    class Meta:
        db_table = 'uploaderliked'

class Order(models.Model):
    product     = models.ForeignKey('product.Product', on_delete = models.SET_NULL, null=True)
    user        = models.ForeignKey('User', on_delete = models.SET_NULL, null=True)
    order_date  = models.DateTimeField(auto_now = True)
    created_at  = models.DateTimeField(auto_now_add = True) 
    deleted_at  = models.DateTimeField(null = True) 

    class Meta:
        db_table = 'orders'

class OrderStatus(models.Model):
    name       = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add = True) 
    deleted_at = models.DateTimeField(null = True) 

    class Meta:
        db_table = 'orderstatuses'

class MannerTemperature(models.Model):
    user                = models.ForeignKey('User', on_delete = models.SET_NULL, null=True)
    manner_temperature  = models.ForeignKey('MannerTemperatureCategory', on_delete = models.SET_NULL, null=True)
    created_at          = models.DateTimeField(auto_now_add = True)     
    deleted_at          = models.DateTimeField(null = True) 

    class Meta: 
        db_table = 'mannertemperatures'

class MannerTemperatureCategory(models.Model):
    name       = models.CharField(max_length=100)
    point      = models.DecimalField(max_digits= 2, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add = True)     
    deleted_at = models.DateTimeField(null = True) 

    class Meta:
        db_table = 'mannertemperaturescategories'

class Review(models.Model):
    uploader     = models.ForeignKey('User', on_delete = models.SET_NULL, null=True)
    product      = models.ForeignKey('product.Product', on_delete = models.SET_NULL, null=True)
    description  = models.CharField(max_length=2000)
    created_at   = models.DateTimeField(auto_now_add = True) 
    deleted_at   = models.DateTimeField(null = True) 

    class Meta:
        db_table = 'reviews'
