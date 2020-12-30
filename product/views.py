import json

from django.views     import View
from django.http      import JsonResponse

from .models import (
    Product,
    ProductImage,
    MainCategory,
    ProductCategory
)

class ProductListView(View):
    def get(self, request, type):
            category_seq    = request.GET.get('category', None)

            products = Product.objects.filter(Q(category=category_seq) | Q (subcategory=subcategory_seq)).order_by(sort).values()

            result= [{
                "id"            : item["id"],
                "name"          : item["name"],
                "price"         : int(item["price"]),
                "viewed"        :,
                "description"   : item["description"],
                "access_range"  :,
                "created_at"    : item["created_at"],
            }for item in products]

            return JsonResponse({"message" : "SUCCESS", "result" : result}, status = 200)
            
class ProductDetailView(View):
    def get(self, request, product_id):
            if Product.objects.filter(id=product_id).exists():
                products =  Product.objects.filter(id=product_id).values()
                average_star_rating = Review.objects.filter(product_id=product_id).aggregate(Avg('star_rating'))["star_rating__avg"]
                result = [{
                    "id"            : item["id"],
                    "name"          : item["name"],
                    "price"         : int(item["price"]),
                    "star_rating"   : round(average_star_rating, 1),
                    "description"   : item["description"],
                    "category_id"   : item["category_id"],
                    "subcategory_id": item["subcategory_id"],
                    "discount_id"   : item["discount_id"],
                    "image_url"     : item["image_url"],
                    "created_at"    : item["created_at"],
                    "images_slider" : list(ProductImage.objects.filter(product_id = item["id"]).values_list('image_url', flat=True))
                }for item in products]            
                
                return JsonResponse({"result" : result}, status = 200)
            return JsonResponse({"message" : "PRODUCT_DOES_NOT_EXIST"}, status=404)