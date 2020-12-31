from django.urls   import path
from product.views import (
    ProductsView, 
    ProductDetailView,
    SellerItemsView, 
    WishlistView
)
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [path('/<int:product_id>', ProductDetailView.as_view()),
               path('', ProductsView.as_view()),
               path('/selleritems', SellerItemsView.as_view()),
               path('/wishlist', WishlistView.as_view()),
]
