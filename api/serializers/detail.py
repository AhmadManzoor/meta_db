from ast import Not
from collections import OrderedDict

from django.conf import settings
from rest_framework import serializers

from sugar.address.iso_country_codes import COUNTRY
import logging
from api.serializers.brand import BrandListSimpleSerializer
from apps.models.style_detail_models import StyleModel
from apps.models.brand import BrandAverageOrderReviewModel
from meta_db.style.style_list_models import StyleListPopularModel 


class StyleDetailSerializer(serializers.ModelSerializer):

    product_id =  serializers.SerializerMethodField()
    style_name =  serializers.SerializerMethodField()
    popular_point_7 =  serializers.SerializerMethodField()
    popular_point_14 =  serializers.SerializerMethodField()
    popular_point_30 =  serializers.SerializerMethodField()
    popular_point_60 =  serializers.SerializerMethodField()


    five_star_percentage = serializers.SerializerMethodField()
    four_star_percentage = serializers.SerializerMethodField()
    three_star_percentage = serializers.SerializerMethodField()
    two_star_percentage = serializers.SerializerMethodField()
    one_star_percentage = serializers.SerializerMethodField()


    price = serializers.SerializerMethodField()
    sale_price = serializers.SerializerMethodField()
    created_date =  serializers.SerializerMethodField()
    modified_date =  serializers.SerializerMethodField()

    
    colors = serializers.SerializerMethodField()
    group_id = serializers.SerializerMethodField()
    # badges = serializers.SerializerMethodField()
    style_number = serializers.CharField(source='brand_style_number')
    is_pre_order = serializers.SerializerMethodField()
    is_sale = serializers.SerializerMethodField()
    is_plus_size = serializers.SerializerMethodField()

    brand_id = serializers.SerializerMethodField()
    brand_name = serializers.SerializerMethodField()
    brand_web_name = serializers.SerializerMethodField()

    category = serializers.SerializerMethodField()
    is_restock = serializers.SerializerMethodField()
    restock_date = serializers.SerializerMethodField()
    brand_category = serializers.SerializerMethodField()
    originality = serializers.SerializerMethodField()


    def  get_five_star_percentage(self,obj):
        try :
            branddata= BrandListSimpleSerializer(obj.brand).data
            return BrandAverageOrderReviewModel.objects.get(vendor_id_id =branddata['id']).five_star_percentage
        except Exception as e:
            return 0


    def  get_four_star_percentage(self,obj):
        try :
            branddata= BrandListSimpleSerializer(obj.brand).data
            return BrandAverageOrderReviewModel.objects.get(vendor_id_id =branddata['id']).four_star_percentage
        except Exception as e:
            return 0


    def  get_three_star_percentage(self,obj):

        try :
            branddata= BrandListSimpleSerializer(obj.brand).data
            return BrandAverageOrderReviewModel.objects.get(vendor_id_id =branddata['id']).three_star_percentage
        except Exception as e:
            return 0


    def  get_two_star_percentage(self,obj):
        try :
            branddata= BrandListSimpleSerializer(obj.brand).data
            return BrandAverageOrderReviewModel.objects.get(vendor_id_id =branddata['id']).two_star_percentage
        except Exception as e:
            return 0

            
    def  get_one_star_percentage(self,obj):
        try :
            branddata= BrandListSimpleSerializer(obj.brand).data
            return BrandAverageOrderReviewModel.objects.get(vendor_id_id =branddata['id']).one_star_percentage
        except Exception as e:
            return 0
        

    def get_popular_point_7 (self,obj):
        try:
            return StyleListPopularModel.objects.get(item_id=obj.id).popular_point_7
        except:
            return 0
    def get_popular_point_14 (self,obj):
            try:
                return StyleListPopularModel.objects.get(item_id=obj.id).popular_point_14
            except:
                return 0

    def get_popular_point_30 (self,obj):
            try:
                return StyleListPopularModel.objects.get(item_id=obj.id).popular_point_30
            except:
                return 0
    def get_popular_point_60 (self,obj):
            try:
                return StyleListPopularModel.objects.get(item_id=obj.id).popular_point_7
            except:
                return 0

    def get_product_id(self,obj):
        return obj.id

    def get_style_name(self,obj):
        return obj.style_name

    def get_created_date(self,obj):
        try:
            return str(obj.created)
        except Exception as e:
            return ""

    def get_modified_date(self,obj):
        return str(obj.updated)
        

    def get_price(self, obj):
        # TODO: ref.
        return  float(obj.price)

    def get_sale_price(self, obj):
        return float(obj.sale_price),
        # TODO: ref.


    def get_colors(self, obj):
        try:

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
        except Exception as e:
            return []

    def get_group_id(self, obj):
        try:

            _grouped_items = []
            for _g in obj.grouped_items:
                _grouped_items.append(_g.id)
            return _grouped_items
        except Exception as e:
            return []

    # def get_size_chart(self, obj):
    #     if obj.is_shoes:
    #         _size_chart = []
    #         for s in obj.shoe_size.all():
    #             _size_chart.append({
    #                 'id':
    #                 s.shoe_size.id,
    #                 'name':
    #                 s.shoe_size.name,
    #                 'pack':
    #                 s.shoe_size.shoe_size_chart,
    #                 'size':
    #                 s.shoe_size.shoe_size_chart_label,
    #                 'size_chart':
    #                 OrderedDict(
    #                     zip(s.shoe_size.shoe_size_chart_label,
    #                         s.shoe_size.shoe_size_chart)),
    #                 'description':
    #                 s.shoe_size.description,
    #                 'total':
    #                 sum(s.shoe_size.shoe_size_chart),
    #             })
    #     else:
    #         try:
    #             pack_quantity_list = obj.pack.qty_list
    #         except:
    #             pack_quantity_list = []
    #         try:
    #             size_chart_list = obj.size_chart.size_list
    #         except:
    #             size_chart_list = []

    #         _size_chart = {
    #             'pack': pack_quantity_list,
    #             'size': size_chart_list,
    #             'size_chart':
    #             OrderedDict(zip(size_chart_list, pack_quantity_list)),
    #             'total': sum(pack_quantity_list),
    #         }
    #     return _size_chart

    def get_is_pre_order(self, obj):

        return  obj.is_preorder,

    def get_is_sale(self, obj):
        return  obj.is_sale,

    def get_is_plus_size(self, obj):
        return  obj.is_plus,

    def get_brand_id(self, obj):
        branddata= BrandListSimpleSerializer(obj.brand).data
        return branddata['id']

    def get_brand_name(self, obj):
        try :
            branddata= BrandListSimpleSerializer(obj.brand).data
            if branddata['name'] is not None:
                return branddata['name']
            else :
                return "NOBRANDNAME"
        except :
            return "NOBRANDNAME"

    def get_brand_web_name(self, obj):
        try:
            branddata= BrandListSimpleSerializer(obj.brand).data
            if branddata['web_name'] is not None:
                return branddata['web_name']
            else :
                return "NOBRANDWEBNAME"
        except:
            return "NOBRANDWEBNAME"

    def get_category(self, obj):
        try : 
            return obj.os_category_master.name
        except Exception as e:
            return ""

        

    def get_brand_category(self, obj):
       return  obj.brand_category.name if obj.brand_category.name else "",
               
       

    def get_originality(self, obj):
        return COUNTRY.get(obj.made_in, str())

    def get_is_restock(self, obj):
        return obj.is_restock

    def get_restock_date(self, obj):
        return obj.restock_date

    class Meta:
        fields = (
            'product_id',
            'style_name',
            'style_number',
            'description',
            'is_active',
            'created_date',
            'modified_date',
            'pictures',
            'is_shoes',
            'price',
            'sale_price',
            'colors',
            'is_plus_size',
            'is_sale',
            'is_pre_order',
            'group_id',
            'brand_id',
            'brand_name',
            'brand_web_name',
            'category',
            'brand_category',
            'originality',
            'is_restock',
            'restock_date',
            'is_broken_pack',
            'popular_point_7',
            'popular_point_14',
            'popular_point_30',
            'popular_point_60',
            'five_star_percentage',
            'four_star_percentage',
            'three_star_percentage',
            'two_star_percentage',
            'one_star_percentage'


        )
        model = StyleModel
        read_only_fields = fields

