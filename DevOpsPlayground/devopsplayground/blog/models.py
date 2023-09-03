from django.db import models
from devopsplayground.common.models import BaseModel


class Product(BaseModel):
    name = models.TextField(max_length=255)
