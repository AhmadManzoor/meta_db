from __future__ import unicode_literals

from datetime import datetime

from django.db import models, IntegrityError
from meta_db.models import ColorSelectedModel
from meta_db.exceptions import PreventDeleteException
from meta_db.invoice.abstract_invoice_meta_models import AbstractMetaMasterInvoiceModel


##################
# INVOICE MASTER #
##################


class AbstractMasterInvoiceModel(AbstractMetaMasterInvoiceModel):
    # because of db_column name
    id = models.AutoField(db_column='TBInvoiceMaster_SQL_ID', primary_key=True)
    ordered_date = models.DateTimeField(db_column='IMOrderDate', auto_now_add=True)
    order_amount = models.DecimalField(decimal_places=4, null=True, max_digits=19, db_column='IMOrderAmt', blank=True,
                                       default=0.00)
    os_commission = models.FloatField(db_column='IMOSCommission', blank=True, null=False, default=0.0,
                                      help_text='OS Commission Rate')
    merchant_fee = models.FloatField(db_column='IMMerchantFee', blank=True, null=False, default=0.0,
                                     help_text='Credit Card & Paypal Fee Rate')
    invoice_star = models.SmallIntegerField(db_column='InvoiceRating', blank=True, null=True)
    store_credit = models.DecimalField(decimal_places=4, null=True, max_digits=19, db_column='IMStoreCredit',
                                       blank=True, default=0.00, help_text='used store credit')
    sub_total_amount = models.DecimalField(decimal_places=4, null=True, max_digits=19, db_column='IMSubTotal',
                                           blank=True, default=0.00, help_text='sum of order price')

    # Invoice Only Fields
    invoice_master_id = models.CharField(max_length=10, db_column='TBInvoiceMaster_ID', unique=True)
    is_captured = models.BooleanField(null=True,db_column='IMCaptured', default=0)
    is_declined = models.BooleanField(db_column='IMDeclined', default=0)
    is_shipped = models.BooleanField(null=True,db_column='IMComplete_Shipping', default=False,
                                         help_text='is this shipped out')
    actual_shipping_date = models.DateTimeField(db_column='IMActualShippingDate', blank=True, null=True, )
    for_brand_web = models.CharField(max_length=3, db_column='onVendor_ID', blank=True, null=True, help_text='for vendor own site order')
    authorized_response_code = models.CharField(max_length=2, db_column='AuthResponseCode', blank=True, null=True)
    authorized_response_reason_code = models.CharField(max_length=10, db_column='AuthResponseReasonCode',
                                                       help_text='authorized.net response code', blank=True)
    authorized_response = models.CharField(max_length=1000, db_column='AuthResponseResonText',
                                           help_text='authorized.net response result message', blank=True)
    authorized_code = models.CharField(max_length=100, db_column='AuthApprovalCode', blank=True)
    authorized_trans_id = models.CharField(max_length=100, db_column='AuthTransID', blank=True, null=True)
    authorized_amount = models.DecimalField(decimal_places=4, null=True, max_digits=19, db_column='IMAuthorizedAmt',
                                            blank=True, default=0.00)
    captured_amount = models.DecimalField(decimal_places=4, null=True, max_digits=19, db_column='IMCapturedAmt',
                                          blank=True, default=0.00)
    captured_trans_id = models.CharField(max_length=100, db_column='CaptureTransID', blank=True, null=True,
                                         help_text='captured transaction id')
    paid_amount = models.DecimalField(decimal_places=4, null=True, max_digits=19, db_column='IMPaidAmt', blank=True,
                                      default=0.00)
    authorized_date = models.DateTimeField(null=True, db_column='IMAuthorizedDate', blank=True)
    captured_user = models.CharField(max_length=50, db_column='CapturedUser', blank=True, null=True)
    captured_date = models.DateTimeField(db_column='CapturedDate', blank=True, null=True)
    balance_amount = models.DecimalField(decimal_places=4, null=True, max_digits=19, db_column='IMBalance', blank=True,
                                         default=0.00, help_text='remain balance. due amount - payed amount')
    confirmed_date = models.DateTimeField(null=True, db_column='IMConfirmedDate', blank=True)
    created_date = models.DateTimeField(null=True, db_column='IMInputDateAndTime', blank=True, auto_now_add=True)
    discount_amount = models.DecimalField(decimal_places=4, null=True, max_digits=19,
                                          db_column='DiscountedAmount', default=0.00, help_text='discount amount')
    due_amount = models.DecimalField(decimal_places=4, null=True, max_digits=19, db_column='IMDueAmt', blank=True,
                                     default=0.00, help_text='final charged price')
    shipping_fee = models.DecimalField(decimal_places=4, null=True, max_digits=19, db_column='IMInvoiceFChg',
                                       blank=True, default=0.00, help_text='shipping fee')
    handling_fee = models.DecimalField(decimal_places=4, null=True, max_digits=19, db_column='IMInvoiceHFee',
                                       blank=True, default=0.00, help_text='handling fee')
    shipped_date = models.DateTimeField(db_column='IMShippingDate', blank=True, null=True)
    shipping_tracking_number = models.CharField(max_length=60, db_column='ShippingTrackingNo', blank=True,
                                                help_text='shipping tracking number')

    # TODO remove blow code after developing admin site. Redundant codes to match legacy order invoice
    po_number = models.CharField(db_column='IMPONumber', max_length=20, blank=True, null=True, help_text='COD NUMBER')
    _ara_add = models.CharField(max_length=1, db_column='TAdd', blank=True, default='N', help_text='for ARA')
    _ara_update = models.CharField(max_length=1, db_column='TUpdate', blank=True, default='N', help_text='for ARA')
    afconfirm = models.CharField(max_length=1, db_column='AFConfirm', blank=True, default='N', help_text='unknown')
    amount_discount = models.IntegerField(db_column='AmountDiscount', null=True, blank=True, default=0)
    amount_discount_percentage = models.IntegerField(null=True, db_column='AmountDiscountPercentage',
                                                     blank=True, default=0)
    estimate_sp_fee = models.DecimalField(decimal_places=4, null=True, max_digits=19, db_column='IMInvoiceEstimatedSPF',
                                          blank=True, default=0.00, help_text=u'estimated shipping fee')
    estimate_sp_weight = models.FloatField(help_text='estimated shipping weight', db_column='IMInvoiceEstimatedSPW',
                                           default=0.00, blank=True, null=True)
    card_ccv = models.CharField(max_length=255, db_column='CardSecurityCode', blank=True)

    @property
    def ara_add(self):
        return True if self._ara_add == 'Y' else False

    @ara_add.setter
    def ara_add(self, value):
        self._ara_add = 'Y' if value else 'N'

    @property
    def ara_update(self):
        return True if self._ara_update else False

    @ara_update.setter
    def ara_update(self, value):
        self._ara_update = 'Y' if value else 'N'

    def save(self, *args, **kwargs):
        """
        paid amount != captured amount BECAUSE OF PAYPAL
        """
        if not self.pk:
            self.invoice_master_id = _get_unique_invoice_id(self)

        # adjust numbers
        self.sub_total_amount = self.order_amount + self.shipping_fee + self.handling_fee
        self.due_amount = self.sub_total_amount - self.store_credit - self.discount_amount
        self.balance_amount = self.due_amount - self.paid_amount
        try:
            super(AbstractMasterInvoiceModel, self).save(*args, **kwargs)
        except IntegrityError as e:
            # TODO: log here
            if not self.pk and hasattr(e, 'args') and 'The duplicate key value' in e.args[-1]:
                self.save(*args, **kwargs)
            else:
                raise e

    def delete(self, *args, **kwargs):
        raise PreventDeleteException('cannot delete master invoice')

    class Meta(AbstractMetaMasterInvoiceModel.Meta):
        abstract = True
        get_latest_by = 'id'
        db_table = 'TBInvoiceMaster'


