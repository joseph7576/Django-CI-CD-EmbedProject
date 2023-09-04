from devopsplayground.api.mixins import ApiAuthMixin
from devopsplayground.blog.models import Subscription
from devopsplayground.api.pagination import LimitOffsetPagination

from devopsplayground.blog.services.post import create_post
from devopsplayground.blog.selectors.posts import post_detail, post_list

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, serializers

from drf_spectacular.utils import extend_schema
from devopsplayground.blog.models import Post
from devopsplayground.api.pagination import get_paginated_response, get_paginated_response_context


class PostAPI(ApiAuthMixin, APIView):

    class Pagination(LimitOffsetPagination):
        default_limit = 10

    class FilterSerializer(serializers.Serializer):
        title = serializers.CharField(required=False, max_length=100)
        search = serializers.CharField(required=False, max_length=100)
        created_at__range = serializers.CharField(required=False, max_length=100)
        author__in = serializers.CharField(required=False, max_length=100)
        slug = serializers.CharField(required=False, max_length=100)
        content = serializers.CharField(required=False, max_length=100)

    class InputPostSerializer(serializers.Serializer):
        content = serializers.CharField(max_length=1000)
        title = serializers.CharField(max_length=100)

    class OutputPostSerializer(serializers.ModelSerializer):
        author = serializers.SerializerMethodField("get_author")
        url = serializers.SerializerMethodField("get_url")

        class Meta:
            model = Post
            fields = ("url", "title", "author")

        def get_author(self, post):
            return post.author.username

        def get_url(self, post):
            request = self.context.get("request")
            path = reverse("api:blog:post_detail", args=(post.slug,))
            return request.build_absolute_uri(path)

    @extend_schema(responses=OutputPostSerializer, request=InputPostSerializer)
    def post(self, request):
        serializer = self.InputPostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            query = create_post(
                user=request.user,
                content=serializer.validated_data.get("content"),
                title=serializer.validated_data.get("title"))
        except Exception as ex:
            return Response(
                {"detail": "Database Error - " + str(ex)},
                status=status.HTTP_400_BAD_REQUEST)

        return Response(self.OutputPostSerializer(query, context={"request": request}).data)

    @extend_schema(responses=OutputPostSerializer, parameters=[FilterSerializer])
    def get(self, request):
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)

        try:
            query = post_list(filters=filters_serializer.validated_data, user=request.user)
        except Exception as ex:
            return Response(
                {"detail": "Filter Error - " + str(ex)},
                status=status.HTTP_400_BAD_REQUEST)

        return get_paginated_response_context(
            request=request,
            pagination_class=self.Pagination,
            queryset=query,
            serializer_class=self.OutputPostSerializer,
            view=self)


class PostDetailAPI(ApiAuthMixin, APIView):

    class Pagination(LimitOffsetPagination):
        default_limit = 10

    class OutputPostDetailSerializer(serializers.ModelSerializer):
        author = serializers.SerializerMethodField("get_author")

        class Meta:
            model = Post
            fields = ('author', 'slug', 'title', 'content', 'created_at', 'updated_at')

        def get_author(self, post):
            return post.author.username

    @extend_schema(responses=OutputPostDetailSerializer)
    def get(self, request, slug):
        try:
            query = post_detail(slug=slug, user=request.user)
        except Exception as ex:
            return Response(
                {"detail": "Database Error - " + str(ex)},
                status=status.HTTP_400_BAD_REQUEST)

        return Response(self.OutputPostDetailSerializer(query).data, status=status.HTTP_200_OK)
