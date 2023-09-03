from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers

from devopsplayground.api.pagination import LimitOffsetPagination
from devopsplayground.blog.models import Product

from devopsplayground.blog.services.products import create_product
from devopsplayground.blog.selectors.products import get_products

from drf_spectacular.utils import extend_schema

class ProductAPI(APIView):

    class Pagination(LimitOffsetPagination):
        default_limit = 15

    class InputSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=255)

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Product
            fields = ("name", "created_at", "updated_at")

    @extend_schema(request=InputSerializer, responses=OutputSerializer)
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            query = create_product(name=serializer.validated_data.get("name"))
        except Exception as ex:
            return Response(
                    f"Database Error {ex}",
                    status=status.HTTP_400_BAD_REQUEST
            )

        return Response(self.OutputSerializer(query, context={"request":request}).data, status=status.HTTP_201_CREATED)

    @extend_schema(responses=OutputSerializer)
    def get(self, request):
        query = get_products()
        return Response(self.OutputSerializer(query, context={"request":request}, many=True).data, status=status.HTTP_200_OK)
