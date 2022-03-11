from datetime import datetime, timedelta
from django.conf import settings
from django.utils.text import slugify
from rest_framework import serializers

from meta_db.style.style_list_models import StyleListModel
from meta_db.brand.models import BrandCategoryModel

from apps.models.brand import BrandModel
from apps.models.brand_list_model import BrandListModel




class BrandListSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrandListModel
        fields = (
            'id',
            'name',
            'web_name',

        )
        read_only_fields = fields

