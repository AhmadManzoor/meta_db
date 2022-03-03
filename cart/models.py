from __future__ import unicode_literals

from django.db import models
from meta_db.models import ColorSelectedModel
from meta_db.exceptions import PreventDeleteException, PreventSaveException


class AbstractCartReadOnlyModelManager(models.Manager):
    def all_checkout(self):
        return super(AbstractCartReadOnlyModelManager, self).get_queryset().filter(_is_checkout='Y')

    def all_active(self):
        return super(AbstractCartReadOnlyModelManager, self).get_queryset().filter(_is_active='Y')

    def all_active_and_checkout(self):
        return super(AbstractCartReadOnlyModelManager, self).get_queryset().filter(_is_active='Y', _is_checkout='Y')


class AbstractCartReadOnlyModel(models.Model):
    """
        READY ONLY MODEL
        """
    id = models.AutoField(db_column='TBInvoiceOSSub_ID', primary_key=True)
    description = models.CharField(max_length=3000, db_column='ISDescription', blank=True)
    for_brand_web = models.CharField(db_column='onVendor_ID', max_length=3, blank=True, null=True,
                                     help_text='brand id for vendor own site order')
    price = models.DecimalField(decimal_places=2, max_digits=19,
                                db_column='ISSalePrice', blank=True, null=True,
                                help_text='unit price')
    pack_qty = models.IntegerField(db_column='ISPackageSoo', default=1, help_text='pack qty in cart')
    total_item_qty = models.SmallIntegerField(db_column='ISTotal', blank=True, null=True, help_text='total item number')
    iss1 = models.SmallIntegerField(null=True, db_column='ISs1', blank=True)
    iss2 = models.SmallIntegerField(null=True, db_column='ISs2', blank=True)
    iss3 = models.SmallIntegerField(null=True, db_column='ISs3', blank=True)
    iss4 = models.SmallIntegerField(null=True, db_column='ISs4', blank=True)
    iss5 = models.SmallIntegerField(null=True, db_column='ISs5', blank=True)
    iss6 = models.SmallIntegerField(null=True, db_column='ISs6', blank=True)
    iss7 = models.SmallIntegerField(null=True, db_column='ISs7', blank=True)
    iss8 = models.SmallIntegerField(null=True, db_column='ISs8', blank=True)
    iss9 = models.SmallIntegerField(null=True, db_column='ISs9', blank=True)
    iss10 = models.SmallIntegerField(null=True, db_column='ISs10', blank=True)
    iss11 = models.SmallIntegerField(null=True, db_column='ISs11', blank=True)
    iss12 = models.SmallIntegerField(null=True, db_column='ISs12', blank=True)
    iss13 = models.SmallIntegerField(null=True, db_column='ISs13', blank=True)
    iss14 = models.SmallIntegerField(null=True, db_column='ISs14', blank=True)
    iss15 = models.SmallIntegerField(null=True, db_column='ISs15', blank=True)
    iss16 = models.SmallIntegerField(null=True, db_column='ISs16', blank=True)
    sub_total = models.DecimalField(decimal_places=4, null=True, max_digits=19,
                                    db_column='ISSubTotal', blank=True,
                                    help_text='sub total by item')
    # 'N' save it for later, 'Y' can check out
    _is_checkout = models.TextField(db_column='TBCheckout', default='Y',
                                    help_text='save for later')
    modified_date = models.DateTimeField(db_column='DateTimeModified', auto_now=True)
    # 'N' for sold out
    _is_active = models.CharField(db_column='ISStatus', max_length=1, blank=True,
                                  help_text='active or sold out')
    # does not exist on database. added to convince
    # WEIGHT TO SHIP
    master_unit_weight = models.FloatField(blank=True, null=True)
    master_pack_weight = models.FloatField(blank=True, null=True)
    master_length = models.FloatField(blank=True, null=True)
    master_width = models.FloatField(blank=True, null=True)
    master_height = models.FloatField(blank=True, null=True)
    sub_unit_weight = models.FloatField(blank=True, null=True)
    sub_pack_weight = models.FloatField(blank=True, null=True)
    sub_length = models.FloatField(blank=True, null=True)
    sub_width = models.FloatField(blank=True, null=True)
    sub_height = models.FloatField(blank=True, null=True)
    # oniscustomer = models.CharField(max_length=1, db_column='OnisCustomer', blank=True)
    # groupbuyseries = models.CharField(max_length=1, db_column='GroupBuySeries', blank=True)
    # discountprice = models.DecimalField(decimal_places=4, null=True, max_digits=19,
    #                                     db_column='ISnDiscountPrice', blank=True)
    # tbgroupbuystyleno_id = models.BigIntegerField(null=True, db_column='TBGroupBuyStyleNo_ID', blank=True)
    # groupno_id = models.CharField(max_length=50, db_column='GroupNO_ID', blank=True)
    objects = AbstractCartReadOnlyModelManager()

    @property
    def qty_list(self):
        _fields = ['iss%s' % i for i in range(1, 17)]
        return [getattr(self, i) for i in _fields]

    @property
    def is_checkout(self):
        return True if self._is_checkout == 'Y' else False

    @property
    def is_active(self):
        return True if self._is_active == 'Y' else False

    def save(self, *args, **kwargs):
        raise PreventSaveException('cannot update readonly model')

    def delete(self, *args, **kwargs):
        raise PreventDeleteException('cannot delete readonly model')

    class Meta:
        abstract = True
        db_table = 'vTBInvoiceOSSub'