class MasterInvoiceModel(AbstractMasterInvoiceModel):
    user = models.ForeignKey('meta_db.UserModel', db_column='TBCustomer_ID', to_field='customer_id',
                             related_name='master_invoice', on_delete=models.DO_NOTHING)
    shipping_method = models.ForeignKey('meta_db.ShippingMethodModel', db_column='TBShipMethod_ID', to_field='sp_id', on_delete=models.DO_NOTHING)
    # TODO: update payment_method not sql id. authorized.net id -- ?
    payment_method = models.ForeignKey('meta_db.PaymentMethodModel', db_column='TBSaleMethod_ID', help_text='FK. payment method id. Table = TBSaleMethod', on_delete=models.DO_NOTHING)
    invoice_status = models.ForeignKey('meta_db.MasterInvoiceStatusModel', db_column='IMStatus', help_text='order status', on_delete=models.DO_NOTHING)
    fulfilled_by = models.ForeignKey('meta_db.FulfillmentModel', db_column='ShippedFrom', to_field='fulfillment', blank=True, null=True, on_delete=models.DO_NOTHING)

    @property
    def payment_method_alias(self):
        """
        Credit Card: WH1
        Paypal: WH20
        COD: WH22 - disabled
        WIRE: WH21
        """
        if self.payment_method.id == 'WH1':
            return 'credit_card'
        elif self.payment_method.id == 'WH20':
            return 'paypal'
        elif self.payment_method.id == 'WH22':
            return 'cod'
        elif self.payment_method.id == 'WH21':
            return 'wire'
        return

    @property
    def is_preorder(self):
        return True if self.invoice_status.id in (9, 10, 11, 12) else False

    @property
    def is_brand_fulfillment(self):
        return False if self.fulfilled_by.fulfillment in ('OrangeShine.com', 'OS SHOES') else True

    class Meta(AbstractMasterInvoiceModel.Meta):
        managed = False


