from django.urls import path
from .views import product, productList


urlpatterns = [
    path("products/", productList.ProductsListView.as_view(), name="products"),

    path("product/<str:name>", product.handle, name="product")
]
