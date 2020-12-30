from django.db import models

class Product(models.Model):
    name             = models.CharField(max_length=100)
    price            = models.DecimalField(max_digits= 7, decimal_places=2)
    product_category = models.ForeignKey('ProductCategory', on_delete = models.SET_NULL, null=True)
    uploader         = models.ForeignKey('user.User', on_delete = models.SET_NULL, null=True)
    viewed           = models.IntegerField(null=True)
    selling_address  = models.ForeignKey('user.Address', on_delete = models.SET_NULL, null=True)
    description      = models.CharField(max_length=2000)
    access_range     = models.IntegerField(null=True)
    order_status     = models.ForeignKey('user.OrderStatus', on_delete = models.SET_NULL, null=True)
    created_at       = models.DateTimeField(auto_now_add = True) 
    updated_at       = models.DateTimeField(auto_now = True)
    deleted_at       = models.DateTimeField(null = True) 

    class Meta:
        db_table = 'products'

class ProductImage(models.Model):
    product    = models.ForeignKey('Product', on_delete = models.SET_NULL, null=True)
    image_url  = models.URLField(max_length = 2000, null=True)
    created_at = models.DateTimeField(auto_now_add = True) 
    deleted_at = models.DateTimeField(null = True) 

    class Meta:
        db_table = 'productimages'

class MainCategory(models.Model):
    name       = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add = True) 
    deleted_at = models.DateTimeField(null = True) 

    class Meta:
        db_table = 'maincategories'

class ProductCategory(models.Model):
    name          = models.CharField(max_length=100)
    main_category = models.ForeignKey('MainCategory', on_delete = models.SET_NULL, null=True)
    created_at    = models.DateTimeField(auto_now_add = True) 
    deleted_at    = models.DateTimeField(null = True) 

    class Meta:
        db_table = 'productcategories'