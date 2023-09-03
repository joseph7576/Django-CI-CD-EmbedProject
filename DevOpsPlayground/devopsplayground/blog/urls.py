from django.urls import path, include
from devopsplayground.blog.apis.products import ProductAPI

urlpatterns = [
    path("product/", ProductAPI.as_view(), name="product")
]
