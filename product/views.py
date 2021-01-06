import json
from django.utils import timezone
import datetime

from django.views     import View
from django.http      import JsonResponse
from django.db.models import Prefetch, Count

from .models import (
    Product,
    ProductImage,
    MainCategory,
    ProductCategory,
    ProductComment,
)

from .forms import ProductFullForm

from user.models import (
    OrderStatus, 
    Address, 
    User, 
    Wishlist, 
    WishCategory
)

from user.utils import login_check

import boto3          
import uuid   


class ProductsView(View):
    @login_check
    def get(self, request):
        address_id = request.GET.get('address_id', None)

        try:
            if Product.objects.filter(address=address_id).exists():
                wishcategories_ins = WishCategory.objects.filter(user=request.user.id, is_liked=True)
                wishcategories     = [item.product_category for item in wishcategories_ins]

                products = Product.objects.filter(address=address_id, product_category__in = wishcategories).prefetch_related(
                    Prefetch('productimage_set', queryset = ProductImage.objects.all(), to_attr='productimage_list'),
                    Prefetch('wishlist_set', queryset = Wishlist.objects.all(), to_attr='wishlist_list'),
                    Prefetch('productcomment_set', queryset = ProductComment.objects.all(), to_attr='comment_list'))
                                                                                        
                result= [{
                    "itemId"           : item.id,
                    "imgSrc"           : item.productimage_list[0].image_url.url, 
                    "title"            : item.name,
                    "townName"         : (item.address.district+' '+item.address.neighborhood),
                    "postedTime"       : item.updated_at.isoformat(),            
                    "price"            : int(item.price),
                    "wishCount"        : len(item.wishlist_list),
                    "commentCount"     : len(item.comment_list),
                    "viewed"           : item.viewed,
                    "order_status"     : item.order_status.name,
                    "seller_id"        : item.uploader.id,

                }for item in products]

                return JsonResponse({"message" : "SUCCESS", "productList" : result}, status = 200)
            return JsonResponse({"message" : "NO_PRODUCT"}, status = 400)
        except ValueError:
            return JsonResponse({'message':'INVALID'}, status = 404)
    @login_check
    def post(self, request):  
        address_id = request.GET.get("address_id", None)
        form = ProductFullForm(request.POST or None, request.FILES or None)
        files = request.FILES.getlist('image')

        if form.is_valid():
            uploader         = User.objects.get(id=request.user.id) 
            name             = form.cleaned_data['name']
            description      = form.cleaned_data['description']
            price            = form.cleaned_data['price']
            access_range     = form.cleaned_data['access_range']
            order_status     = OrderStatus.objects.get(name="판매중")
            product_category = form.cleaned_data["product_category"]
            address          = Address.objects.get(id=address_id)
            product          = Product.objects.create(
                name             = name, 
                price            = price, 
                viewed           = 0, 
                description      = description, 
                access_range     = access_range, 
                created_at       = 0, 
                updated_at       = 0, 
                order_status     = order_status, 
                product_category = product_category, 
                address          = address, 
                uploader         = uploader)
            for file in files:
                ProductImage.objects.create(product=product,image_url=file)
            return JsonResponse({"message" : "SUCCESS"}, status = 200)
        return JsonResponse({"message" : "INVALID_FORM"}, status = 404)
     
