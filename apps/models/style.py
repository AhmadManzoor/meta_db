from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.utils.text import slugify
from apps.models.category import StyleCategoryMasterModel, StyleCategorySubModel, BrandCategoryModel
from apps.models.brand import BrandModel
from meta_db.models import (
    AbstractColorSelectedModel,
    AbstractProductInfoStyleSelectedModel,
    ColorModel,
    ProductInfoPatternModel,
    ProductInfoStyleModel,
    ProductInfoSleeveModel,
    AbstractProductModel,
    ColorSelectedModel,
)


class StyleListModelManager(models.Manager):
    @property
    def os(self):
        return super().get_queryset().filter(is_cm=False)

    @property
    def cm(self):
        return super().get_queryset().filter(is_cm=True)


class StyleListModel(models.Model):
    """
    READ ONLY MODEL
    """
    # TODO: go to META
    id = models.CharField(max_length=8,
                          db_column='TBItem_ID',
                          primary_key=True,
                          help_text='primary key / product id')
    group_id = models.CharField(max_length=12,
                                db_column='nVendorBarItem',
                                blank=True,
                                help_text='set bundle')
    brand = models.ForeignKey(BrandModel,
                              db_column='TBVendor_ID',
                              help_text='brand',
                              on_delete=models.DO_NOTHING)
    style_number = models.CharField(max_length=30,
                                    db_column='nVendorStyleNo',
                                    blank=True)
    price = models.DecimalField(decimal_places=2,
                                null=True,
                                max_digits=19,
                                db_column='nPrice2',
                                blank=True,
                                help_text='price per unit')
    _is_sale = models.CharField(max_length=1,
                                db_column='nOnSale',
                                blank=True,
                                help_text='on sale T/F')
    _sale_price = models.DecimalField(decimal_places=2,
                                      null=True,
                                      max_digits=19,
                                      db_column='nSalePrice2',
                                      blank=True,
                                      help_text='sale price')
    picture = models.CharField(max_length=100,
                               db_column='Picture1',
                               blank=True,
                               help_text='picture size 173x217')
    master_category = models.ForeignKey(
        StyleCategoryMasterModel,
        db_column='TBStyleNo_OS_Category_Master_ID',
        blank=True,
        null=True,
        help_text='top category id',
        on_delete=models.DO_NOTHING)
    sub_category = models.ForeignKey(StyleCategorySubModel,
                                     db_column='TBStyleNo_OS_Category_Sub_ID',
                                     blank=True,
                                     null=True,
                                     help_text='sub category id',
                                     on_delete=models.DO_NOTHING)
    brand_category = models.ForeignKey(BrandCategoryModel,
                                       db_column='TBVendorOwnCategory_ID',
                                       blank=True,
                                       null=True,
                                       on_delete=models.DO_NOTHING)
    _is_preorder = models.CharField(max_length=1,
                                    db_column='nPreOrder',
                                    help_text='preorder T/F')
    preorder_available_date = models.DateTimeField(
        null=True,
        db_column='preorder_available_date',
        blank=True,
        help_text='preorder date')
    style_name = models.CharField(max_length=40,
                                  db_column='nStyleName',
                                  blank=True,
                                  help_text='style name using for thumbnail')
    # brand_name = models.CharField(max_length=50, db_column='VDName', blank=False, null=False, help_text='vendor name')
    brand_web_name = models.CharField(max_length=50,
                                      db_column='VDWebName',
                                      blank=False,
                                      null=False,
                                      help_text='vendor name')
    _is_restock = models.CharField(max_length=1,
                                   db_column='nReStock',
                                   blank=True)
    restock_date = models.DateTimeField(null=True,
                                        db_column='nReStockDate',
                                        blank=True)
    is_prevention = models.BooleanField(db_column='copyprevention')
    fulfillment = models.CharField(db_column='ShippedFrom',
                                   max_length=50,
                                   null=True,
                                   blank=True)
    collection_id = models.SmallIntegerField(
        db_column='TBStyleNo_OS_Collection_ID',
        help_text=
        'style collection id. should use TBStyleNo_OS_CollectionSelect table later.'
    )
    description = models.TextField(db_column='nItemDescription', blank=True)
    _is_preorderrestock = models.CharField(max_length=1,
                                           db_column='nPreOrderReStock',
                                           help_text='preorder or restock Y/N')
    created_date = models.DateTimeField(null=True,
                                        db_column='nDate',
                                        blank=True,
                                        help_text='item register date')
    updated_date = models.DateTimeField(null=True,
                                        db_column='nModifyDate',
                                        blank=True,
                                        help_text='item updated date')
    is_cm = models.BooleanField(default=0)
    objects = StyleListModelManager()

    @property
    def brand_name(self):
        return self.brand.name

    @property
    def brand_web_name(self):
        return self.brand.web_name

    @property
    def image(self):
        return '{}/{}'.format(settings.BASE_STYLE_IMAGE_URL, self.picture)

    @property
    def sale_price(self):
        return self._sale_price if self.is_sale and self._sale_price < self.price else self.price

    @property
    def is_plus_size(self):
        return True if self.master_category.id == 9 else False

    @property
    def is_sale(self):
        return True if self._is_sale == 'Y' else False

    @property
    def url(self):
        return '/styles/%s/%s/%s/' % (slugify(
            self.brand_web_name), slugify(self.style_name.lower()), self.id)

    @property
    def is_sale(self):
        return True if self._is_sale == 'Y' else False

    @property
    def is_preorder(self):
        # TODO: remove self._is_restock after removing restock logic
        return True if self._is_preorder == 'Y' or self._is_restock == 'Y' else False

    @property
    def is_restock(self):
        return False

    @property
    def has_available_colors(self):
        return True if ListColorSelectedModel.objects.all_active().filter(
            item__group_id=self.group_id,
            item__brand=self.brand,
            image_link__isnull=False).exclude(
                image_link__exact='').count() >= 2 else False

    def save(self, *args, **kwargs):
        return

    def delete(self, *args, **kwargs):
        return

    class Meta:
        managed = False
        ordering = ['-created_date']
        db_table = 'vTBStyleNoList'  # connect to Views


