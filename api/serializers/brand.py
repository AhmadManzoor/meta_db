from datetime import datetime, timedelta
from django.conf import settings
from django.utils.text import slugify
from rest_framework import serializers

from meta_db.style.style_list_models import StyleListModel
from meta_db.brand.models import BrandCategoryModel

from apps.models.brand import BrandModel
from apps.models.brand_list_model import BrandListModel


# class PopularBrandSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OSPopularBrandModel
#         fields = ('brand', 'brand_name', 'web_name', 'banner_image', 'popularity')
#         read_only_fields = fields


class BrandListSimpleSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    brand_logo = serializers.SerializerMethodField()
    brand_image = serializers.SerializerMethodField()
    newly_joined = serializers.SerializerMethodField()
    brand_score = serializers.SerializerMethodField()

    def get_url(self, obj):
        return '/brands/{}/'.format(obj.web_name)

    def get_brand_logo(self, obj):
        return "%s/%s/%s" % (settings.OS_MEDIA_URL, 'OSFile/OS/banners/vendor', obj.brand_image or "blank.png")

    def get_brand_image(self, obj):
        if obj.brand_image:
            _path = "%s/%s/%s" % (settings.OS_MEDIA_URL, 'OSFile/OS/banners/vendor', obj.brand_image)
        else:
            _path = 'https://os-media-files.s3.amazonaws.com/os.com/mobile/assets/img/no_item_images.gif'
        return _path

    def get_newly_joined(self, obj):
        _since_date = datetime.now() - timedelta(30)
        return True if obj.active_date > _since_date else False

    def get_brand_score(self, obj):
        if obj.average_total_score is None:
            return None
        try:
            return round(obj.average_total_score / 20)
        except AttributeError:
            return None

    class Meta:
        model = BrandListModel
        fields = (
            'id',
            'name',
            'web_name',
            'url',
            'brand_logo',
            'brand_image',
            'newly_joined',
            'brand_score',
        )
        read_only_fields = fields


class BrandSimpleSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    brand_logo = serializers.SerializerMethodField()
    brand_image = serializers.SerializerMethodField()
    newly_joined = serializers.SerializerMethodField()
    brand_score = serializers.SerializerMethodField()

    def get_url(self, obj):
        return '/brands/{}/'.format(obj.web_name)

    def get_brand_logo(self, obj):
        return "%s/%s/%s" % (settings.OS_MEDIA_URL, 'OSFile/OS/banners/vendor', obj.banners.get('banner2')
                             or "blank.png")

    def get_brand_image(self, obj):
        if obj.banners.get('brand'):
            _path = "%s/%s/%s" % (settings.OS_MEDIA_URL, 'OSFile/OS/banners/vendor', obj.banners.get('brand'))
        else:
            _path = 'https://os-media-files.s3.amazonaws.com/os.com/mobile/assets/img/no_item_images.gif'
        return _path

    def get_newly_joined(self, obj):
        _since_date = datetime.now() - timedelta(30)
        return True if obj.joined_date > _since_date else False

    def get_brand_score(self, obj):
        try:
            return round(obj.brand_average_review.average_total_score / 20)
        except AttributeError:
            return None

    class Meta:
        model = BrandModel
        fields = (
            'id',
            'name',
            'web_name',
            'url',
            'brand_logo',
            'brand_image',
            'newly_joined',
            'brand_score',
        )
        read_only_fields = fields