class ProductDetailView(View):
    def get(self, request, product_id):

        try:
            if Product.objects.filter(id=product_id).exists():
    
                viewed = Product.objects.get(id=product_id).viewed
                Product.objects.filter(id=product_id).update(viewed=viewed+1)
                products = Product.objects.filter(id=product_id).prefetch_related(
                    Prefetch('productimage_set', queryset = ProductImage.objects.all(), to_attr='productimage_list'),         
                    Prefetch('wishlist_set', queryset = Wishlist.objects.filter(product_id = product_id), to_attr='wishlist_list'), 
                    Prefetch('productcomment_set', queryset = ProductComment.objects.all(), to_attr='comment_list'))   

                result= [{
                    "sellerdata"    : {
                        "seller_profilepic": '사진 데이터가 없음',
                        "seller"           : item.uploader.nickname,
                        "seller_id"        : item.uploader.id,
                        "townName"         : (item.address.district+' '+item.address.neighborhood),
                        "towncode"         : item.address.id,
                        "mannerTemperature": 36.5,                 
                    },
                    "productdetail" : {
                        "imgSrcList"       : [item.productimage_list[num].image_url.url for num in range(0, len(item.productimage_list))],
                        "price"            : int(item.price),
                        "title"            : item.name,    
                        "category"         : item.product_category.name,    
                        "postedTime"       : item.updated_at.isoformat(),          
                        "description"      : item.description,        
                        "wishCount"        : len(item.wishlist_list),
                        "hits"             : item.viewed,
                        "itemId"           : item.id,
                        "order_status"     : item.order_status.name,
                        "commentCount"     : len(item.comment_list),
                        }
                    }for item in products]
                
                return JsonResponse({"message" : "SUCCESS", "itemDetailData" : result}, status = 200)
            return JsonResponse({"message" : "NO_PRODUCT"}, status = 400)
        except ValueError:
            return JsonResponse({'message':'INVALID_VALUE'}, status = 404)

class SellerItemsView(View):
    def get(self, request):
        uploader_id = request.GET.get('uploader_id', None)
        try:
            if Product.objects.filter(uploader_id=uploader_id).exists():
                products = Product.objects.filter(uploader_id=uploader_id).prefetch_related(Prefetch('productimage_set', queryset = ProductImage.objects.all(), to_attr='productimage_list'))   

                result= [{
                    "id"               : item.id,
                    "imgSrc"           : item.productimage_list[0].image_url.url,
                    "title"            : item.name,
                    "price"            : int(item.price),
                    "order_status"     : item.order_status.name,
                    }for item in products]

                return JsonResponse({"message" : "SUCCESS", "sellerItemsData" : result}, status = 200)
            return JsonResponse({"message" : "NO_SELLING_PRODUCT"}, status = 400)
        except ValueError:
            return JsonResponse({'message':'INVALID_VALUE'}, status = 404)

class RelatedProductView(View):
    @login_check
    def get(self, request, address_id):

        wishcategories_ins = WishCategory.objects.filter(user=request.user.id, is_liked=True)
        wishcategories     = [item.product_category for item in wishcategories_ins]

        products = Product.objects.filter(address=address_id, product_category__in=wishcategories).prefetch_related(
            Prefetch('productimage_set', queryset = ProductImage.objects.all(), to_attr='productimage_list'))

        result= [{
            "itemId"           : item.id,
            "imgSrc"           : item.productimage_list[0].image_url, 
            "title"            : item.name,
            "price"            : item.price,
            "order_status"     : item.order_status.name,
            }for item in products]

        return JsonResponse({"message" : "SUCCESS", "sellerItemsData" : result}, status = 200) 

class WishCategoryView(View):
    @login_check
    def get(self, request):
        user = User.objects.get(id=request.user.id)

        wishcategories_list = WishCategory.objects.filter(user=user, is_liked=True)
        result = [item.product_category.id for item in wishcategories_list]
        return JsonResponse({"message" : "SUCCESS", "WishCategory" : result}, status = 200) 
        
    @login_check
    def post(self, request):
        user = User.objects.get(id=2)
        data = json.loads(request.body)
        print(data)

        wishcategories = ProductCategory.objects.filter(id__in = data["category"])        

        [WishCategory.objects.update_or_create(
            user = user,
            product_category = item,
            defaults = {
                'product_category' : item,
                'is_liked'         : True
                }) for item in wishcategories]

        WishCategory.objects.filter(user_id=user.id).exclude(product_category__in=wishcategories).update(is_liked=False)
    
        return JsonResponse({"message" : "SUCCESS"}, status = 200)