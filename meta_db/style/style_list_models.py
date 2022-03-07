from __future__ import unicode_literals

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.db import models
from django.utils.text import slugify

from meta_db.style.models import ColorSelectedModel

from meta_db.style_category.models import StyleCategoryMasterModel
from meta_db.style_category.models import StyleCategorySubModel

from apps.models.brand import BrandModel


class StyleListModelManager(models.Manager):
    @property
    def os(self):
        return super().get_queryset().filter(is_cm=False)

    @property
    def cm(self):
        return super().get_queryset().filter(is_cm=True)

    def site(self, request):
        site_type = 'cm' if get_current_site(
            request).domain in settings.CM_SITES else 'os'
        return getattr(self, site_type)


class StyleListModel(models.Model):
    """
    READ ONLY MODEL
    """
    id = models.CharField(max_length=8,
                          db_column=u'TBItem_ID',
                          primary_key=True,
                          help_text=u'primary key / product id')
    grouped_item_code = models.CharField(max_length=12,
                                         db_column='nVendorBarItem',
                                         blank=True,
                                         help_text='set bundle')
    brand = models.ForeignKey(BrandModel,
                              db_column=u'TBVendor_ID',
                              help_text=u'brand',
                              on_delete=models.DO_NOTHING)
    style_number = models.CharField(max_length=30,
                                    db_column=u'nVendorStyleNo',
                                    blank=True)
    our_style_number = models.CharField(max_length=30,
                                        db_column=u'nOurStyleNo',
                                        blank=True)
    price = models.DecimalField(decimal_places=2,
                                null=True,
                                max_digits=19,
                                db_column=u'nPrice2',
                                blank=True,
                                help_text=u'price per unit')
    _is_sale = models.CharField(max_length=1,
                                db_column=u'nOnSale',
                                blank=True,
                                help_text=u'on sale T/F')
    sale_price = models.DecimalField(decimal_places=2,
                                     null=True,
                                     max_digits=19,
                                     db_column=u'nSalePrice2',
                                     blank=True,
                                     help_text=u'sale price')
    created_date = models.DateTimeField(null=True,
                                        db_column=u'nDate',
                                        blank=True,
                                        help_text=u'item register date')
    picture = models.CharField(max_length=100,
                               db_column=u'Picture1',
                               blank=True,
                               help_text=u'picture size 173x217')
    master_category = models.ForeignKey(
        StyleCategoryMasterModel,
        db_column=u'TBStyleNo_OS_Category_Master_ID',
        blank=True,
        null=True,
        help_text=u'top category id',
        on_delete=models.DO_NOTHING)
    sub_category = models.ForeignKey(StyleCategorySubModel,
                                     db_column=u'TBStyleNo_OS_Category_Sub_ID',
                                     blank=True,
                                     null=True,
                                     help_text=u'sub category id',
                                     on_delete=models.DO_NOTHING)
    brand_category = models.ForeignKey('meta_db.BrandCategoryModel',
                                       db_column=u'TBVendorOwnCategory_ID',
                                       blank=True,
                                       null=True,
                                       on_delete=models.DO_NOTHING)
    _is_preorder = models.CharField(max_length=1,
                                    db_column=u'nPreOrder',
                                    help_text=u'preorder T/F')
    preorder_available_date = models.DateTimeField(
        null=True,
        db_column=u'preorder_available_date',
        blank=True,
        help_text=u'preorder date')
    style_name = models.CharField(max_length=40,
                                  db_column=u'nStyleName',
                                  blank=True,
                                  help_text=u'style name using for thumbnail')
    brand_name = models.CharField(max_length=50,
                                  db_column=u'VDName',
                                  blank=False,
                                  null=False,
                                  help_text=u'vendor name')
    brand_web_name = models.CharField(max_length=50,
                                      db_column=u'VDWebName',
                                      blank=False,
                                      null=False,
                                      help_text=u'vendor name')
    _is_restock = models.CharField(max_length=1,
                                   db_column='nReStock',
                                   blank=True)
    restock_date = models.DateTimeField(null=True,
                                        db_column='nReStockDate',
                                        blank=True)
    is_prevention = models.BooleanField(db_column='copyprevention')
    own_style_ordering = models.IntegerField(
        db_column='PageIDX', help_text='brand own ordering style')
    popular_point = models.SmallIntegerField(db_column='popular_point',
                                             help_text='popular point')
    view_point = models.SmallIntegerField(db_column='view_point',
                                          help_text='most viewed')
    sales_point = models.SmallIntegerField(db_column='sales_point',
                                           help_text='most sales')
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
    _is_preorderrestock = models.CharField(
        max_length=1,
        db_column=u'nPreOrderReStock',
        help_text=u'preorder or restock Y/N')
    is_cm = models.BooleanField(default=0)
    _is_hidden = models.CharField(
        db_column='nHidden',
        blank=True,
        max_length=1,
        default='N',
        help_text='sold out and vendor want to hide items. technically deleted.'
    )
    objects = StyleListModelManager()

    @property
    def is_plus(self):
        # return True if self.master_category_id == 9 else False
        try:
            return self.master_category_id == 9
        except:
            return False

    @property
    def is_sale(self):
        return True if self._is_sale == 'Y' else False

    @property
    def absolute_url(self):
        # FIXME: not working. fix me.
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
        return True if ColorSelectedModel.objects.all_active().filter(
            item__grouped_item_code=self.grouped_item_code,
            item__brand=self.brand,
            image_link__isnull=False).exclude(
                image_link__exact='').count() >= 2 else False

    @property
    def os_colors(self):
        try:
            r = ListColorOSSelectedModel.objects.all_active(
            ).only('os_color').filter(
                color__list_color_selected__item_id=self.id,
                color__list_color_selected___is_active='Y').exclude(
                    os_color_id=17).prefetch_related('os_color').distinct()[:8]
            return r
        except Exception as e:
            print("COLOR ERROR: ", e)
        return None

    def save(self, *args, **kwargs):
        return

    def delete(self, *args, **kwargs):
        return

    class Meta:
        managed = False
        ordering = ['-created_date']
        db_table = 'vTBStyleNoList'  # connect to Views


