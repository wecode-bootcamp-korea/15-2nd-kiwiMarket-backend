import json

from django.views     import View
from django.http      import JsonResponse
from django.db.models import Prefetch

from .models import (
    Product,
    ProductImage,
    MainCategory,
    ProductCategory
)

class ProductListView(View):
    def get(self, request, address_id):
        #wishcategories = Wishcategory.objects.filter(user=request.user)
        #Products = Product.objects.filter(address=address, product_category__in=wishcategories)
        products = Product.objects.filter(address=address_id).prefetch_related(Prefetch('productimage_set', queryset = ProductImage.objects.all(), to_attr='productimage_list'))   

        result= [{
            "itemId"           : item.id,
            "imgSrc"           : item.productimage_list[0].image_url, 
            "title"            : item.name,
            "townName"         : (item.address.address2+' '+item.address.address3),
            "postedTime"       : item.updated_at,            
            "price"            : int(item.price),
            "wishCount"        : 0,
            "commentCount"     : 0,
            "viewed"           : item.viewed,
            "order_status"     : item.order_status.name,
        }for item in products]

        return JsonResponse({"message" : "SUCCESS", "productList" : result}, status = 200)
            
class ProductDetailView(View):
    def get(self, request, product_id):
        products = Product.objects.filter(id=product_id).prefetch_related(Prefetch('productimage_set', queryset = ProductImage.objects.all(), to_attr='productimage_list'))   
        #Product.objects.update(viewed + 1)

        result= {
            "sellerdata"    : [{
                "seller_profilepic": '사진 데이터가 없음',
                "seller"           : item.uploader.nickname,
                "seller_id"        : item.uploader.id,
                "townName"         : (item.address.address2+' '+item.address.address3),
                "towncode"         : item.address.id,
                "mannerTemperature": 36.5,                 
            }for item in products],
            "productdetail" : [{
                "imgSrcList"       : [[item.productimage_list[num].image_url] for num in range(0, len(item.productimage_list))],
                "price"            : int(item.price),
                "title"            : item.name,    
                "category"         : item.product_category.name,    
                "postedTime"       : item.updated_at,          
                "description"      : item.description,        
                # "wishCount"      : s,
                "hits"             : item.viewed,
                "itemId"           : item.id,
                "order_status"     : item.order_status.name,
            }for item in products]
        }
        return JsonResponse({"message" : "SUCCESS", "itemDetailData" : result}, status = 200)

class ProductUploadView(View):
    def post(self, request, address_id):
        data = json.loads(request.body)

        order_status_ins = OrderStatus.objects.get(name=data["order_status"])
        product_categroy_ins = ProductCategory.objects.get(name=data["category"])
        selling_address_ins = Address.objects.get(id=data["address"])
        uploader_ins = User.objects.get(id=1) #데코레이터 적용 전 임시

        Product.objects.create(name=data["title"], price=data["price"], viewed=0, description=data["description"], access_range=data["access_range"], created_at=0, updated_at=0, order_status=order_status_ins, product_category=product_categroy_ins, address = selling_address_ins, uploader = uploader_ins)
        
        product_images_list = []
        for image in data["product_images"]:
            product_images_list.append(ProductImage(product=data["product_id"], image_url=image))
        ProductImage.objects.bulk_create(product_images_list)

        return JsonResponse({"message" : "SUCCESS"}, status = 200)

class CommentDetailView(View):
    def get(self, request, product_id):
        #wishcategories = Wishcategory.objects.filter(user=request.user)
        #Products = Product.objects.filter(address=address, product_category__in=wishcategories)
        comments = ProductComment.objects.filter(product=product_id)
        result= {
            "uploaderdata"    : [{
                "uploader_profilepic": '사진 데이터가 없음',
                "uploader"           : item.uploader.nickname,
                "uploader_id"        : item.uploader.id,
                # "townName"         : (item.address.address2+' '+item.address.address3),
                # "towncode"         : item.address.id,
                "mannerTemperature": 36.5,                 
            }for item in comments],
            "commentdetail" : [{
                "uploader"         : item.uploader,
                "content"          : item.content,
                "postedTime"       : item.updated_at,  
            }for item in comments]
        }

        return JsonResponse({"message" : "SUCCESS", "commentList" : result}, status = 200)

class CommentUploadView(View):
    def post(self, request, product_id):
        data = json.loads(request.body)

        uploader_ins = User.objects.get(id=1) #데코레이터 적용 전 임시
        product_ins = Product.objects.get(id=product_id)

        Product.objects.create(uploader=uploader_ins, product=product_ins, content=data["content"])

        return JsonResponse({"message" : "SUCCESS"}, status = 200)

        
class SellerItemsView(View):
    def get(self, request, uploader_id):
        products = Product.objects.filter(uploader_id=uploader_id).prefetch_related(Prefetch('productimage_set', queryset = ProductImage.objects.all(), to_attr='productimage_list'))   

        result= [{
            "id"               : item.id,
            "imgSrc"           : item.productimage_list[0].image_url, 
            "title"            : item.name,
            "price"            : int(item.price),
            "order_status"     : item.order_status.name,
            }for item in products]

        return JsonResponse({"message" : "SUCCESS", "sellerItemsData" : result}, status = 200)

class RelatedProductView(View):
    def get(self, request, address_id):
        #wishcategories = Wishcategory.objects.filter(user=request.user)
        #Products = Product.objects.filter(address=address, product_category__in=wishcategories)
        products = Product.objects.filter(address=address).prefetch_related(Prefetch('productimage_set', queryset = ProductImage.objects.all(), to_attr='productimage_list'))

        result= [{
            "id"               : item.id,
            "imgSrc"           : item.productimage_list[0].image_url, 
            "title"            : item.name,
            "price"            : item.price,
            "order_status"     : item.order_status.name,
            }for item in products]

        return JsonResponse({"message" : "SUCCESS", "sellerItemsData" : result}, status = 200)        