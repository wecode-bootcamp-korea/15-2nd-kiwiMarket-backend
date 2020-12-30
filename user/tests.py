import json
import datetime
import jwt
from random import randint

from django.test import TestCase, Client

from user.models import User, AuthSms, FullAddress, Address, OrderStatus
from product.models import Product, ProductImage
from my_settings import (
    service_id,
    secretKey,
    AUTH_ACCESS_KEY,
    AUTH_SECRET_KEY,
    SMS_SEND_PHONE_NUMBER,
    SECRET_KEY,
    ALGORITHM
)


class UserTest(TestCase):

    def setUp(self):
        self.client = Client()
        User.objects.create(
            phone_number='01000000000',
            nickname='테식이',
            email='test@naver.com'
        )
        AuthSms.objects.create(
            phone_number='01000000000',
            auth_number = str(randint(100000, 999999))
        )
        AuthSms.objects.create(
            phone_number='01067841882',
            auth_number = str(randint(100000, 999999))
        )
        Address.objects.create(
            code='1111017500',
            longitude='127.018802',
            latitude='37.575979',
            region='서울특별시',
            district='종로구',
            neighborhood='숭인동'
        )
        Address.objects.create(
            code='1129011100',
            longitude='127.007942',
            latitude='37.585059',
            region='서울특별시',
            district='성북구',
            neighborhood='삼선동1가'
        )
        FullAddress.objects.create(
            user_id=User.objects.get(nickname='테식이').id,
            full_address_id=Address.objects.get(code='1111017500').id
        )
        OrderStatus.objects.create(
            name='판매중'
        )
        OrderStatus.objects.create(
            name='거래완료'
        )
        OrderStatus.objects.create(
            name='숨김'
        )
        Product.objects.create(
            name='상품상품',
            price=10000,
            description='설명설명',
            order_status_id=OrderStatus.objects.get(name='판매중').id,
            uploader_id=User.objects.get(nickname='테식이').id
        )
        ProductImage.objects.create(
            product_id=Product.objects.get(name='상품상품').id,
            image_url='https://dnvefa72aowie.cloudfront.net/capri/smb/202012/a80802f0c8ea1c6be4de66c6ff44f809210604961dd5f7604e.jpeg?q=95&s=1440x1440&t=inside'
        )

    def tearDown(self):
        User.objects.all().delete()
        AuthSms.objects.all().delete() 
        FullAddress.objects.all().delete()
        Address.objects.all().delete()
        OrderStatus.objects.all().delete()
        Product.objects.all().delete() 
        ProductImage.objects.all().delete()

    def test_smsverificationview_post_send_sms(self):
        data = {
            'phone_number' : '01067841882'
        }

        response = self.client.post('/user/smscheck', json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'message' : 'SUCCESS'})

    def test_verificationcodeview_post_auth_number_check(self):
        data = {
            'phone_number' : '01067841882',
            'auth_number'  : AuthSms.objects.get(phone_number='01067841882').auth_number
        }

        response = self.client.post('/user/checknum', json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'SIGNUP', 'token': ''})

    def test_checknicknameview_post_nickname_check(self):
        data = {
            'nickname' : '김영이'
        }

        response = self.client.post('/user/checknickname', json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message' : 'SUCCESS'})


    def test_signupview_post_create(self):
        data = {
            'phone_number'    : '01067841882',
            'nickname'        : '김영이',
            'email'           : 'eee@naver.com',
            'address_code'    : '1111017500'
        }

        #self.token = jwt.encode({'id':User.objects.get(nickname='김영이').id}, SECRET_KEY, ALGORITHM)

        response = self.client.post('/user/signup', json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 201)
        #self.assertEqual(response.json(), {'message' : 'SUCCESS', 'token': self.token})

    def test_signinview_post(self):
        UserTest.test_smsverificationview_post_send_sms(self)
        data = {
            'phone_number' : '01000000000',
            'auth_number'  : AuthSms.objects.get(phone_number='01000000000').auth_number
        }

        self.token = jwt.encode({'id':User.objects.latest('id').id}, SECRET_KEY, ALGORITHM)

        response = self.client.post('/user/smscheck', json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'message' : 'SUCCESS'})

    def test_getnearaddressview_get_fulladdress(self):
        headers = {'HTTP_Authorization': jwt.encode({'id':User.objects.get(phone_number='01000000000').id}, SECRET_KEY, ALGORITHM)}
        data = {
            'address_code'  : '1111017500'
        }
        address_code = '1111017500'
        data = Address.objects.filter(code__startswith=address_code)
        near_address_list = [{
            'id'        : near_address.id,
            'code'      : near_address.code,
            'longitude' : str(near_address.longitude),
            'latitude'  : str(near_address.latitude),
            'address'   : near_address.district + ' ' + near_address.neighborhood
        } for near_address in data]

        response = self.client.get(f'/user/getnearaddress/{address_code}', **headers, content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message' : 'SUCCESS', 'near_address_list': near_address_list})

    def test_selectmyaddressview_get_fulladdress(self):
        headers = {'HTTP_Authorization': jwt.encode({'id':User.objects.get(phone_number='01000000000').id}, SECRET_KEY, ALGORITHM)}
        data = FullAddress.objects.select_related('full_address').filter(user_id = User.objects.get(phone_number='01000000000').id)
        address_list = [{
                'id'            : address.full_address.id,
                'user_id'       : address.user_id,
                'address_code'  : address.full_address.code,
                'address_name'  : address.full_address.neighborhood
            } for address in data]

        response = self.client.get('/user/myaddress', **headers, content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message' : 'SUCCESS', 'address_list' : address_list})

    def test_addmyaddressview_post_create_fulladdress(self):
        headers = {'HTTP_Authorization': jwt.encode({'id':User.objects.get(phone_number='01000000000').id}, SECRET_KEY, ALGORITHM)}

        data = {
            'address_code'  : '1129011100'
        }
        
        response = self.client.post('/user/myaddress', json.dumps(data), **headers, content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'message' : 'SUCCESS'})

    def test_deletemyaddressview_delete_fulladdress(self):
        headers = {'HTTP_Authorization': jwt.encode({'id':User.objects.get(phone_number='01000000000').id}, SECRET_KEY, ALGORITHM)}
        data = {
            'address_code'  : '1129011100'
        }
        
        response = self.client.delete('/user/myaddress', json.dumps(data), **headers, content_type='application/json')

        self.assertEqual(response.status_code, 204)
        #self.assertEqual(response.json(), {'message' : 'SUCCESS'})

    def test_userprofileview_get_select_profile(self):
        headers = {'HTTP_Authorization': jwt.encode({'id':User.objects.get(phone_number='01000000000').id}, SECRET_KEY, ALGORITHM)}

        data = User.objects.get(phone_number='01000000000')
        address_data = FullAddress.objects.select_related('full_address').filter(user_id=data.id).first()
        user = {
            'user_id'           : '#'+str(data.id),
            'nickname'          : data.nickname,
            'profile_picture'   : data.profile_picture,
            'address_name'      : address_data.full_address.neighborhood,
            'address_code'      : address_data.full_address.id
        }
        
        response = self.client.get('/user/profile', **headers, content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message' : 'SUCCESS', 'user' : user})

    def test_orderstatusview_get_sales_list(self):
        headers = {'HTTP_Authorization': jwt.encode({'id':User.objects.get(phone_number='01000000000').id}, SECRET_KEY, ALGORITHM)}
        sales_list = [{
                'id'                : item.id,
                'name'              : item.name,
                'address_code'      : item.address_id,
                'address_name'      : item.address.region + ' ' + item.address.district,
                'price'             : item.price,
                'order_status_id'   : item.order_status_id,
                'order_status_name' : item.order_status.name,
                'images'            : list(ProductImage.objects.filter(product_id=item.id).values_list('image_url', flat=True))
            } for item in Product.objects.filter(uploader_id=User.objects.get(phone_number='01000000000').id, order_status_id=1)]

        response = self.client.get('/user/orderstatus?order_status_id=1', **headers, content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message' : 'SUCCESS', 'sales_list': sales_list})

    def test_ChangeOrderStatusView_update_sales_status(self):
        headers = {'HTTP_Authorization': jwt.encode({'id':User.objects.get(id=1).id}, SECRET_KEY, ALGORITHM)}
        data = {
            'order_status_id' : 2
        }
        
        response = self.client.post('/user/changestatus/1', json.dumps(data), **headers, content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message' : 'SUCCESS'})



# if __name__ == '__main__':
#     unittest.main()
