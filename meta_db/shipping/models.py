from __future__ import unicode_literals

from django.db import models
from meta_db.exceptions import PreventDeleteException


class AbstractBoxSizeModel(models.Model):
    # TODO: depreciated?
    """
    Unit: inch, pound
    """
    size = models.CharField(db_column='size',
                            max_length=10,
                            primary_key=True,
                            help_text='box name')
    length = models.IntegerField(db_column='length')
    width = models.IntegerField(db_column='width')
    height = models.IntegerField(db_column='height')
    min_weight = models.IntegerField(db_column='minweight',
                                     help_text='minimum weight')
    is_active = models.BooleanField(db_column='Active', default=True)

    def delete(self, *args, **kwargs):
        raise PreventDeleteException('cannot delete box')

    class Meta:
        abstract = True
        db_table = 'TBOSCustomBoxSize'


class BoxSizeModel(AbstractBoxSizeModel):
    class Meta(AbstractBoxSizeModel.Meta):
        managed = False


class AbstractShippingMethodModelManager(models.Manager):
    def all_active(self):
        return super(AbstractShippingMethodModelManager,
                     self).get_queryset().filter(_is_active='Y')

    def all_defaults(self):
        return super(AbstractShippingMethodModelManager,
                     self).get_queryset().filter(_is_active='Y',
                                                 is_default=True)


class AbstractShippingMethodModel(models.Model):
    id = models.AutoField(db_column='TBShipMethod_Local_ID', primary_key=True)
    sp_id = models.CharField(db_column='TBShipMethod_ID',
                             max_length=10,
                             unique=True,
                             help_text='WHxx')
    method_name = models.CharField(db_column='SMShipMethodName',
                                   max_length=100)
    description = models.CharField(db_column='SMDescription',
                                   max_length=100,
                                   blank=True,
                                   null=True)
    carrier = models.CharField(db_column='Carrier',
                               null=True,
                               blank=True,
                               max_length=10)
    easypost_description = models.CharField(db_column='EasyPostDescription',
                                            null=True,
                                            blank=True,
                                            max_length=50)
    _is_active = models.CharField(db_column='TActive',
                                  max_length=1,
                                  default='Y')
    ordering = models.SmallIntegerField(db_column='DefaultOrder',
                                        default=0,
                                        blank=True,
                                        null=True,
                                        help_text='ordering')
    is_international = models.BooleanField(db_column='IsInternational',
                                           default=False,
                                           help_text='sp for international')
    is_default = models.BooleanField(db_column='IsDefault',
                                     default=False,
                                     help_text='if brands has no sp')

    objects = AbstractShippingMethodModelManager()

    @property
    def is_active(self):
        return True if self._is_active == 'Y' else False

    @is_active.setter
    def is_active(self, value):
        self._is_active = 'Y' if value else 'N'

    def save(self, *args, **kwargs):
        if not self.pk:
            self.sp_id = 'WH%s' % (ShippingMethodModel.objects.last().id, )
        super(AbstractShippingMethodModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise PreventDeleteException('cannot delete shipping method')

    class Meta:
        abstract = True
        ordering = ['ordering', 'id']
        db_table = 'TBShipMethod'


class ShippingMethodModel(AbstractShippingMethodModel):
    class Meta(AbstractShippingMethodModel.Meta):
        managed = False


class AbstractBrandSelectedShippingMethodModel(models.Model):
    id = models.AutoField(db_column='TBVendorShipMethod_ID', primary_key=True)
    # fulfillment_id = models.IntegerField(db_column='TBShipFrom_ID')
    ordering = models.SmallIntegerField(db_column='Order',
                                        blank=True,
                                        null=True)
    is_international = models.BooleanField(db_column='IsInternational',
                                           default=False)

    class Meta:
        abstract = True
        ordering = ['ordering', 'id']
        db_table = 'TBVendorShipMethod'


class BrandSelectedShippingMethodModel(AbstractBrandSelectedShippingMethodModel
                                       ):
    fulfillment = models.ForeignKey('meta_db.FulfillmentModel',
                                    db_column='TBShipFrom_ID',
                                    related_name='shipping_methods',
                                    on_delete=models.DO_NOTHING)
    ship_method = models.ForeignKey('meta_db.ShippingMethodModel',
                                    db_column='TBShipMethod_ID',
                                    to_field='sp_id',
                                    max_length=10,
                                    on_delete=models.DO_NOTHING)

    class Meta(AbstractBrandSelectedShippingMethodModel.Meta):
        managed = False
