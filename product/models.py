from django.db import models
from django.forms import ModelForm

#from user.models    import User, Address, OrderStatus

def user_directory_path(instance,filename):
    base_name = os.path.basename(filename)
    name,ext = os.path.splitext(base_name)

    return "note/user/"+ str(instance.note.user.id) + "/"+ str(instance.note.id)+ "/"+"IMG_" + str(instance.note.id)+ext

class Product(models.Model):
    name             = models.CharField(max_length=100)
    price            = models.DecimalField(max_digits= 10, decimal_places=2)
    product_category = models.ForeignKey('ProductCategory', on_delete = models.SET_NULL, null=True)
    uploader         = models.ForeignKey('user.User', on_delete = models.SET_NULL, null=True)
    viewed           = models.IntegerField(null=True)
    address          = models.ForeignKey('user.Address', on_delete = models.SET_NULL, null=True)
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
    image_url  = models.ImageField(upload_to=user_directory_path,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add = True) 
    deleted_at = models.DateTimeField(null = True) 

    class Meta:
        db_table = 'productimages'

class ProductComment(models.Model):
    uploader   = models.ForeignKey('user.User', on_delete = models.SET_NULL, null=True)
    product    = models.ForeignKey('Product', on_delete = models.SET_NULL, null=True)
    content    = models.CharField(max_length=2000)
    created_at = models.DateTimeField(auto_now = True)
    deleted_at = models.DateTimeField(null = True) 
    
    class Meta:
        db_table='productcomments'

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
        
