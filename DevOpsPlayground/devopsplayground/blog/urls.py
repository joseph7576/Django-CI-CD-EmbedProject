from django.urls import path

from .apis.post import PostAPI, PostDetailAPI
from .apis.subscription import SubscribeAPI, SubscribeDetailAPI


app_name = "blog"
urlpatterns = [
        path("subscribe/", SubscribeAPI.as_view(), name="subscribe"),
        path("subscribe/<str:email>", SubscribeDetailAPI.as_view(), name="subscribe_detail"),
        path("post/", PostAPI.as_view(), name="post"),
        path("post/<slug:slug>", PostDetailAPI.as_view(), name="post_detail"),
        ]

