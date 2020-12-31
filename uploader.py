import os
import django
import csv
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kiwimarket.settings")
django.setup()

from product.models import MainCategory, ProductCategory, Product, ProductImage
from nearby.models  import NearbyCategory
from user.models    import Address, OrderStatus, User

a1 = MainCategory(name="동네홍보")
a2 = MainCategory(name="중고거래")

MainCategory.objects.bulk_create([a1, a2])

a1 = ProductCategory(name="디지털/가전")
a2 = ProductCategory(name="가구/인테리어")
a3 = ProductCategory(name="유아동/유아도서")
a4 = ProductCategory(name="생활/가공식품")
a5 = ProductCategory(name="스포처/레저")
a6 = ProductCategory(name="여성잡화")
a7 = ProductCategory(name="여성의류")
a8 = ProductCategory(name="남성패션/잡화")
a9 = ProductCategory(name="게임/취미")
a10 = ProductCategory(name="뷰티/미용")
a11 = ProductCategory(name="반려동물용품")
a12 = ProductCategory(name="도서/티켓/음반")
a13 = ProductCategory(name="식물")
a14 = ProductCategory(name="기타 중고물품")
a15 = ProductCategory(name="삽니다")

ProductCategory.objects.bulk_create([a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15])

a1 = NearbyCategory(name="동네 구인구직")
a2 = NearbyCategory(name="과외/클래스")
a3 = NearbyCategory(name="농수산물")
a4 = NearbyCategory(name="부동산")
a5 = NearbyCategory(name="중고차")
a6 = NearbyCategory(name="전시/행사")
a7 = NearbyCategory(name="지역업체 소개")

NearbyCategory.objects.bulk_create([a1, a2, a3, a4, a5, a6, a7])

a1 = OrderStatus(name='판매중')
a2 = OrderStatus(name='거래완료')
a3 = OrderStatus(name='숨김')

OrderStatus.objects.bulk_create([a1, a2, a3])

CSV_PATH = 'data/동중심좌표.csv'
with open(CSV_PATH) as csv_file:
    data_reader = csv.reader(csv_file)
    rows = csv.reader(csv_file, delimiter=',')
    next(rows)
    for row in rows:
        Address.objects.create(code=row[0], longitude=row[5], latitude=row[4], address1=row[1], address2=row[2], address3=row[3])

CSV_PATH = 'data/상품리스트.csv'
with open(CSV_PATH) as csv_file:
    data_reader = csv.reader(csv_file)
    rows = csv.reader(csv_file, delimiter=',')
    next(rows)
    for row in rows:
        order_status_ins = OrderStatus.objects.get(name=row[7])
        product_categroy_ins = ProductCategory.objects.get(name=row[8])
        selling_address_ins = Address.objects.get(code=row[9])
        uploader_ins = User.objects.get(id=row[10])
        Product.objects.create(name=row[0], price=row[1], viewed=row[2], description=row[3], access_range=row[4], created_at=row[5], updated_at=row[6], order_status=order_status_ins, product_category=product_categroy_ins, address = selling_address_ins, uploader = uploader_ins)

CSV_PATH = 'data/상품이미지.csv'
with open(CSV_PATH) as csv_file:
    data_reader = csv.reader(csv_file)
    rows = csv.reader(csv_file, delimiter=',')
    next(rows)
    for row in rows:
        product_ins = Product.objects.get(id=row[0])
        ProductImage.objects.create(product = product_ins, image_url=row[1])


