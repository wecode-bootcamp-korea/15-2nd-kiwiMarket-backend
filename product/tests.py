import json
import bcrypt
import datetime
import io

from .models import (
    Product,
    ProductImage,
    MainCategory,
    ProductCategory,
    ProductComment
)

from user.models import(
    User,
    Address,
    OrderStatus,
    Wishlist
)

from .forms import ProductFullForm

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models               import Prefetch, Count
from django.test                    import TestCase, Client
from django.utils                   import timezone

from freezegun     import freeze_time
from io            import BytesIO
from PIL           import Image
from unittest.mock import MagicMock, Mock

TestCase.maxDiff = None

@freeze_time("2021-01-04T09:26:14.946000+00:00")
class ProductListTest(TestCase):
    def setUp(self):
        a1 = ProductCategory(name="여성의류")
        a1.save()

        a1 = OrderStatus(name='판매중')
        a1.save()

        User.objects.create(
            id           = 1,
            phone_number = '01063510445',
            nickname     = '승연',
            anonymous    = False,
            created_at   = 0000
        )

        Address.objects.create(
            id            = 1817,
            code          = 1129011100,
            longitude     = 127.007942,
            latitude      = 37.585059,
            region        = '서울특별시',
            district      = '성북구',
            neighborhood  = '삼선동1가'
        )

        Product.objects.create(
            id               = 1,
            name             = "멋진 티셔츠 팝니다",
            price            = 10000,
            product_category = ProductCategory.objects.get(name='여성의류'),
            uploader         = User.objects.get(id=1),
            description      = "몇번 안입었어요",
            access_range     = 4,
            address          = Address.objects.get(id=1817),
            order_status     = OrderStatus.objects.get(name='판매중'),
            )

        ProductImage.objects.create(
            id        = 1,
            image_url = "www.lyl.com",
            product   = Product.objects.get(id=1)
        )

        Wishlist.objects.create(
            is_liked = True,
            product  = Product.objects.get(id=1),
            user     = User.objects.get(id=1)
        )

    def tearDown(self):
        ProductCategory.objects.all().delete()
        OrderStatus.objects.all().delete()
        User.objects.all().delete()
        Address.objects.all().delete()
        Product.objects.all().delete()
        ProductImage.objects.all().delete()
        Wishlist.objects.all().delete()

    def test_product_list_get_success(self):
        client   = Client()
        response = client.get('/product?address_id=1817')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "message" : "SUCCESS", 
            "productList" :[
                {'commentCount': 0,
                'imgSrc'       : 'https://kiwimarket-productimages.s3.ap-northeast-2.amazonaws.com/media/www.lyl.com',
                'itemId'       : 1,
                'order_status' : '판매중',
                'postedTime'   : '2021-01-04T09:26:14.946000+00:00',
                'price'        : 10000,
                'title'        : '멋진 티셔츠 팝니다',
                'townName'     : '성북구 삼선동1가',
                'viewed'       : None,
                'wishCount'    : 1
                }]})

    def test_product_list_get_fail(self):
        client   = Client()
        response = client.get('/product?address_id=1')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            "message" : "NO_PRODUCT"
            })
        
@freeze_time("2021-01-04T09:26:14.946000+00:00")
class ProductDetailTest(TestCase):
    def setUp(self):
        a1 = ProductCategory(name="여성의류")
        a1.save()

        a1 = OrderStatus(name='판매중')
        a1.save()

        User.objects.create(
            id           = 1,
            phone_number = '01063510445',
            nickname     = '승연',
            anonymous    = False,
            created_at   = 0000
        )

        Address.objects.create(
            id            = 1817,
            code          = 1129011100,
            longitude     = 127.007942,
            latitude      = 37.585059,
            region        = '서울특별시',
            district      = '성북구',
            neighborhood  = '삼선동1가'
        )

        Product.objects.create(
            id               = 1,
            name             = "멋진 티셔츠 팝니다",
            price            = 10000,
            product_category = ProductCategory.objects.get(name='여성의류'),
            uploader         = User.objects.get(id=1),
            description      = "몇번 안입었어요",
            access_range     = 4,
            address          = Address.objects.get(id=1817),
            order_status     = OrderStatus.objects.get(name='판매중'),
            viewed           = 3,
        )

        ProductImage.objects.create(
            id        = 1,
            image_url = "www.lyl.com",
            product   = Product.objects.get(id=1)
        )

        Wishlist.objects.create(
            is_liked = True,
            product  = Product.objects.get(id=1),
            user     = User.objects.get(id=1)
        )

    def tearDown(self):
        ProductCategory.objects.all().delete()
        OrderStatus.objects.all().delete()
        User.objects.all().delete()
        Address.objects.all().delete()
        Product.objects.all().delete()
        ProductImage.objects.all().delete()
        Wishlist.objects.all().delete()

    def test_product_detail_get_success(self):
        client   = Client()
        response = client.get('/product/detail?product_id=1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "message" : "SUCCESS", 
            "itemDetailData" : 
            [{'productdetail': 
                {'category'    : '여성의류',
                'commentCount' : 0,
                'description'  : '몇번 안입었어요',
                'hits'         : 4,
                'imgSrcList'   : ['https://kiwimarket-productimages.s3.ap-northeast-2.amazonaws.com/media/www.lyl.com'],
                'itemId'       : 1,
                'order_status' : '판매중',
                'postedTime'   : '2021-01-04T09:26:14.946000+00:00',
                'price'        : 10000,
                'title'        : '멋진 티셔츠 팝니다',
                'wishCount'    : 1},
            'sellerdata': 
                {'mannerTemperature': 36.5,
                'seller'            : '승연',
                'seller_id'         : 1,
                'seller_profilepic' : '사진 데이터가 없음',
                'townName'          : '성북구 삼선동1가',
                'towncode'          : 1817}}]
                })

    def test_product_detail_get_fail(self):
        client   = Client()
        response = client.get('/product/detail?product_id=2')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            "message" : "NO_PRODUCT"
            })

