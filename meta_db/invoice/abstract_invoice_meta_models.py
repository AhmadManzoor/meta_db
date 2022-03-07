from __future__ import unicode_literals
from django.db import models


class AbstractMetaMasterInvoiceModel(models.Model):
    """
    Shipping Fee: shipping fee.
    Handling Fee: depreciated.
    Store Credit: used store credit on an invoice.
    Order Amount: total of products price.
    Sub Total: "order amount + shipping fee + handling fee"
    Due Amount: "order amount - shipping fee - handling fee"
    Paid Amount: captured amount.
    balance: "sub total - store credit - paid amount"
    """
    which_place = models.CharField(max_length=10,
                                   db_column='TBWhichPlace',
                                   blank=True,
                                   default='Web')
    # BILLING ADDRESS
    # ctcompanyname = models.CharField(max_length=100, db_column='CTCompanyName', blank=True)
    bill_first_name = models.CharField(max_length=50,
                                       db_column='CTCustomerFirstName',
                                       blank=True)
    bill_last_name = models.CharField(max_length=50,
                                      db_column='CTCustomerLastName',
                                      blank=True)
    bill_address1 = models.CharField(max_length=200,
                                     db_column='CTAddress1',
                                     blank=True)
    bill_address2 = models.CharField(max_length=60,
                                     db_column='CTAddress2',
                                     blank=True)
    bill_city = models.CharField(max_length=50, db_column='CTCity', blank=True)
    bill_state = models.CharField(max_length=50,
                                  db_column='CTState',
                                  blank=True)
    bill_zipcode = models.CharField(max_length=50,
                                    db_column='CTZip',
                                    blank=True)
    bill_country = models.CharField(max_length=50,
                                    db_column='CTCountry',
                                    blank=True)
    bill_phone_number = models.CharField(max_length=50,
                                         db_column='CTPhone',
                                         blank=True)
    # SHIPPING INFO
    mail_company_name = models.CharField(max_length=100,
                                         db_column='CTMailCompanyName',
                                         blank=True)
    mail_attention_name = models.CharField(max_length=50,
                                           db_column='CTMailAttention',
                                           blank=True)
    mail_address1 = models.CharField(max_length=200,
                                     db_column='CTMailAddress1',
                                     blank=True)
    mail_address2 = models.CharField(max_length=60,
                                     db_column='CTMailAddress2',
                                     blank=True)
    mail_city = models.CharField(max_length=50,
                                 db_column='CTMailCity',
                                 blank=True)
    mail_state = models.CharField(max_length=50,
                                  db_column='CTMailState',
                                  blank=True)
    mail_zipcode = models.CharField(max_length=50,
                                    db_column='CTMailZip',
                                    blank=True)
    mail_country = models.CharField(max_length=50,
                                    db_column='CTMailCountry',
                                    blank=True)
    mail_phone_number = models.CharField(max_length=50,
                                         db_column='CTMailPhone',
                                         blank=True)
    # CARD INFO
    card_type = models.CharField(max_length=255,
                                 db_column='CardType',
                                 blank=True)
    card_number = models.CharField(max_length=255,
                                   db_column='CardNumber',
                                   blank=True)

    card_expire_month = models.CharField(max_length=255,
                                         db_column='CardExpireMonth',
                                         blank=True)
    card_expire_year = models.CharField(max_length=255,
                                        db_column='CardExpireYear',
                                        blank=True,
                                        help_text='card security code')
    payment_profile_id = models.CharField(max_length=50,
                                          db_column='PaymentProfileID',
                                          blank=True)
    customer_comment = models.CharField(
        max_length=3000,
        db_column='CommentsByCustomer',
        blank=True,
        help_text='a leaved message when it ordered')
    customer_ip_address = models.CharField(max_length=30,
                                           db_column='CustomerIP_Address',
                                           blank=True,
                                           help_text='user ip')
    reserved_store_credit = models.DecimalField(
        decimal_places=4,
        max_digits=19,
        db_column='ReservedStoreCredit',
        blank=True,
        default=0.00,
        help_text='reserved store credit')

    # bill_fax = models.CharField(max_length=50, db_column='CTFax', blank=True)
    # bill_handphone = models.CharField(max_length=50, db_column='CTHandPhone', blank=True)
    # tbcustomershippingaddresslists_id = models.BigIntegerField(null=True, db_column='TBCustomerShippingAddressLists_ID', blank=True)
    # imseriesgroup = models.IntegerField(null=True, db_column='IMSeriesGroup', blank=True)
    # comments = models.TextField(db_column='Comments', blank=True)
    # shippingprofileid = models.CharField(max_length=50, db_column='ShippingProfileID', blank=True)
    # authcodeonedollar = models.CharField(max_length=1000, db_column='AuthCodeOneDollar', blank=True)
    # authcode = models.CharField(max_length=1000, db_column='AuthCode', blank=True)
    # transactiongatewayresponse = models.CharField(max_length=1000, db_column='TransactionGatewayResponse', blank=True)
    # shippinginsurance = models.CharField(max_length=1, db_column='ShippingInsurance', blank=True)
    # shipouremailstatus = models.CharField(max_length=1, db_column='ShipourEmailStatus', blank=True)
    # oniscustomer = models.CharField(max_length=1, db_column='OnisCustomer', blank=True)
    # shippinginsurancefee = models.DecimalField(decimal_places=4, null=True, max_digits=19, db_column='ShippingInsuranceFee', blank=True)
    # ndefshippingpref = models.CharField(max_length=1, db_column='nDefShippingPref', help_text='shipping preference')
    # ngbshippingpref = models.CharField(max_length=1, db_column='nGBShippingPref')
    # nssnm = models.CharField(max_length=1, db_column='nSSNM', blank=True)
    # imcodadditionalamt = models.DecimalField(decimal_places=4, null=True, max_digits=19, db_column='IMCODAdditionalAmt', blank=True)
    # captureresponsereasoncode = models.CharField(max_length=10, db_column='CaptureResponseReasonCode', blank=True)
    # captureresponsecode = models.CharField(max_length=2, db_column='CaptureResponseCode', blank=True)
    # authresponsecode = models.CharField(max_length=2, db_column='AuthResponseCode', blank=True, null=True)
    # groupbuyseries = models.CharField(max_length=1, db_column='GroupBuySeries')
    # groupshippinginvoicemaster_id = models.CharField(max_length=10, db_column='GroupShippingInvoiceMaster_ID', blank=True)
    # npreorderpref = models.CharField(max_length=1, db_column='nPreOrderPref')
    # customershippingaccount = models.CharField(max_length=50, db_column='CustomerShippingAccount', blank=True)
    # payment_othersoption = models.CharField(max_length=2, db_column='Payment_OthersOption', blank=True)
    # others_contactname = models.CharField(max_length=50, db_column='Others_ContactName', blank=True)
    # others_contactphone = models.CharField(max_length=50, db_column='Others_ContactPhone', blank=True)
    # others_contacttime = models.CharField(max_length=50, db_column='Others_ContactTime', blank=True)
    # shoeprocessingstatus = models.CharField(max_length=10, db_column='ShoeProcessingStatus', blank=True)
    # pointused = models.CharField(max_length=1, db_column='PointUSED')
    # imvoidreason = models.CharField(max_length=500, db_column='IMVoidReason', blank=True)
    # amountdiscountminimumamount = models.DecimalField(decimal_places=0, null=True, blank=True, max_digits=18, db_column='AmountDiscountMinimumAmount')
    # iminvoicedcamt = models.DecimalField(decimal_places=4, null=True, max_digits=19, db_column='IMInvoiceDCAmt', blank=True, default=0.00)
    # iminvoicegbdcamt = models.DecimalField(decimal_places=4, null=True, max_digits=19, db_column='IMInvoiceGBDCAmt', blank=True, default=0.00)
    # imcustomermemo = models.CharField(max_length=1000, db_column='IMCustomerMemo', blank=True)
    # imrequireddate = models.DateTimeField(null=True, db_column='IMRequiredDate', blank=True, auto_now_add=True)
    # imcompletepaid = models.NullBooleanField(null=True, db_column='IMCompletePaid', blank=True, default=False)
    # imvoid = models.NullBooleanField(null=True, db_column='IMVoid', blank=True, default=False)
    # imshippingmemo = models.CharField(max_length=3000, db_column='IMShippingMemo', blank=True)
    # impackingcheck = models.NullBooleanField(null=True, db_column='IMPackingCheck', blank=True, default=False)
    # imnote = models.TextField(db_column='IMNote', blank=True)
    # tbpaymentmethod_id = models.BigIntegerField(db_column='TBPaymentMethod_ID', help_text='FK of TBPaymentMethods')
    # tbpayment_id = models.BigIntegerField(null=True, db_column='TBPayment_ID', blank=True)

    class Meta:
        abstract = True