class ListColorSelectedModel(AbstractColorSelectedModel):
    # TODO: meta db
    item = models.ForeignKey(
        StyleListModel,
        db_column='TBItem_ID',
        related_name='only_colors_for_list',
        help_text=
        'colors only belong to an item. Excluding set bundle or set docking ',
        on_delete=models.DO_NOTHING)
    color = models.ForeignKey(ColorModel, db_column='TBColor_ID', on_delete=models.DO_NOTHING)

    class Meta(AbstractColorSelectedModel.Meta):
        managed = False


class ListProductInfoStyleSelectedModel(AbstractProductInfoStyleSelectedModel):
    # TODO: meta db
    item = models.ForeignKey(StyleListModel,
                             db_column='TBItem_ID',
                             max_length=8,
                             related_name='pi_style_item',
                             on_delete=models.DO_NOTHING)
    style = models.ForeignKey('meta_db.ProductInfoStyleModel',
                              db_column='TBStyleNo_OS_Style_ID',
                              related_name='pi_style',
                              on_delete=models.DO_NOTHING)

    class Meta(AbstractProductInfoStyleSelectedModel.Meta):
        managed = False


class ProductInfoStyleSelectedModel(models.Model):
    id = models.AutoField(db_column='TBStyleNo_OS_StyleSelect_ID',
                          primary_key=True)
    item_id = models.ForeignKey(StyleListModel,
                                db_column='TBItem_ID',
                                max_length=8,
                                related_name='af_style',
                                on_delete=models.DO_NOTHING)
    af_payload = models.ForeignKey(ProductInfoStyleModel,
                                   db_column='TBStyleNo_OS_Style_ID',
                                   blank=True,
                                   null=True,
                                   on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'TBStyleNo_OS_StyleSelect'


class ProductInfoPatternSelectedModel(models.Model):
    id = models.AutoField(db_column='TBStyleNo_OS_PatternSelect_ID',
                          primary_key=True)
    item_id = models.ForeignKey(StyleListModel,
                                db_column='TBItem_ID',
                                max_length=8,
                                related_name='af_pattern',
                                on_delete=models.DO_NOTHING)
    af_payload = models.ForeignKey(ProductInfoPatternModel,
                                   db_column='TBStyleNo_OS_Pattern_ID',
                                   blank=True,
                                   null=True,
                                   on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'TBStyleNo_OS_PatternSelect'


class ProductInfoSleeveSelectedModel(models.Model):
    id = models.AutoField(db_column='TBStyleNo_OS_SleeveSelect_ID',
                          primary_key=True)
    item_id = models.ForeignKey(StyleListModel,
                                db_column='TBItem_ID',
                                max_length=8,
                                related_name='af_sleeve',
                                on_delete=models.DO_NOTHING)
    af_payload = models.ForeignKey(ProductInfoSleeveModel,
                                   db_column='TBStyleNo_OS_Sleeve_ID',
                                   blank=True,
                                   null=True,
                                   on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'TBStyleNo_OS_SleeveSelect'


class ProductModel(AbstractProductModel):
    brand = models.ForeignKey(BrandModel, db_column='TBVendor_ID', on_delete=models.DO_NOTHING)
    brand_category = models.ForeignKey('meta_db.BrandCategoryModel',
                                       db_column='TBVendorOwnCategory_ID',
                                       help_text='brand own categories',
                                       on_delete=models.DO_NOTHING)
    os_category_master = models.ForeignKey(
        'meta_db.StyleCategoryMasterModel',
        db_column='TBStyleNo_OS_Category_Master_ID',
        on_delete=models.DO_NOTHING)
    os_category_sub = models.ForeignKey(
        'meta_db.StyleCategorySubModel',
        db_column='TBStyleNo_OS_Category_Sub_ID',
        on_delete=models.DO_NOTHING)
    os_collection = models.ForeignKey('meta_db.StyleCollectionModel',
                                      db_column='TBStyleNo_OS_Collection_ID',
                                      help_text='os style collection id',
                                      on_delete=models.DO_NOTHING)
    size_chart = models.ForeignKey('meta_db.SizeChartLabelModel',
                                   db_column='TBSizeChart_ID',
                                   on_delete=models.DO_NOTHING)
    pack = models.ForeignKey('meta_db.SizeChartQuantityModel',
                             db_column='TBPackNo_ID',
                             on_delete=models.DO_NOTHING)

    @property
    def grouped_items(self):
        return ProductModel.objects.filter(
            grouped_item_code=self.grouped_item_code, brand=self.brand)

    @property
    def colors(self):
        """
        all related colors including set bundle
        """
        return ColorSelectedModel.objects.all_active().filter(
            item__grouped_item_code=self.grouped_item_code,
            item__brand=self.brand_id)

    @property
    def is_shoes(self):
        return True if self.os_category_master_id == 15 and self.shoe_size.all(
        ) else False

    class Meta(AbstractProductModel.Meta):
        managed = False