class AbstractSubInvoiceModel(models.Model):
    id = models.AutoField(db_column='TBInvoiceSub_SQL_ID', primary_key=True)
    line_id = models.CharField(max_length=10, db_column='TBInvoiceSub_ID', unique=True)
    description = models.CharField(max_length=3000, db_column='ISDescription', blank=True)
    purchase_price = models.DecimalField(decimal_places=4, null=True, max_digits=19,
                                         db_column='ISPurchasePrice', blank=True)
    retail_price = models.DecimalField(decimal_places=4, null=True, max_digits=19,
                                       db_column='ISSalePrice', blank=True, help_text='retail price')
    discount_price = models.DecimalField(decimal_places=4, null=True, max_digits=19,
                                         db_column='ISnDiscountPrice', blank=True, default=0.0)
    package_qty = models.IntegerField(null=True, db_column='ISPackageSoo', blank=True)
    iss1 = models.SmallIntegerField(null=True, db_column='ISs1', default=0)
    iss2 = models.SmallIntegerField(null=True, db_column='ISs2', default=0)
    iss3 = models.SmallIntegerField(null=True, db_column='ISs3', default=0)
    iss4 = models.SmallIntegerField(null=True, db_column='ISs4', default=0)
    iss5 = models.SmallIntegerField(null=True, db_column='ISs5', default=0)
    iss6 = models.SmallIntegerField(null=True, db_column='ISs6', default=0)
    iss7 = models.SmallIntegerField(null=True, db_column='ISs7', default=0)
    iss8 = models.SmallIntegerField(null=True, db_column='ISs8', default=0)
    iss9 = models.SmallIntegerField(null=True, db_column='ISs9', default=0)
    iss10 = models.SmallIntegerField(null=True, db_column='ISs10', default=0)
    iss11 = models.SmallIntegerField(null=True, db_column='ISs11', default=0)
    iss12 = models.SmallIntegerField(null=True, db_column='ISs12', default=0)
    iss13 = models.SmallIntegerField(null=True, db_column='ISs13', default=0)
    iss14 = models.SmallIntegerField(null=True, db_column='ISs14', default=0)
    iss15 = models.SmallIntegerField(null=True, db_column='ISs15', default=0)
    iss16 = models.SmallIntegerField(null=True, db_column='ISs16', default=0)
    total_item_qty = models.SmallIntegerField(null=True, db_column='ISTotal', blank=True)
    sub_total = models.DecimalField(db_column='ISSubTotal', decimal_places=4, max_digits=19)
    stock_state = models.CharField(max_length=10, db_column='TInstockOrSoldout', blank=True,
                                   default="I", help_text='I: in-stock, S: sold out')
    # TODO: depreciated: delete later
    _is_preorder = models.CharField(max_length=1, db_column='nPreOrder', help_text='Y/N', default='N')
    preorder_available_date = models.DateTimeField(db_column='nPreOrderAvailableDate', blank=True, null=True)
    _ara_add = models.CharField(max_length=1, db_column='TAdd', default='Y')
    _ara_update = models.CharField(max_length=1, db_column='TUpdate', default='N')
    # regular_price = models.DecimalField(db_column='ISRegularPrice', decimal_places=4, max_digits=19, default=0.00)
    # restock_date = models.DateTimeField(null=True, db_column='Requested_Restock_Date', blank=True)
    # shipping_fee = models.DecimalField(decimal_places=4, null=True, max_digits=19,
    #                                    db_column='ShippingFee', blank=True)
    # shipping_tracking = models.CharField(max_length=50, db_column='ShippingTracking', blank=True, null=True)
    # shoe_size_id_requested = models.BigIntegerField(db_column='TBShoeSize_ID_Requested', blank=True, null=True)
    # free_shipping_amt = models.DecimalField(decimal_places=4, null=True, max_digits=19,
    #                                         db_column='ISnFreeShippingAmt', blank=True)
    # groupbuyseries = models.CharField(max_length=1, db_column='GroupBuySeries', blank=True, default='N')
    # oniscustomer = models.CharField(max_length=1, db_column='OnisCustomer', blank=True, default='N')
    # tbgroupbuystyleno_id = models.BigIntegerField(null=True, db_column='TBGroupBuyStyleNo_ID', blank=True)
    # brandinvno = models.CharField(max_length=50, db_column='BrandInvNO', blank=True, null=True)

    @property
    def qty_list(self):
        _fields = ['iss%s' % i for i in range(1, 17)]
        return [getattr(self, i) for i in _fields]

    @qty_list.setter
    def qty_list(self, values):
        _fields = ['iss%s' % i for i in range(1, 17)]
        for f, v in zip(_fields, values):
            setattr(self, f, v)

    @property
    def pack_price(self):
        return self.total_item_qty * self.retail_price

    @property
    def size_chart(self):
        return [getattr(self, 'iss%s' % s) for s in range(1, 17)]

    @size_chart.setter
    def size_chart(self, val):
        for s in range(1, len(val)+1):
            setattr(self, 'iss%s' % s, val[s-1])

    @property
    def ara_add(self):
        return True if self._ara_add == 'Y' else False

    @ara_add.setter
    def ara_add(self, value):
        self._ara_add = 'Y' if value else 'N'

    @property
    def ara_update(self):
        return True if self._ara_update else False

    @ara_update.setter
    def ara_update(self, value):
        self._ara_update = 'Y' if value else 'N'

    @property
    def is_preorder(self):
        return True if self._is_preorder == 'Y' else False

    @is_preorder.setter
    def is_preorder(self, val):
        self._is_preorder = 'Y' if val else 'N'

    def delete(self, *args, **kwargs):
        raise PreventDeleteException('cannot delete sub invoice')

    class Meta:
        abstract = True
        get_latest_by = 'id'
        db_table = 'TBInvoiceSub'