class BrandSerializer(BrandSimpleSerializer):
    fulfillment = serializers.SerializerMethodField()
    contact = serializers.SerializerMethodField()
    information = serializers.SerializerMethodField()
    is_featured_product_sort = serializers.SerializerMethodField()

    def get_fulfillment(self, obj):
        return {
            'id': obj.fulfillment_id,
            'fulfillment': obj.fulfillment.fulfillment,
            'city': obj.fulfillment.city,
            'state': obj.fulfillment.state,
            'min_order_amount': obj.fulfillment.min_order_amt,
            'free_shipping_amt': obj.fulfillment.free_shipping_amt,
        }

    def get_contact(self, obj):
        return dict(
            name=obj.name,
            address="%s %s %s, %s %s" % (obj.address, obj.address2, obj.city, obj.state, obj.zipcode),
            phone=obj.phone,
            fax=obj.fax,
            email=obj.email,
            represent=obj.contact,
        )

    def get_information(self, obj):
        return {
            'price_range': obj.brand_price_range,
            'description': obj.brand_description,
            'store_policy': obj.store_policy,
            'return_policy': obj.return_policy,
            'copy_prevention': obj.copy_prevention,
            'manufacture': obj.manufacture,
            'size_chart_list': obj.size_chart_list,
            'segment': obj.brand_segment,
            'is_paid_home': obj.is_paid_home,
            'seo_title': obj.seo_title if obj.seo_title else '',
            'seo_description': obj.seo_description if obj.seo_description else '',
            'reviews': self._review(obj)
        }

    def get_is_featured_product_sort(self, obj):
        return True if obj.is_featured_product_sort else False

    def _review(self, obj):
        _new_brand = self.get_newly_joined(obj)
        r = obj.brand_review.last()
        return {
            'sold_out_rate': 0 if _new_brand else getattr(r, 'sold_out_rate', 0),
            'avg_shipping_days': 0 if _new_brand else getattr(r, 'avg_shipping_days', 0),
            'backorder_rate': 0 if _new_brand else getattr(r, 'backorder_rate', 0),
            'sold_out_rate_with_unit': getattr(r, 'sold_out_rate_with_unit', 0),
            'avg_shipping_days_with_unit': getattr(r, 'avg_shipping_days_with_unit', 0),
            'backorder_rate_with_unit': getattr(r, 'backorder_rate_with_unit', 0),
            'po_drop_rate_with_unit': getattr(r, 'po_drop_rate_with_unit', 0),
            'po_processing_day_grade': getattr(r, 'po_processing_day_grade', 0),
        }

    class Meta(BrandSimpleSerializer.Meta):
        fields = (
            'id',
            'name',
            'web_name',
            'brand_image',
            'brand_logo',
            'fulfillment',
            'contact',
            'information',
            'url',
            'joined_date',
            'newly_joined',
            'is_featured_product_sort',
        )


# class BrandCategorySerializer(serializers.ModelSerializer):
#     cnt = serializers.SerializerMethodField()
#     url = serializers.SerializerMethodField()

#     def get_cnt(self, obj):
#         return StyleListModel.objects.filter(brand=self.context.get('brand'), brand_category=obj).count()

#     def get_url(self, obj):
#         brand = self.context.get('brand')
#         # TODO: slugify into os meta
#         return '/brands/{}/{}/?bc={}'.format(brand.web_name, slugify(obj.name), obj.id)

#     class Meta:
#         model = BrandCategoryModel
#         fields = ('id', 'name', 'sorting_order', 'cnt', 'url')


# class BrandCustomCategorySerializer(object):
#     @staticmethod
#     def data(brand_category, brand):
#         # fields = ('id', 'name', 'sorting_order', 'cnt', 'url')
#         _dict = {
#             'sale': {},
#             'new-arrivals': {},
#             'all': {},
#         }
#         _base_url = "/brands/%s" % brand.web_name
#         _style = StyleListModel.objects.filter(brand=brand)
#         # new-arrivals
#         _dict['new-arrivals'] = {
#             'id': 'new-arrivals',
#             'name': 'NEW ARRIVALS',
#             'sorting_order': 0,
#             'cnt': _style.filter(created_date__gte=datetime.now() - timedelta(14)).count(),
#             'url': '%s/new-arrivals/' % _base_url,
#         }
#         # new
#         _dict['all'] = {
#             'id': 'all',
#             'name': 'ALL',
#             'sorting_order': 0,
#             'cnt': _style.count(),
#             'url': '%s/all/' % _base_url,
#         }
#         # sale
#         _dict['sale'] = {
#             'id': 'sale',
#             'name': 'SALE',
#             'sorting_order': 0,
#             'cnt': _style.filter(_is_sale='Y').count(),
#             'url': '%s/sale/' % _base_url,
#         }
#         return BrandCustomCategorySerializer._merge(brand_category, _dict)

#     @staticmethod
#     def _merge(brand_category, custom_category):
#         brand_category.insert(0, custom_category.get('new-arrivals'))
#         brand_category.insert(1, custom_category.get('all'))
#         brand_category.append(custom_category.get('sale'))
#         return brand_category