class StyleListPopularModel(models.Model):
    item = models.OneToOneField(StyleListModel,
                                db_column='TBItem_ID',
                                primary_key=True,
                                max_length=8,
                                related_name='popular_styles',
                                on_delete=models.DO_NOTHING)
    popular_point_7 = models.SmallIntegerField(
        db_column='popular_point_7', help_text='popular point of last 7 days')
    popular_point_14 = models.SmallIntegerField(
        db_column='popular_point_14',
        help_text='popular point of last 14 days')
    popular_point_30 = models.SmallIntegerField(
        db_column='popular_point_30',
        help_text='popular point of last 30 days')
    popular_point_60 = models.SmallIntegerField(
        db_column='popular_point_60',
        help_text='popular point of last 60 days')

    class Meta:
        managed = False
        db_table = 'TBStyleNo_Popular'


class PopularItemByStateModel(models.Model):
    item = models.OneToOneField(StyleListModel,
                                db_column='TBItem_ID',
                                primary_key=True,
                                max_length=8,
                                related_name='popular_items',
                                on_delete=models.DO_NOTHING)
    popularity_15 = models.SmallIntegerField(
        db_column='popularity_15', help_text='popular point of last 15 days')
    popularity_30 = models.SmallIntegerField(
        db_column='popularity_30', help_text='popular point of last 30 days')
    ct_state = models.CharField(max_length=2,
                                db_column=u'CTState',
                                help_text=u'buyer state')
    update_time = models.DateTimeField(db_column='update_time', auto_now=True)

    class Meta:
        managed = False
        db_table = 'TBStyleNo_Popular_by_CTState'


#####################################################################
class ListColorSelectedModelManager(models.Manager):
    def all_active(self, **kwargs):
        return super(ListColorSelectedModelManager,
                     self).get_queryset().filter(_is_active='Y', **kwargs)


class ListColorSelectedModel(models.Model):
    """
    READ ONLY MODEL
    """
    id = models.AutoField(db_column='TBColorSelect_ID', primary_key=True)
    item = models.ForeignKey(StyleListModel,
                             db_column='TBItem_ID',
                             max_length=8,
                             related_name='list_color_select',
                             on_delete=models.DO_NOTHING)
    color = models.ForeignKey('meta_db.ColorModel',
                              db_column='TBColor_ID',
                              related_name='list_color_selected',
                              on_delete=models.DO_NOTHING)
    _is_active = models.CharField(max_length=1,
                                  db_column='Active',
                                  default='Y',
                                  help_text='active Y/N')
    image_link = models.CharField(max_length=50,
                                  db_column='ImageLink',
                                  blank=True)
    objects = ListColorSelectedModelManager()

    @property
    def is_active(self):
        return True if self._is_active == 'Y' else False

    @is_active.setter
    def is_active(self, value):
        self._is_active = 'Y' if value else 'N'

    def save(self, *args, **kwargs):
        return

    def delete(self, *args, **kwargs):
        return

    class Meta:
        managed = False
        db_table = 'TBColorSelect'


class ListColorOSSelectManager(models.Manager):
    def all_active(self, **kwargs):
        return super(ListColorOSSelectManager,
                     self).get_queryset().filter(is_active=True, **kwargs)


class ListColorOSSelectedModel(models.Model):
    """
    READ ONLY MODEL
    """
    id = models.AutoField(db_column='IDX', primary_key=True)
    color = models.ForeignKey('meta_db.ColorModel',
                              db_column='TBColor_ID',
                              related_name='list_color_os_select',
                              on_delete=models.DO_NOTHING)
    os_color = models.ForeignKey('meta_db.ColorOSModel',
                                 db_column='TBColorOS_ID',
                                 on_delete=models.DO_NOTHING)
    is_active = models.BooleanField(db_column='nActive')
    objects = ListColorOSSelectManager()

    def save(self, *args, **kwargs):
        return

    def delete(self, *args, **kwargs):
        return

    class Meta:
        managed = False
        db_table = 'TBColorOS_Select'


class ColorOSManager(models.Manager):
    def all_active(self, **kwargs):
        return super(ColorOSManager,
                     self).get_queryset().filter(is_active=True, **kwargs)


class ColorOSModel(models.Model):
    """
    READ ONLY MODEL
    """
    id = models.AutoField(max_length=10,
                          db_column='TBColorOS_ID',
                          primary_key=True)
    name = models.CharField(max_length=50, db_column='osColorName')
    is_active = models.BooleanField(db_column='osColorActive',
                                    default=True,
                                    help_text='T/F')
    objects = ColorOSManager()

    def save(self, *args, **kwargs):
        return

    def delete(self, *args, **kwargs):
        return

    class Meta:
        managed = False
        db_table = 'TBColorOS'
