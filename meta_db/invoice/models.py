from __future__ import unicode_literals

from django.db import models


# Master Invoice Status
class AbstractMasterInvoiceStatusModel(models.Model):
    id = models.AutoField(db_column='TBInvoiceStatus_ID', primary_key=True)
    invoice_status = models.TextField(db_column='TBInvoiceStatus')
    invoice_status_espanol = models.TextField(
        db_column='TBInvoiceStatus_espanol')

    def delete(self, using=None, keep_parents=False):
        raise Exception('cannot delete master invoice Status')

    class Meta:
        abstract = True
        db_table = 'TBInvoiceStatus'


class MasterInvoiceStatusModel(AbstractMasterInvoiceStatusModel):
    class Meta(AbstractMasterInvoiceStatusModel.Meta):
        managed = False


# Payment Method
class AbstractPaymentMethodModelManager(models.Manager):
    def all(self):
        return super(AbstractPaymentMethodModelManager,
                     self).get_queryset().filter(is_active=True)

    def all_with_inactive(self):
        return super(AbstractPaymentMethodModelManager,
                     self).get_queryset().all()


class AbstractPaymentMethodModel(models.Model):
    """
    Credit Card: WH1
    Paypal: WH20
    COD: WH22 - disabled
    WIRE: WH21
    """
    id = models.CharField(db_column='TBSaleMethod_ID',
                          max_length=10,
                          primary_key=True)
    name = models.CharField(db_column='SMSaleMethodName', max_length=20)
    description = models.CharField(db_column='SMDescription',
                                   max_length=50,
                                   blank=True,
                                   null=True)
    is_active = models.BooleanField(db_column='is_active', default=True)
    objects = AbstractPaymentMethodModelManager()

    def __unicode__(self):
        return '%s %s' % (self.id, self.name)

    def save(self, *args, **kwargs):
        if not self.pk:
            raise Exception('cannot save without id like WH00')

    def delete(self, *args, **kwargs):
        raise Exception('cannot delete payment method. inactive instead.')

    class Meta:
        abstract = True
        db_table = 'TBSaleMethod'


class PaymentMethodModel(AbstractPaymentMethodModel):
    class Meta(AbstractPaymentMethodModel.Meta):
        managed = False


class AbstractVoidHistoryModel(models.Model):
    # TODO: abstract and meta
    id = models.AutoField(db_column='TBVoidHistory_ID', primary_key=True)
    type = models.CharField(
        db_column='Type',
        max_length=10,
        null=False,
        default='INV',
        help_text='PO: for TBPOMaster, INV: for TBInvoiceMaster')
    order_id = models.CharField(db_column='OrderID',
                                max_length=17,
                                null=False,
                                help_text='PONumber or TBInvoiceMaster_ID')
    void_reason = models.CharField(max_length=500,
                                   db_column='VoidReason',
                                   null=False)
    # void_type = models.ForeignKey('VoidTypeModel', db_column='TBVoidType_ID', to_field='id', help_text='VoidTypeModel', on_delete=models.DO_NOTHING)
    requester_id = models.CharField(
        max_length=100,
        db_column='RequesterID',
        null=True,
        help_text=
        'Brand_ID, TBCustomer.TBCustomer_ID, WebsiteAdministrators.LoginID or None for System'
    )
    requester_type = models.CharField(
        max_length=10,
        db_column='RequesterType',
        null=True,
        help_text='Brand, Buyer, OS Admin or System')
    approver_id = models.CharField(
        max_length=100,
        db_column='ApproverID',
        null=True,
        help_text='TBCustomer.TBCustomer_ID or WebsiteAdministrators.LoginID')
    approver_type = models.CharField(max_length=10,
                                     db_column='ApproverType',
                                     null=True,
                                     help_text='Buyer or OS')
    approver_comment = models.CharField(max_length=500,
                                        db_column='ApproverComment',
                                        null=False)
    void_status = models.CharField(
        max_length=20,
        db_column='VoidStatus',
        null=False,
        help_text='Void Pending, Void, or Void Cancelled')
    void_request_date = models.DateTimeField(db_column='VoidRequestDate',
                                             null=False)
    completed_date = models.DateTimeField(db_column='CompletedDate', null=True)
    is_confirmed = models.BooleanField(db_column='isConfirmed', default=False)

    class Meta:
        abstract = True
        get_latest_by = 'id'
        db_table = 'TBVoidHistory'


class VoidHistoryModel(AbstractVoidHistoryModel):
    pass

    class Meta(AbstractVoidHistoryModel.Meta):
        managed = False


class VoidReasonModel(models.Model):
    void_reason_code = models.CharField(db_column='VoidReasonCode',
                                        max_length=5,
                                        primary_key=True)
    description = models.CharField(db_column='Description',
                                   max_length=100,
                                   null=True)
    is_brand_active = models.BooleanField(
        db_column='IsVendorActive', null=False, default=True)
    is_active = models.BooleanField(
        db_column='IsActive', null=False, default=True)

    class Meta:
        managed = False
        db_table = 'TBVoidReason'
