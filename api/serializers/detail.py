from collections import OrderedDict

from django.conf import settings
from rest_framework import serializers

from sugar.address.iso_country_codes import COUNTRY

from api.serializers.brand import BrandSerializer
from apps.models.style_detail_models import StyleModel


class StyleDetailSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()
    pre_order = serializers.SerializerMethodField()
    colors = serializers.SerializerMethodField()
    size_chart = serializers.SerializerMethodField()
    grouped_items = serializers.SerializerMethodField()
    badges = serializers.SerializerMethodField()
    brand = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    is_restock = serializers.SerializerMethodField()
    restock_date = serializers.SerializerMethodField()
    brand_category = serializers.SerializerMethodField()
    originality = serializers.SerializerMethodField()

    def get_price(self, obj):
        # TODO: ref.
        return {
            'regular_price': obj.price,
            'price': obj.sale_price if obj.is_sale else obj.price,
            'is_sale': obj.is_sale,
            'sale_price': obj.sale_price,
        }

    def get_pre_order(self, obj):
        # TODO: ref.
        return {
            'available_date': obj.preorder_available_date,
            'is_pre_order': obj.is_preorder,
        }

    def get_colors_legacy(self, obj):
        return [{
            'item_id':
            c.item_id,
            'color_id':
            c.color_id,
            'image':
            '{}/{}'.format(settings.BASE_COLOR_SWATCH_URL, c.image_link)
            if c.image_link else None,
            'name':
            c.color.name,
        } for c in obj.colors_distinct]

    def get_colors(self, obj):
        return [{
            'item_id':
            c['item_id'],
            'color_id':
            c['color_id'],
            'image':
            '{}/{}'.format(settings.BASE_COLOR_SWATCH_URL, c['image_link'])
            if c['image_link'] else None,
            'name':
            c['color__name'],
        } for c in obj.colors_distinct]

    def get_grouped_items(self, obj):
        _grouped_items = []
        for _g in obj.grouped_items:
            _shoe_size = None
            if obj.is_shoes:
                _shoe_size = []
                for _s in _g.shoe_size.all():
                    _shoe_size.append({
                        'shoe_size': {
                            'id': _s.shoe_size.id,
                            'name': _s.shoe_size.name,
                            'size': _s.shoe_size.shoe_size_chart_label,
                            'pack': _s.shoe_size.shoe_size_chart,
                        }
                    })
            _grouped_items.append({'id': _g.id, 'shoe_sizes': _shoe_size})
        return _grouped_items

    def get_size_chart(self, obj):
        if obj.is_shoes:
            _size_chart = []
            for s in obj.shoe_size.all():
                _size_chart.append({
                    'id':
                    s.shoe_size.id,
                    'name':
                    s.shoe_size.name,
                    'pack':
                    s.shoe_size.shoe_size_chart,
                    'size':
                    s.shoe_size.shoe_size_chart_label,
                    'size_chart':
                    OrderedDict(
                        zip(s.shoe_size.shoe_size_chart_label,
                            s.shoe_size.shoe_size_chart)),
                    'description':
                    s.shoe_size.description,
                    'total':
                    sum(s.shoe_size.shoe_size_chart),
                })
        else:
            try:
                pack_quantity_list = obj.pack.qty_list
            except:
                pack_quantity_list = []
            try:
                size_chart_list = obj.size_chart.size_list
            except:
                size_chart_list = []

            _size_chart = {
                'pack': pack_quantity_list,
                'size': size_chart_list,
                'size_chart':
                OrderedDict(zip(size_chart_list, pack_quantity_list)),
                'total': sum(pack_quantity_list),
            }
        return _size_chart

    def get_badges(self, obj):
        return {
            'pre_order': obj.is_preorder,
            'sale': obj.is_sale,
            'plus': obj.is_plus,
        }

    def get_brand(self, obj):
        return BrandSerializer(obj.brand).data

    def get_category(self, obj):
        ret_dict = dict(master='', sub='')
        try:
            ret_dict['master'] = {
                'id':
                obj.os_category_master_id,
                'name':
                obj.os_category_master.name,
                'slug_name':
                obj.os_category_master.slug_name,
                'display_group_order':
                obj.os_category_master.display_group_order_id
            }
        except:
            pass

        try:
            ret_dict['sub'] = {
                'name':
                obj.os_category_sub.name if obj.os_category_sub.name else '',
                'slug_name':
                obj.os_category_sub.slug_name
                if obj.os_category_sub.slug_name else ''
            }
        except:
            pass

        return ret_dict

    def get_brand_category(self, obj):
        try:
            brand_category = {
                'id': obj.brand_category_id if obj.brand_category_id else "",
                'name':
                obj.brand_category.name if obj.brand_category.name else ""
            }
        except Exception:
            brand_category = {'id': "", 'name': ""}
        return brand_category

    def get_originality(self, obj):
        return COUNTRY.get(obj.made_in, str())

    def get_is_restock(self, obj):
        return obj.is_restock

    def get_restock_date(self, obj):
        return obj.restock_date

    class Meta:
        fields = (
            'id',
            'style_name',
            'brand_style_number',
            'description',
            'is_active',
            'created',
            'updated',
            'pictures',
            'is_shoes',
            'pre_order',
            'price',
            'colors',
            'size_chart',
            'badges',
            'grouped_items',
            'brand',
            'category',
            'brand_category',
            'originality',
            'is_restock',
            'restock_date',
            'is_broken_pack',
        )
        model = StyleModel
        read_only_fields = fields