class SubInvoiceModel(AbstractSubInvoiceModel):
    master_order = models.ForeignKey('MasterInvoiceModel', db_column='TBInvoiceMaster_ID', to_field='invoice_master_id', related_name='sub_invoices', on_delete=models.DO_NOTHING)
    item = models.ForeignKey('meta_db.ProductModel', db_column='TBItem_ID', on_delete=models.DO_NOTHING)
    brand = models.ForeignKey('meta_db.BrandModel', db_column='TBVendor_ID', on_delete=models.DO_NOTHING)
    color = models.ForeignKey('meta_db.ColorModel', db_column='TBColor_ID', on_delete=models.DO_NOTHING)
    shoe_size = models.ForeignKey('meta_db.ShoeSizeChartModel', db_column='TBShoeSize_ID', blank=True, null=True, on_delete=models.DO_NOTHING)
    line_status = models.ForeignKey('InvoiceSubStatusModel', db_column='TBInvoiceSubStatus_ID', on_delete=models.DO_NOTHING)

    @property
    def available_color_link(self):
        try:
            available_color = ColorSelectedModel.objects.values_list('image_link', flat=True). \
                filter(item_id=self.item_id, color=self.color_id, image_link__isnull=False).first()
            return available_color
        except ColorSelectedModel.DoesNotExist:
            return None

    def save(self, *args, **kwargs):
        if not self.pk:
            self.line_id = _get_unique_invoice_id(self)
            self.sub_invoice_status = InvoiceSubStatusModel.objects.get(pk=1)
            self.brand = self.item.brand
            self.description = self.item.description
            if self.item.is_sale:
                self.purchase_price = self.item.sub_invoice_sale_price
            else:
                self.purchase_price = self.item.purchase_price
        try:
            super(AbstractSubInvoiceModel, self).save(*args, **kwargs)
        except IntegrityError as e:
            # TODO: log here
            if not self.pk and hasattr(e, 'args') and 'The duplicate key value' in e.args[-1]:
                self.save(*args, **kwargs)
            else:
                raise e

    class Meta(AbstractSubInvoiceModel.Meta):
        managed = False


