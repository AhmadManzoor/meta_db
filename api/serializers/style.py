from rest_framework import serializers
from apps.models.style import StyleListModel, StyleCategorySubModel


class StyleListSerializer(serializers.ModelSerializer):
    # brand_id
    # category
    # segment
    # style
    # pattern
    # sleeve
    # colors
    # badges
    brand_id = serializers.SerializerMethodField()
    segment = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    sub_category = serializers.SerializerMethodField()
    badges = serializers.SerializerMethodField()
    colors = serializers.SerializerMethodField()
    af_style = serializers.SerializerMethodField()
    af_pattern = serializers.SerializerMethodField()
    af_sleeve = serializers.SerializerMethodField()

    def get_brand_id(self, obj):
        return obj.brand.id

    def get_segment(self, obj):
        return getattr(obj.master_category, 'display_group', '')

    def get_category(self, obj):
        return getattr(obj.master_category, 'name', '')

    def get_sub_category(self, obj):
        try:
            return getattr(obj.sub_category, 'name', '')
        except StyleCategorySubModel.DoesNotExist:
            pass
        return ''

    def get_badges(self, obj):
        tmp = []
        if obj.is_sale:
            tmp.append('sale')
        if obj.is_plus_size:
            tmp.append('plus-size')
        if obj.is_preorder:
            tmp.append('pre-order')
        return tmp

    def get_colors(self, obj):
        return [
            c.color.name for c in obj.only_colors_for_list.filter(
                item__group_id=obj.group_id)
        ]

    def get_af_style(self, obj):
        return [af.af_payload.name for af in obj.af_style.all()]

    def get_af_pattern(self, obj):
        return [af.af_payload.name for af in obj.af_pattern.all()]

    def get_af_sleeve(self, obj):
        return [af.af_payload.name for af in obj.af_sleeve.all()]

    class Meta:
        model = StyleListModel
        fields = [
            'id', 'group_id', 'style_number', 'brand_id', 'brand_name',
            'brand_web_name', 'is_prevention', 'style_name', 'image', 'price',
            'sale_price', 'is_plus_size', 'is_sale', 'created_date',
            'is_preorder', 'preorder_available_date', 'fulfillment', 'url',
            'segment', 'category', 'sub_category', 'badges', 'colors',
            'af_style', 'af_pattern', 'af_sleeve','description','updated_date'
        ]
        read_only_fields = fields
