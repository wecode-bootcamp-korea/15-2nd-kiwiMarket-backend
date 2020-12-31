from django.urls   import path
from product.views import (
    ProductDetailView, 
    ProductListView, 
    SellerItemsView, 
    RelatedProductView, 
    ProductUploadView,
    CommentDetailView,
    CommentUploadView
)

urlpatterns = [path('/detail/<int:product_id>', ProductDetailView.as_view()),
               path('/<int:address_id>', ProductListView.as_view()),
               path('/selleritems/<int:uploader_id>', SellerItemsView.as_view()),
               path('/relateditems/<int:address_id>', RelatedProductView.as_view()),
               path('/productupload/<int:address_id>', ProductUploadView.as_view()),
               path('/comment/<int:product_id>', CommentDetailView.as_view()),
               path('/commentupload/<int:product_id>', CommentUploadView.as_view())
]
