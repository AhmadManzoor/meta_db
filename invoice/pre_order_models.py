from __future__ import unicode_literals

from datetime import datetime
import time
import random
import string

from django.db import models, IntegrityError
from jsonfield import JSONField
from meta_db.models import ColorSelectedModel, FulfillmentModel
from meta_db.exceptions import PreventDeleteException
from meta_db.invoice.abstract_invoice_meta_models import AbstractMetaMasterInvoiceModel


####################
# PRE-ORDER MASTER #
####################


class POStatusManager(models.Manager):
    # TODO: abstract and meta
    def all_active(self):
        return super(POStatusManager, self).get_queryset().filter(
            is_active=True)


class AbstractMasterPOStatusModel(models.Model):
    # TODO: abstract and meta
    id = models.AutoField(db_column='TBPOStatus_ID', primary_key=True)
    status = models.CharField(db_column='Status', max_length=50, null=False)
    is_active = models.BooleanField(db_column='is_active', null=False, default=1)
    objects = POStatusManager()

    class Meta:
        abstract = True
        managed = False
        get_latest_by = 'id'
        db_table = 'TBPOStatus'


class MasterPOStatusModel(AbstractMasterPOStatusModel):
    class Meta(AbstractMasterPOStatusModel.Meta):
        pass


class AbstractMasterPOModel(AbstractMetaMasterInvoiceModel):
    # TODO: inherit
    id = models.AutoField(db_column='TBPOMaster_ID', primary_key=True)
    po_number = models.CharField(
        max_length=17, db_column='PONumber',
        null=False, unique=True,
        help_text='automatically and uniquely generated as POnn..nn')
    ordered_date = models.DateTimeField(db_column='OrderDate', auto_now_add=True)
    complete_date = models.DateTimeField(null=True, db_column='CompleteDate')
    # PRICE VALUES
    order_amount = models.DecimalField(decimal_places=4, max_digits=19, db_column='OrderAmt', blank=True, default=0.00, help_text='for original order amount, read-only')
    is_void = models.BooleanField(db_column='POVoid', default=False, null=False)
    voided_date = models.DateTimeField(db_column='VoidDate', null=True)
    # COMMENTS
    po_memo = models.CharField(max_length=3000, db_column='PONote', blank=True, default='')
    brand_comment = models.CharField(max_length=3000, db_column='CommentsByBrand', blank=True, help_text='comments by brand on PO')
    void_reason = models.CharField(max_length=500, blank=True, db_column='VoidReason', default='')
    # PROMOTION DISCOUNT
    # promotion_id = models.IntegerField(db_column='Promotion_ID', null=True, help_text='promotion table should be defined')
    po_star = models.SmallIntegerField(db_column='PORating', blank=True, null=True, help_text='for fraud detection algorithm')
    os_commission = models.FloatField(db_column='OSCommission', blank=True, null=False, default=0.0, help_text='OS Commission Rate')
    merchant_fee = models.FloatField(db_column='MerchantFee', blank=True, null=False, default=0.0, help_text='Credit Card & Paypal Fee Rate')

    @property
    def parent_master_invoice(self):
        """
        get back-ordered (BO) PO's parent invoice master
        :return: invoice_master model object
        """
        try:
            parent_master = POMasterInvoiceMapModel.objects.get(
                po__id=self.id,
                map_type="BO").invoice_master
            return parent_master
        except:
            return None

    @property
    def child_master_invoices(self):
        """
        get current PO's child invoice masters
        :return: invoice_master model objects
        """
        try:
            invoices = list()
            for _map in POMasterInvoiceMapModel.objects.filter(
                    po__id=self.id,
                    map_type__in=['PO', 'BPO']):
                invoices.append(_map.invoice_master)
            return invoices
        except Exception as e:
            print("[debug] Exception - %s (%s)" % (str(e), str(type(e))))
            return None

    def _get_unique_po_number(self):
        """
        :param :
        :return: po_number
        """
        _now = datetime.now()
        _salt = (_now.year - 2000) * 1209000 + (_now.month * 93000) \
                + (_now.day * 2905) + (_now.hour * 121) + (_now.minute * 2)
        _key = MasterPOModel.objects.latest().pk + _salt
        _candidate_id = "PO-WB%s" % _key
        try:
            while True:
                _po_id = MasterPOModel.objects.get(**{'po_number': _candidate_id})
                _key += 1
                _candidate_id = "PO-WB%s" % _key
        except MasterPOModel.DoesNotExist:
            _candidate_id = "PO-WB%s" % _key
            return _candidate_id

    def save(self, *args, **kwargs):
        if not self.pk:
            self.po_number = self._get_unique_po_number()
            try:
                super(AbstractMasterPOModel, self).save(*args, **kwargs)
            except IntegrityError as e:
                if not self.pk and hasattr(e, 'args') and 'The duplicate key value' in \
                        e.args[-1]:
                    self.po_number = self._get_unique_po_number()
                    self.save(*args, **kwargs)
                else:
                    raise e
        else:
            super(AbstractMasterPOModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise PreventDeleteException('cannot delete master PO')

    class Meta:
        abstract = True
        managed = False
        get_latest_by = 'id'
        db_table = 'TBPOMaster'


class MasterPOModel(AbstractMasterPOModel):
    user = models.ForeignKey('meta_db.UserModel', db_column='TBCustomer_ID', to_field='customer_id', related_name='master_po', on_delete=models.DO_NOTHING)
    po_status = models.ForeignKey('MasterPOStatusModel', db_column='TBPOStatus_ID', default=1, on_delete=models.DO_NOTHING)
    shipping_method = models.ForeignKey('meta_db.ShippingMethodModel', db_column='TBShipMethod_ID', to_field='sp_id', on_delete=models.DO_NOTHING)
    payment_method = models.ForeignKey('meta_db.PaymentMethodModel', db_column='TBSaleMethod_ID', help_text='FK. payment method id. TBSaleMethod table', on_delete=models.DO_NOTHING)
    fulfilled_by = models.ForeignKey('meta_db.FulfillmentModel', db_column='TBShipFrom_ID', to_field='id', blank=False, null=False, on_delete=models.DO_NOTHING)

    @property
    def get_status_name(self):
        PO_STATUS = {
            1: 'Processing',
            2: 'Complete',
            3: 'Void Requested',
            4: 'Void'
        }
        try:
            if self.is_void and self.po_status.id != 4:
                return "Void Requested"
            else:
                return PO_STATUS[self.po_status.id]
        except:
            return ""

    @property
    def is_void_requested(self):
        return True if self.is_void and self.po_status.id != 4 else False

    @property
    def void_request(self):
        try:
            return VoidHistoryModel.objects.filter(
                order_id=self.po_number, void_status='Void Pending'). \
                order_by('-id').first()
        except VoidHistoryModel.DoesNotExist:
            return None

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
    def get_shipping_method_name(self):
        try:
            return self.shipping_method.method_name
        except (ValueError, AttributeError, KeyError):
            return ""

    @property
    def is_brand_fulfillment(self):
        return False if self.fulfillment.fulfillment in ('OrangeShine.com', 'OS SHOES') else True

    @property
    def fulfillment_by(self):
        try:
            return self.fulfillment.fulfillment
        except FulfillmentModel.DoesNotExist:
            return ""

    class Meta(AbstractMasterPOModel.Meta):
        pass


class AbstractPOLineModel(models.Model):
    id = models.AutoField(db_column='TBPOLine_ID', primary_key=True)
    line_id = models.CharField(max_length=17, db_column='POLineNumber', null=False, unique=True, help_text='automatically and uniquely generated as PLnn..nn')
    created_date = models.DateTimeField(null=True, db_column='CreateDate', auto_now_add=True)
    updated_date = models.DateTimeField(db_column='UpdateDate', auto_now_add=True)
    size_chart = JSONField('SizeChart')  # json dict type
    # _size_chart = models.CharField(max_length=255, null=False, db_column='SizeChart', help_text='{"S":"2", "M":"2", "L":"2"}')
    package_qty = models.SmallIntegerField(db_column='PackageQty', null=False)
    total_item_qty = models.SmallIntegerField(db_column='TotalItemQty', null=False)
    # PRICE VALUES
    purchase_price = models.DecimalField(decimal_places=4, max_digits=19, null=True, blank=True, db_column='PurchasePrice', default=0.00)
    retail_price = models.DecimalField(decimal_places=4, max_digits=19, null=True, blank=True, db_column='SalePrice', default=0.00, help_text='retail price')
    discounted_price = models.DecimalField(decimal_places=4, max_digits=19, null=True, blank=True, db_column='DiscountedPrice', default=0.00)
    sub_total = models.DecimalField(decimal_places=4, max_digits=19, db_column='SubTotal')
    is_preorder = models.BooleanField(db_column='is_preorder', default=True)
    preorder_available_date = models.DateTimeField(null=True, blank=True, db_column='nPreOrderAvailableDate')

    # @property
    # def size_chart(self):
    #     return json.loads(self._size_chart)

    # @size_chart.setter
    # def size_chart(self, json_dict):
    #     self._size_chart = json.dumps(json_dict)

    @property
    def pack_price(self):
        return self.total_item_qty * self.retail_price

    def delete(self, *args, **kwargs):
        raise PreventDeleteException('cannot delete sub invoice')

    class Meta:
        abstract = True
        managed = False
        get_latest_by = 'id'
        db_table = 'TBPOLine'


class POLineModel(AbstractPOLineModel):
    master_order = models.ForeignKey('MasterPOModel', db_column='PONumber', to_field='po_number', related_name='po_lines', on_delete=models.DO_NOTHING)
    item = models.ForeignKey('meta_db.ProductModel', db_column='TBItem_ID', related_name='po_item', on_delete=models.DO_NOTHING)
    brand = models.ForeignKey('meta_db.BrandModel', db_column='Brand_ID', to_field='id', on_delete=models.DO_NOTHING)
    color = models.ForeignKey('meta_db.ColorModel', db_column='TBColor_ID', on_delete=models.DO_NOTHING)
    shoe_size = models.ForeignKey('meta_db.ShoeSizeChartModel', db_column='TBShoeSize_ID', blank=True, null=True, default=0, on_delete=models.DO_NOTHING)
    line_status = models.ForeignKey('POLineStatusModel', db_column='TBPOLineStatus_ID', default=1, on_delete=models.DO_NOTHING)

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
            self.po_line_status = POLineStatusModel.objects.get(pk=1)
            self.brand = self.item.brand
            if self.item.is_sale:
                self.purchase_price = self.item.sub_invoice_sale_price
            else:
                self.purchase_price = self.item.purchase_price

            self.line_id = 'PL-{}-{}'.format(int(time.time()), ''.join(
                random.choice(string.ascii_uppercase + string.digits) for i in range(3)))
            try:
                super(POLineModel, self).save(*args, **kwargs)
            except IntegrityError as e:
                if not self.pk and hasattr(e, 'args') and 'The duplicate key value' in \
                        e.args[-1]:
                    self.line_id = 'PL-{}-{}'.format(int(time.time()), ''.join(
                        random.choice(string.ascii_uppercase + string.digits) for i in range(3)))
                    self.save(*args, **kwargs)
                else:
                    raise e
        else:
            super(POLineModel, self).save(*args, **kwargs)

    class Meta(AbstractPOLineModel.Meta):
        pass


class POLineStatusManager(models.Manager):
    # TODO: abstract and meta
    def all_active(self):
        return super(POLineStatusManager, self).get_queryset().filter(
            is_active=True)


class AbstractPOLineStatusModel(models.Model):
    # TODO: abstract and meta
    id = models.AutoField(db_column='TBPOLineStatus_ID', primary_key=True)
    status = models.CharField(
        db_column='Status', max_length=50, null=False)
    is_active = models.BooleanField(
        db_column='is_active', null=False, default=True)
    objects = POLineStatusManager()

    class Meta:
        abstract = True
        managed = False
        get_latest_by = 'id'
        db_table = 'TBPOLineStatus'


class POLineStatusModel(AbstractPOLineStatusModel):
    class Meta(AbstractPOLineStatusModel.Meta):
        pass


class AbstractPOMasterInvoiceMapModel(models.Model):
    # TODO: abstract and meta
    id = models.AutoField(db_column='TBPOInvoiceMaster_ID', primary_key=True)
    po = models.ForeignKey('MasterPOModel',
                           db_column='PONumber',
                           to_field='po_number',
                           on_delete=models.PROTECT,
                           help_text='not NULL for CIM method')
    invoice_master = models.ForeignKey('MasterInvoiceModel',
                                       db_column='TBInvoiceMaster_ID',
                                       to_field='invoice_master_id',
                                       on_delete=models.PROTECT)
    map_type = models.CharField(db_column='MapType', max_length=5,
                                default='PO',
                                help_text='PO: pre-order,'
                                          'BO: back-order,'
                                          'BPO: invoice from back-order')

    def delete(self, *args, **kwargs):
        raise PreventDeleteException('cannot delete PO-MasterInvoice map')

    class Meta:
        abstract = True
        managed = False
        get_latest_by = 'id'
        db_table = 'TBPOInvoiceMasterMap'


class POMasterInvoiceMapModel(AbstractPOMasterInvoiceMapModel):
    class Meta(AbstractPOMasterInvoiceMapModel.Meta):
        pass