class ProductUploadTest(TestCase):

    def setUp(self):

        User.objects.create(
            id           = 2,
            phone_number = '01063510445',
            nickname     = '승연',
            anonymous    = False,
            created_at   = 0000
        )   

        a1 = ProductCategory(name="여성의류")
        a1.save()

        a1 = OrderStatus(name='판매중')
        a1.save()

        Address.objects.create(
            id            = 1817,
            code          = 1129011100,
            longitude     = 127.007942,
            latitude      = 37.585059,
            region        = '서울특별시',
            district      = '성북구',
            neighborhood  = '삼선동1가'
        )               

    def test_product_upload_post_success(self):
        client = Client()

        def generate_photo_file(self):
            file = io.BytesIO()
            image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
            image.save(file, 'png')
            file.name = 'test.png'
            file.seek(0)
            return file        

        form_data = {
            "name"                 : "책 팔아요",
            "description"          : "사놓고 한번도 안읽었어요",
            "price"                : 200000,
            "access_range"         : 1,
            "product_category_ins" : 12
            }                                               
        image_data = {   
                'image' : generate_photo_file(self) 
            }    

        form = ProductFullForm(data=form_data, files=image_data) 
        form_response = {'form' : form}
        response = client.post('/product/productwrite?address_id=1817', form_response, content_type='multipart')      
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "message" : "SUCCESS"
            })

    def test_product_upload_post_fail(self):
        client = Client()

        form_data = {
            "name"                 : "책 팔아요",
            "description"          : "사놓고 한번도 안읽었어요",
            "price"                : 200000,
            "access_range"         : 1,
            "product_category_ins" : 12,
            }                                               
        image_data = {   
                'image' : '' 
            }    

        form = ProductFullForm(data=form_data, files=image_data) 
        form_response = {'form' : form}
        response = client.post('/product/productwrite?address_id=1817', form_response, content_type='text/html')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {
            "message" : "INVALID_FORM"
            })

class SellerItemsTest(TestCase):
    def setUp(self):
        a1 = ProductCategory(name="여성의류")
        a1.save()
        a2 = ProductCategory(name="게임/취미")
        a2.save()

        a1 = OrderStatus(name='판매중')
        a1.save()

        User.objects.create(
            id           = 1,
            phone_number = '01063510445',
            nickname     = '승연',
            anonymous    = False,
            created_at   = 0000
        )

        Address.objects.create(
            id            = 1817,
            code          = 1129011100,
            longitude     = 127.007942,
            latitude      = 37.585059,
            region        = '서울특별시',
            district      = '성북구',
            neighborhood  = '삼선동1가'
        )

        Product.objects.create(
            id               = 1,
            name             = "멋진 티셔츠 팝니다",
            price            = 10000,
            product_category = ProductCategory.objects.get(name='여성의류'),
            uploader         = User.objects.get(id=1),
            description      = "몇번 안입었어요",
            access_range     = 4,
            address          = Address.objects.get(id=1817),
            order_status     = OrderStatus.objects.get(name='판매중'),
            )

        Product.objects.create(
            id               = 2,
            name             = "두뇌능력 향상 보드게임",
            price            = 10000,
            product_category = ProductCategory.objects.get(name='게임/취미'),
            uploader         = User.objects.get(id=1),
            description      = "딸아이가 좋아했던 보드게임입니다.",
            access_range     = 4,
            address          = Address.objects.get(id=1817),
            order_status     = OrderStatus.objects.get(name='판매중'),
            )

        ProductImage.objects.create(
            id        = 1,
            image_url = "www.lyl.com",
            product   = Product.objects.get(id=1)
        )

        ProductImage.objects.create(
            id        = 2,
            image_url = "www.lyl.com",
            product   = Product.objects.get(id=2)
        )

        Wishlist.objects.create(
            is_liked = True,
            product  = Product.objects.get(id=1),
            user     = User.objects.get(id=1)
        )

    def tearDown(self):
        ProductCategory.objects.all().delete()
        OrderStatus.objects.all().delete()
        User.objects.all().delete()
        Address.objects.all().delete()
        Product.objects.all().delete()
        ProductImage.objects.all().delete()
        Wishlist.objects.all().delete()

    def test_seller_items_list_get_success(self):
        client   = Client()
        response = client.get('/product/selleritems?seller_id=1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "message" : "SUCCESS", 
            "sellerItemsData" : [
            {
            "id"           : 1,
            "imgSrc"       : "https://kiwimarket-productimages.s3.ap-northeast-2.amazonaws.com/media/www.lyl.com",
            "title"        : "멋진 티셔츠 팝니다",
            "price"        : 10000,
            "order_status" : '판매중'
            },
            {
            "id"           : 2,
            "imgSrc"       : "https://kiwimarket-productimages.s3.ap-northeast-2.amazonaws.com/media/www.lyl.com",
            "title"        : "두뇌능력 향상 보드게임",
            "price"        : 10000,
            "order_status" : '판매중'
            }]})

    def test_seller_items_list_get_fail(self):
        client   = Client()
        response = client.get('/product/selleritems?seller_id=2')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            "message" : "NO_SELLING_PRODUCT"
            })