class CartReadOnlyModel(AbstractCartReadOnlyModel):
    user = models.ForeignKey('meta_db.UserModel', db_column='TBCustomer_ID', related_name='cart_items',
                             to_field='customer_id', on_delete=models.DO_NOTHING)
    item = models.ForeignKey('meta_db.ProductModel', db_column='TBItem_ID', blank=True, null=True, on_delete=models.DO_NOTHING)
    color = models.ForeignKey('meta_db.ColorModel', db_column='TBColor_ID', on_delete=models.DO_NOTHING)
    shoe_size = models.ForeignKey('meta_db.ShoeSizeChartModel', db_column='TBShoeSize_ID', blank=True, null=True, on_delete=models.DO_NOTHING)

    @property
    def available_color_link(self):
        try:
            available_color = ColorSelectedModel.objects.values_list('image_link', flat=True) \
                .filter(item=self.item, color=self.color, image_link__isnull=False).first()
            return available_color
        except ColorSelectedModel.DoesNotExist:
            return None

    class Meta(AbstractCartReadOnlyModel.Meta):
        managed = False


class AbstractCartBaseModel(models.Model):
    """
    Basic Cart model for create/update/delete
    """
    id = models.AutoField(db_column='TBInvoiceOSSub_ID', primary_key=True)
    customer_id = models.CharField(db_column='TBCustomer_ID', max_length=8)
    for_brand_web = models.CharField(db_column='onVendor_ID', max_length=3, blank=True, null=True,
                                     help_text='brand id for vendor own site order')
    item_id = models.CharField(db_column='TBItem_ID', max_length=20)
    color_id = models.CharField(db_column='TBColor_ID', max_length=20)
    shoe_size_id = models.CharField(max_length=20, db_column='TBShoeSize_ID', blank=True, null=True)
    modified_date = models.DateTimeField(db_column='DateTimeModified', auto_now=True)
    pack_qty = models.IntegerField(db_column='ISPackageSoo', default=1, help_text='pack qty in cart')
    _is_checkout = models.TextField(db_column='TBCheckout', default='Y')  # 'N' save it for later, 'Y' can check out

    @property
    def is_checkout(self):
        return True if self._is_checkout == 'Y' else False

    @is_checkout.setter
    def is_checkout(self, value):
        self._is_checkout = 'Y' if value else 'N'

    class Meta:
        abstract = True
        unique_together = (('customer_id', 'item_id', 'color_id', 'shoe_size_id', 'for_brand_web'),)
        db_table = 'TBInvoiceOSSub'


class CartBaseModel(AbstractCartBaseModel):
    class Meta(AbstractCartBaseModel.Meta):
        managed = False
