from django.conf.urls.static import static
from django.conf import settings
from django.urls   import path

from product.views import (
    ProductsView, 
    ProductDetailView,
    SellerItemsView, 
    WishCategoryView
)
urlpatterns = [path('/<int:product_id>', ProductDetailView.as_view()),
               path('', ProductsView.as_view()),
               path('/selleritems', SellerItemsView.as_view()),
               path('/wishcategory', WishCategoryView.as_view())
]
