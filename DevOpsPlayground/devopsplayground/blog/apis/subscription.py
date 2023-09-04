from devopsplayground.api.mixins import ApiAuthMixin
from devopsplayground.blog.models import Subscription
from devopsplayground.api.pagination import LimitOffsetPagination, get_paginated_response
from devopsplayground.blog.selectors.posts import get_subscribers
from devopsplayground.blog.services.post import subscribe, unsubscribe

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, serializers

from drf_spectacular.utils import extend_schema


class SubscribeDetailAPI(ApiAuthMixin, APIView):

    def delete(self, request, email):
        try:
            unsubscribe(user=request.user, email=email)
        except Exception as ex:
            return Response(
                {"detail": "Database Error - " + str(ex)},
                status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_204_NO_CONTENT)


class SubscribeAPI(ApiAuthMixin, APIView):

    class Pagination(LimitOffsetPagination):
        defualt_limit=10

    class InputSubSerializer(serializers.Serializer):
        email = serializers.CharField(max_length=100)

    class OutputSubSerializer(serializers.Serializer):
        email = serializers.SerializerMethodField("get_email")

        class Meta:
            model = Subscription
            fields = ("email",)

        def get_email(self, subscription):
            return subscription.target.email


    @extend_schema(responses=OutputSubSerializer)
    def get(self, request):
        user = request.user
        query = get_subscribers(user=user)

        return get_paginated_response(
            request=request,
            pagination_class=self.Pagination,
            queryset=query,
            serializer_class=self.OutputSubSerializer,
            view=self)

    @extend_schema(request=InputSubSerializer, responses=OutputSubSerializer)
    def post(self, request):
        serializer = self.InputSubSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            query = subscribe(user=request.user, email=serializer.validated_data.get("email"))
        except Exception as ex:
            return Response(
                {"detail": "Database Error - " + str(ex)},
                status=status.HTTP_400_BAD_REQUEST)

        return Response(self.OutputSubSerializer(query).data, status=status.HTTP_201_CREATED)