class AbstractInvoiceSubStatusModelManager(models.Manager):
    def all_active(self):
        return super(AbstractInvoiceSubStatusModelManager, self).get_queryset().filter(is_active=True)


class AbstractInvoiceSubStatusModel(models.Model):
    id = models.AutoField(db_column='TBInvoiceSubStatus_ID', primary_key=True)
    status = models.CharField(db_column='Status', max_length=50)
    is_active = models.BooleanField(db_column='is_active', default=1)
    objects = AbstractInvoiceSubStatusModelManager()

    class Meta:
        abstract = True
        db_table = 'TBInvoiceSubStatus'


class InvoiceSubStatusModel(AbstractInvoiceSubStatusModel):
    class Meta(AbstractInvoiceSubStatusModel.Meta):
        managed = False


def _get_unique_invoice_id(obj):
    """
    :param _class:
    :return: invoice_id
    """
    _class = obj.__class__
    _now = datetime.now()
    _salt = (_now.year - 2000) * 1209000 + (_now.month * 93000) \
            + (_now.day * 2905) + (_now.hour * 121) + (_now.minute * 2)
    _key = _class.objects.latest().pk + _salt
    _candidate_id = "WB%s" % _key
    try:
        while True:
            # TODO: in case sub invoice, may cause 'Return more than one' error
            _filed_name = 'invoice_master_id' if _class.__name__ == 'MasterInvoiceModel' else 'line_id'
            _class.objects.get(**{_filed_name: _candidate_id})
            _key += 1
            _candidate_id = "WB%s" % _key
    except _class.DoesNotExist:
        _candidate_id = "WB%s" % _key
        return _candidate_id

