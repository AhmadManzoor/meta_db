from __future__ import unicode_literals

# import base64
import datetime
import calendar

from django.db import models
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager)

from meta_db.exceptions import PreventSaveException, PreventDeleteException

from sugar.string.fernet import FernetHandler


########
# USER #
########
class AbstractUserModelManager(BaseUserManager):
    def create(self, email, password=None, brand_id=None, **kwargs):
        if not email:
            raise ValueError('Users must have an email address')

        try:
            _customer_id = int(super(AbstractUserModelManager, self).get_queryset().last().id) + 1
        except ValueError:
            raise ValueError('Please try later.')

        # try:
        #     # password = base64.b64encode(password.encode('utf-8')).decode()
        #     # fh = FernetHandler(settings.ENCRYPT_KEY_USER_PASSWORD_OS_WEB)
        #     # password = fh.encrypt(password)
        # except TypeError:
        #     raise TypeError('Password is not appropriated.')

        user = self.model(email=self.normalize_email(email),
                          customer_id="WB%s" % _customer_id,
                          password=password,
                          brand_id=brand_id,
                          **kwargs)
        user.save(using=self._db)
        return user

    def brand_user(self, brand_id=None):
        return super(AbstractUserModelManager, self).get_queryset().filter(brand_id=brand_id)

    def brand_active_user(self, brand_id=None):
        return super(AbstractUserModelManager, self).get_queryset().filter(brand_id=brand_id,
                                                                           _is_active='Y',
                                                                           _is_approved='Y')

    def os_user(self):
        return super(AbstractUserModelManager, self).get_queryset().filter(brand_id__isnull=True)

    def os_active_user(self):
        return super(AbstractUserModelManager, self).get_queryset().filter(brand_id__isnull=True,
                                                                           _is_active='Y',
                                                                           _is_approved='Y')

    def site(self, request):
        _site = 'cm' if get_current_site(request).domain in settings.CM_SITES else 'web'
        return super(AbstractUserModelManager, self).get_queryset().filter(brand_id__isnull=True,
                                                                           register_source__iexact=_site)

    def site_active(self, request):
        _site = 'cm' if get_current_site(request).domain in settings.CM_SITES else 'web'
        return super(AbstractUserModelManager, self).get_queryset().filter(brand_id__isnull=True,
                                                                           _is_active='Y',
                                                                           _is_approved='Y',
                                                                           register_source__iexact=_site)


class AbstractUserModel(AbstractBaseUser):
    """
    USER MODEL
    """
    id = models.AutoField(db_column='TBCustomer_SQL_ID', primary_key=True, help_text='pk')
    register_source = models.CharField(max_length=10,
                                       db_column='TBWhichPlace',
                                       blank=True,
                                       default='WEB',
                                       help_text='mark source of register')
    customer_id = models.CharField(max_length=8,
                                   db_column='TBCustomer_ID',
                                   blank=True,
                                   unique=True,
                                   help_text='unique id each customer')
    customer_profile_id = models.CharField(max_length=50, db_column='CustomerProfileID', blank=True, null=True)
    brand_id = models.CharField(max_length=3,
                                db_column='onVendor_ID',
                                blank=True,
                                null=True,
                                help_text='brand id for brand own customer ')
    company_name = models.CharField(max_length=200, db_column='CTCompanyName', blank=True)
    email = models.EmailField(max_length=100, db_column='email')
    password = models.CharField(max_length=250,
                                db_column='password',
                                blank=True,
                                help_text='encrypted login password - hold 127 bytes of plain password')

    _is_active = models.CharField(max_length=1, db_column='is_active', default='Y')  # when it signup. active should Y
    first_name = models.CharField(max_length=50, db_column='first_name', blank=True)
    last_name = models.CharField(max_length=50, db_column='last_name', blank=True)
    # CONTACT INFORMATION
    ct_website = models.CharField(max_length=100, db_column='CTWebsite', blank=True)
    ct_phone_number = models.CharField(max_length=100, db_column='CTPhone', blank=True)
    ct_contact_title = models.CharField(max_length=100, db_column='CTContactTitle', blank=True, null=True)
    ct_mobile_phone = models.CharField(max_length=100, db_column='CTHandPhone', blank=True)
    ct_address1 = models.CharField(max_length=200, db_column='CTAddress1', blank=True, help_text='company address 1')
    ct_address2 = models.CharField(max_length=200, db_column='CTAddress2', blank=True, help_text='company address 2')
    ct_city = models.CharField(max_length=100, db_column='CTCity', blank=True, help_text='company city')
    ct_state = models.CharField(max_length=100, db_column='CTState', blank=True, help_text='company state')
    ct_zipcode = models.CharField(max_length=100, db_column='CTZip', blank=True, help_text='company zip')
    ct_country = models.CharField(max_length=100,
                                  db_column='CTCountry',
                                  blank=True,
                                  default='US',
                                  help_text='company country')
    ct_fax = models.CharField(max_length=100, db_column='CTFax', blank=True)

    # BILLING INFORMATION. depreciated
    mail_address1 = models.CharField(max_length=200,
                                     db_column='CTMailAddress1',
                                     blank=True,
                                     help_text='shipping address 1')
    mail_address2 = models.CharField(max_length=200,
                                     db_column='CTMailAddress2',
                                     blank=True,
                                     help_text='shipping address 2')
    mail_city = models.CharField(max_length=100, db_column='CTMailCity', blank=True, help_text='shipping city')
    mail_state = models.CharField(max_length=100, db_column='CTMailState', blank=True, help_text='shipping state')
    mail_zipcode = models.CharField(max_length=100, db_column='CTMailZip', blank=True, help_text='shipping zipcode')
    mail_country = models.CharField(max_length=100, db_column='CTMailCountry', blank=True, help_text='shipping country')
    mail_phone_number = models.CharField(max_length=100,
                                         db_column='CTMailPhone',
                                         blank=True,
                                         help_text='shipping phone')
    # ACCOUNT INFORMATION
    resale_id = models.CharField(max_length=100, db_column='ResaleID', blank=True)
    _is_receive_email = models.CharField(max_length=1, db_column='ReceiveEmail', blank=True, default='Y')
    receive_push = models.BooleanField(db_column='ReceivePush', default=True)
    total_order_count = models.IntegerField(null=True, db_column='TotalOrderCount', blank=True, default=0)
    total_order_amount = models.DecimalField(decimal_places=4,
                                             null=True,
                                             max_digits=19,
                                             db_column='TotalOrderAmount',
                                             blank=True,
                                             default=0.00)
    total_login_count = models.IntegerField(null=True, db_column='TotalLoginCount', blank=True, default=0)
    date_joined = models.DateTimeField(null=True, db_column='date_joined', blank=True, auto_now_add=True)
    date_time_last_updated = models.DateTimeField(db_column='DateTimeLastUpdated', null=True, blank=True, auto_now=True)
    _is_approved = models.CharField(max_length=1,
                                    db_column='Approved',
                                    default='N',
                                    help_text='when is sign up. approved should be N')
    register_ip = models.CharField(max_length=50, db_column='RegisterIP', blank=True)
    last_login_ip = models.CharField(max_length=50, db_column='LastLoginIP', blank=True, null=True)
    is_available_email = models.NullBooleanField(null=True, db_column='isAvailableEmail', blank=True, default=True)
    is_email_verified = models.NullBooleanField(db_column='IsEmailVerified', blank=True, null=True, default=False)
    _is_staff = models.CharField(max_length=1, db_column='nOSStaff', blank=True, default='N', help_text='check staff')
    store_credit_amount = models.DecimalField(decimal_places=4,
                                              max_digits=19,
                                              db_column='CTStoreCredit',
                                              help_text='store credit',
                                              default=0.00)
    auth_password = models.CharField(max_length=100,
                                     db_column='AuthPassword',
                                     blank=True,
                                     help_text='uuid as a token to password reset')
    auth_password_on_date = models.DateTimeField(null=True,
                                                 db_column='AuthPasswordOnDate',
                                                 blank=True,
                                                 help_text='requested date and time')
    changed_password_on_date = models.DateTimeField(null=True,
                                                    db_column='ChangedPasswordOnDate',
                                                    blank=True,
                                                    help_text='date and time of changed password')
    _mobile_phone_validation = models.CharField(max_length=1,
                                                db_column='Confirm1st',
                                                blank=True,
                                                help_text='mobile phone number validation',
                                                default='N')
    _is_good_paypal_customer = models.CharField(max_length=1, db_column='Confirm2st', blank=True)
    # confirm3st = models.CharField(max_length=1, db_column='Confirm3st', blank=True)
    seller_permit_image = models.CharField(max_length=200,
                                           db_column='CTPermitImg1',
                                           blank=True,
                                           help_text='user seller permit image')
    seller_permit_image2 = models.CharField(max_length=200,
                                            db_column='CTPermitImg2',
                                            blank=True,
                                            help_text='user seller permit image')
    # is_residential = models.CharField(max_length=1, db_column='IsResidential', blank=True, null=True, default='N')
    # password = models.CharField(max_length=100, db_column='CTLoginPassword', blank=True) # cannot override BaseUser model
    # last_login = models.DateTimeField(null=True, db_column='last_login', blank=True) # cannot override BaseUser model
    # secret_question_id = models.IntegerField(null=True, db_column='TBSecretQuestion_ID', blank=True, default=1)
    # ctnationtype = models.CharField(max_length=1, db_column='CTNationType', default='') #I for international, U for united
    # tbmajormarket_id = models.CharField(max_length=100, db_column='TBMajorMarket_ID', blank=True)
    # africanamerican = models.CharField(max_length=1, db_column='AfricanAmerican', blank=True)
    # asianethnicities = models.CharField(max_length=1, db_column='AsianEthnicities', blank=True)
    # caucasian = models.CharField(max_length=1, db_column='Caucasian', blank=True)
    # latinamerican = models.CharField(max_length=1, db_column='LatinAmerican', blank=True)
    # middleeasternethnicity = models.CharField(max_length=1, db_column='MiddleEasternEthnicity', blank=True)
    # nativeamerican = models.CharField(max_length=1, db_column='NativeAmerican', blank=True)
    # pacificislandethnicity = models.CharField(max_length=1, db_column='PacificIslandEthnicity', blank=True)
    # tbmyvendor_use = models.CharField(max_length=1, db_column='TBMyVendor_Use', blank=True)
    # cardtype = models.CharField(max_length=50, db_column='CardType', blank=True)
    # cardnumber = models.CharField(max_length=50, db_column='CardNumber', blank=True)
    # cardsecuritycode = models.CharField(max_length=50, db_column='CardSecurityCode', blank=True)
    # cardexpiremonth = models.CharField(max_length=10, db_column='CardExpireMonth', blank=True)
    # cardexpireyear = models.CharField(max_length=10, db_column='CardExpireYear', blank=True)
    # ctnote = models.CharField(max_length=300, db_column='CTNote', blank=True)
    # ctcreditcardinfo = models.CharField(max_length=50, db_column='CTCreditCardInfo', blank=True)
    # ctdisc = models.FloatField(null=True, db_column='CTDISC', blank=True)
    # ctfirstpurchasedate = models.DateTimeField(null=True, db_column='CTFirstPurchaseDate', blank=True)
    # ctlastpurchasedate = models.DateTimeField(null=True, db_column='CTLastPurchaseDate', blank=True)
    # ctbalance = models.DecimalField(decimal_places=4, null=True, max_digits=19, db_column='CTBalance', blank=True)
    # ctpricelevel = models.CharField(max_length=50, db_column='CTPriceLevel', blank=True)
    # ctmemo = models.CharField(max_length=200, db_column='CTMemo', blank=True)
    # ctmailcompanyname = models.CharField(max_length=100, db_column='CTMailCompanyName', blank=True)
    # ctmailattention = models.CharField(max_length=100, db_column='CTMailAttention', blank=True)
    # upsinsurance = models.CharField(max_length=1, db_column='UPSinsurance', blank=True)

    # ctshoworlocal = models.CharField(max_length=100, db_column='CTSHOWorLOCAL', blank=True)
    # ctcreditlimitline = models.DecimalField(decimal_places=4, null=True, max_digits=19, db_column='CTCreditLimitLine', blank=True)
    # favoritestbvendor = models.ForeignKey(Tbvendor, null=True, db_column='FavoritesTBVendor_ID', blank=True, on_delete=models.DO_NOTHING)
    # penaltyamount = models.DecimalField(decimal_places=4, null=True, max_digits=19, db_column='PenaltyAmount', blank=True)
    # commentbycustomer = models.TextField(db_column='CommentByCustomer', blank=True)
    # isofflinecustomer = models.CharField(max_length=1, db_column='IsOfflineCustomer', blank=True)
    # ctinvoiceimg1 = models.CharField(max_length=200, db_column='CTInvoiceImg1', blank=True)
    # ctinvoiceimg2 = models.CharField(max_length=200, db_column='CTInvoiceImg2', blank=True)
    # afconfirm = models.CharField(max_length=1, db_column='AFConfirm', blank=True)
    # previewotp = models.CharField(max_length=1, db_column='PreviewOTP', blank=True)
    # tadd = models.CharField(max_length=1, db_column='TAdd', blank=True)
    # tupdate = models.CharField(max_length=1, db_column='TUpdate', blank=True) # UPDATE FOR ARA LOCAL
    # isvendor = models.CharField(max_length=1, db_column='IsVendor', blank=True)
    # retailerorno = models.CharField(max_length=1, db_column='RetailerOrNo', blank=True)
    # sendtheemailtoconfirm = models.CharField(max_length=1, db_column='SendTheEmailToConfirm', blank=True)
    # emaildate = models.DateTimeField(null=True, db_column='EmailDate', blank=True)
    # oniscustomer = models.CharField(max_length=1, db_column='OnisCustomer', blank=True)
    # customerpaymentprofileid = models.CharField(max_length=50, db_column='CustomerPaymentProfileID', blank=True)
    # customershippingaddressprofileid = models.CharField(max_length=50, db_column='CustomerShippingAddressProfileID',
    #                                                     blank=True)
    # locationfromip = models.CharField(max_length=1000, db_column='LocationFromIP', blank=True)
    # ctresaleid1_us = models.CharField(max_length=100, db_column='CTResaleID1_US', blank=True)
    # ctimg1_us = models.CharField(max_length=100, db_column='CTImg1_US', blank=True)
    # ctcompanyname1_int = models.CharField(max_length=100, db_column='CTCompanyName1_INT', blank=True)
    # ctcompanyname2_int = models.CharField(max_length=100, db_column='CTCompanyName2_INT', blank=True)
    # ctcompanyname3_int = models.CharField(max_length=100, db_column='CTCompanyName3_INT', blank=True)
    # ctphone1_int = models.CharField(max_length=50, db_column='CTPhone1_INT', blank=True)
    # ctphone2_int = models.CharField(max_length=50, db_column='CTPhone2_INT', blank=True)
    # ctphone3_int = models.CharField(max_length=50, db_column='CTPhone3_INT', blank=True)
    # ctimg1_int = models.CharField(max_length=100, db_column='CTImg1_INT', blank=True)
    # ctimg2_int = models.CharField(max_length=100, db_column='CTImg2_INT', blank=True)
    # ctimg3_int = models.CharField(max_length=100, db_column='CTImg3_INT', blank=True)
    # cttype = models.CharField(max_length=1, db_column='CTType')
    # nssnm = models.CharField(max_length=1, db_column='nSSNM')
    # nlandingpage = models.CharField(max_length=10, db_column='nLandingPage', blank=True)
    # nsecretquestionanswer = models.CharField(max_length=1000, db_column='nSecretQuestionAnswer')
    # vegas2011 = models.CharField(max_length=1, db_column='Vegas2011')
    # sfreeshipping = models.CharField(max_length=3, db_column='sFreeShipping')
    # isusemyshippingaccount = models.CharField(max_length=3, db_column='isUseMyShippingAccount')
    # nmyshippingacount = models.CharField(max_length=20, db_column='nMyShippingAcount', blank=True)
    # isusemyshippingaccount1 = models.CharField(max_length=3, db_column='isUseMyShippingAccount1')
    # nmyshippingaccount = models.CharField(max_length=20, db_column='nMyShippingAccount', blank=True)
    # nhidden = models.CharField(max_length=1, db_column='nHidden',
    #                            blank=True, default='N')  # when it sign up. nHidden should be 'N'
    # cod_email = models.CharField(max_length=50, db_column='CODEmail', null=True, blank=True)
    # cod_request_date = models.DateTimeField(db_column='CODRequestedDate', null=True, blank=True)
    # is_cod_approved = models.CharField(max_length=1, db_column='IsCODCustomer', default='N',
    #                                    help_text='if user is approved cod, then Y')
    # _cod_min_amount = models.DecimalField(decimal_places=2, null=True, max_digits=19, db_column='CODCapitalMinAmount',
    #                             blank=True, help_text='cod minimum amount')
    objects = AbstractUserModelManager()

    USERNAME_FIELD = 'customer_id'

    def __unicode__(self):
        return self.email

    @property
    def is_active(self):
        return True if self._is_active == 'Y' else False

    @is_active.setter
    def is_active(self, value):
        self._is_active = 'Y' if value else 'N'

    @property
    def is_approved(self):
        return True if self._is_approved == 'Y' else False

    @is_approved.setter
    def is_approved(self, value):
        self._is_approved = 'Y' if value else 'N'

    @property
    def is_staff(self):
        return True if self._is_staff == 'Y' else False

    @is_staff.setter
    def is_staff(self, value):
        self._is_staff = 'Y' if value else 'N'

    @property
    def is_receive_email(self):
        return True if self._is_receive_email == 'Y' else False

    @is_receive_email.setter
    def is_receive_email(self, value):
        self._is_receive_email = 'Y' if value else 'N'

    @property
    def is_brand_user(self):
        return True if self.brand_id else False

    @property
    def mobile_phone_validation(self):
        return True if self._mobile_phone_validation != 'N' else False

    @mobile_phone_validation.setter
    def mobile_phone_validation(self, value):
        self._mobile_phone_validation = 'Y' if value else 'N'

    @property
    def is_good_paypal_customer(self):
        return True if self._is_good_paypal_customer == 'Y' else False

    @is_good_paypal_customer.setter
    def is_good_paypal_customer(self, value):
        self._is_good_paypal_customer = 'Y' if value else 'N'

    def delete(self, *args, **kwargs):
        raise PreventDeleteException('cannot delete user. please de-active instead')

    def get_full_name(self):
        return '%s %s' % (self.first_name, self.last_name)

    def get_short_name(self):
        return '%s' % self.first_name

    def to_dict(self):
        return dict(first_name=self.first_name,
                    last_name=self.last_name,
                    company_name=self.company_name,
                    job_title_id=self.job_title_id,
                    ct_phone_number=self.ct_phone_number,
                    ct_mobile_phone=self.ct_mobile_phone,
                    ct_fax=self.ct_fax,
                    ct_website=self.ct_website,
                    resale_id=self.resale_id,
                    is_receive_email=self.is_receive_email,
                    ct_address1=self.ct_address1,
                    ct_address2=self.ct_address2,
                    ct_city=self.ct_city,
                    ct_state=self.ct_state,
                    ct_country=self.ct_country,
                    ct_zipcode=self.ct_zipcode,
                    seller_permit_image=self.seller_permit_image)

    class Meta:
        abstract = True
        db_table = 'vUser'
        unique_together = (('email', 'brand_id'), )


class UserModel(AbstractUserModel):
    job_title = models.ForeignKey(
        'meta_db.JobTitleModel',
        null=True,
        db_column='TBCustomerJobTitle_ID',
        blank=True,
        related_name='users',
        default=1,
        on_delete=models.DO_NOTHING,
    )
    big_buyer_staff = models.ForeignKey('meta_db.OSStaffModel',
                                        db_column='BigBuyerStaff',
                                        null=True,
                                        blank=True,
                                        on_delete=models.DO_NOTHING)
    carried_brands = models.CharField(db_column='CTNote', max_length=255, null=True, blank=True)
    _is_suspected_account = models.CharField(max_length=1, db_column='Confirm3st', blank=True)
    inactive_reason = models.CharField(max_length=30, db_column='InactiveReason', blank=True)
    is_paused = models.BooleanField(db_column='isPaused', default=False)
    last_purchase_date = models.DateTimeField(db_column='CTLastPurchaseDate', null=True, blank=True)
    is_encrypted = models.BooleanField(db_column='isEncrypted', default=False)
    new_my_pick_count = models.IntegerField(db_column='NewMyPickCount', null=False, default=0)

    @property
    def is_suspected_account(self):
        return True if self._is_suspected_account == 'Y' else False

    @is_suspected_account.setter
    def is_suspected_account(self, value):
        self._is_suspected_account = 'Y' if value else 'N'

    class Meta(AbstractUserModel.Meta):
        managed = False


####################
# USER INFORMATION #
####################
class DetailUserModel(models.Model):
    id = models.AutoField(primary_key=True, db_column='TBCustomerDetail_ID')
    user = models.ForeignKey('meta_db.UserModel',
                             null=False,
                             db_column='TBCustomer_ID',
                             to_field='customer_id',
                             on_delete=models.DO_NOTHING)
    avg_yearly_sales = models.IntegerField(db_column="AverageYearlySales")
    social_media_urls = models.CharField(db_column='SocialMediaURL', max_length=1024)
    years_business = models.SmallIntegerField(db_column='BusinessYears')
    primary_location = models.CharField(db_column='PrimaryPhysicalLocation', max_length=255)
    location_image = models.CharField(db_column='LocationImages', max_length=2048)
    main_collection = models.CharField(db_column='MainCollection', max_length=255)
    company_label = models.CharField(db_column='CompanyLabel', max_length=255)
    primary_source = models.CharField(db_column='PrimarySource', max_length=31)

    class Meta:
        managed = False
        db_table = 'TBCustomerDetail'


class ChargebackAccountAddresssModel(models.Model):
    id = models.AutoField(primary_key=True)
    customer_id = models.CharField(db_column='TBCustomer_ID', max_length=8)
    address = models.CharField(max_length=400)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'TBChargebackAccountAddresses'


class ChargebackAccountIPsModel(models.Model):
    id = models.AutoField(primary_key=True)
    customer_id = models.CharField(db_column='TBCustomer_ID', max_length=8)
    ip_address = models.CharField(max_length=50)
    access_count = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'TBChargebackAccountIPs'


class ChargebackSuspectedAccountsModel(models.Model):
    id = models.AutoField(primary_key=True)
    customer_id = models.CharField(db_column='TBCustomer_ID', max_length=8)
    associated_id = models.CharField(db_column='associated_id', max_length=8)
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=400)
    resale_id = models.CharField(max_length=100, blank=True, null=True)
    ip_address = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'TBChargebackSuspectedAccounts'


class UserResaleCertificate(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    customer = models.ForeignKey('meta_db.UserModel',
                                 null=False,
                                 db_column='TBCustomer_ID',
                                 to_field='customer_id',
                                 on_delete=models.DO_NOTHING)
    envelope_id = models.CharField(db_column='envelope_id', max_length=40)
    document_url = models.CharField(db_column='document_url', max_length=255)

    class Meta:
        managed = False
        db_table = 'TBCustomer_ResaleCertificate'


# JOB TITLE
class AbstractJobTitleModelManager(models.Manager):
    def all_active(self, **kwargs):
        return super(AbstractJobTitleModelManager, self).get_queryset().filter(_is_active='Y', **kwargs)


class AbstractJobTitleModel(models.Model):
    """
    USER JOB TITLE MODEL
    """
    id = models.AutoField(db_column='TBCustomerJobTitle_ID', primary_key=True)
    title = models.CharField(max_length=50, db_column='Title')
    _is_active = models.CharField(db_column='Active', max_length=1, default='Y')
    objects = AbstractJobTitleModelManager()

    def __str__(self):
        return self.title

    @property
    def is_active(self):
        return True if self._is_active == 'Y' else False

    @is_active.setter
    def is_active(self, value):
        self._is_active = 'Y' if value else 'N'

    def delete(self, *args, **kwargs):
        raise PreventDeleteException('please de-active instead delete')

    class Meta:
        abstract = True
        db_table = 'TBCustomerJobTitle'


class JobTitleModel(AbstractJobTitleModel):
    class Meta(AbstractJobTitleModel.Meta):
        managed = False


# SHIPPING ADDRESS
class AbstractUserShippingAddressModel(models.Model):
    id = models.AutoField(db_column='TBCustomerShippingAddressLists_ID', primary_key=True)
    for_brand_web = models.CharField(max_length=3,
                                     db_column='onVendor_ID',
                                     blank=True,
                                     help_text='brand id for brand web site orders')
    nick_name = models.CharField(max_length=50, db_column='NickName')
    company_name = models.CharField(max_length=50, db_column='MailCompanyName', blank=True)
    first_name = models.CharField(max_length=30, db_column='MailFirstName', blank=True)
    last_name = models.CharField(max_length=30, db_column='MailLastName', blank=True)
    # is_residential = models.CharField(max_length=1, db_column='IsResidential', blank=True)
    # ups_insurance = models.CharField(max_length=1, db_column='UPSinsurance', blank=True)
    address1 = models.CharField(max_length=100, db_column='MailAddress1')
    address2 = models.CharField(max_length=100, db_column='MailAddress2', blank=True)
    city = models.CharField(max_length=50, db_column='MailCity')
    state = models.CharField(max_length=50, db_column='MailStateOrProvince', blank=True)
    zipcode = models.CharField(max_length=50, db_column='MailZip')
    country = models.CharField(max_length=2, db_column='MailCountry', blank=True, help_text='country code')
    phone = models.CharField(max_length=50, db_column='MailPhone', blank=True)
    fax = models.CharField(max_length=50, db_column='MailFax', blank=True)
    # is_saved = models.CharField(max_length=1, db_column='Saved', default='N')
    created = models.DateTimeField(db_column='StartingDateTime', auto_now_add=True)
    # customershippingaddressprofileid = models.CharField(max_length=50, db_column='CustomerShippingAddressProfileID', blank=True)
    _is_default = models.CharField(max_length=1, db_column='nDefault', default='N', help_text='default address')

    @property
    def is_default(self):
        return True if self._is_default == 'Y' else False

    @is_default.setter
    def is_default(self, value):
        self._is_default = 'Y' if value else 'N'

    class Meta:
        abstract = True
        db_table = 'TBCustomerShippingAddressLists'


class UserShippingAddressModel(AbstractUserShippingAddressModel):
    user = models.ForeignKey('UserModel',
                             db_column='TBCustomer_ID',
                             to_field='customer_id',
                             on_delete=models.DO_NOTHING,
                             related_name='shipping_addresses')

    class Meta(AbstractUserShippingAddressModel.Meta):
        managed = False


class AbstractCountryListModelManager(models.Manager):
    def all_active(self):
        return super(AbstractCountryListModelManager, self).get_queryset().filter(is_active=True)


# COUNTRY LIST
class CountryListModel(models.Model):
    """
    READ ONLY MODEL
    """
    id = models.IntegerField(db_column='CountryID')
    name = models.CharField(max_length=50, db_column='CountryName')
    code = models.CharField(max_length=10, db_column='CountryCode', primary_key=True)
    currency_name = models.CharField(max_length=50, db_column='CurrencyName', blank=True)
    currency_code = models.CharField(max_length=10, db_column='CurrencyCode', blank=True)
    # country_group = models.CharField(max_length=50, db_column='CountryGroup', blank=True)
    # starting_date = models.DateTimeField(db_column='StartingDate')
    is_active = models.NullBooleanField(db_column='Active', default=True)
    objects = AbstractCountryListModelManager()

    def __unicode__(self):
        return '%s %s' % (self.name, self.code)

    def __str__(self):
        return '%s %s' % (self.name, self.code)

    def save(self, *args, **kwargs):
        raise PreventSaveException('cannot save read only model')

    def delete(self, *args, **kwargs):
        raise PreventDeleteException('cannot delete read only model')

    class Meta:
        managed = False
        db_table = 'TBCountryLists'


# ZIP CODE
class ZipCodeListModel(models.Model):
    """
    READ ONLY MODEL
    """
    zipcode = models.CharField(primary_key=True, max_length=255, db_column='zip')
    type = models.CharField(max_length=255, blank=True, null=True, db_column='type')
    primary_city = models.CharField(max_length=255, blank=True, null=True, db_column='primary_city')
    state = models.CharField(max_length=255, blank=True, null=True, db_column='state')
    county = models.CharField(max_length=255, blank=True, null=True, db_column='county')
    timezone = models.CharField(max_length=255, blank=True, null=True, db_column='timezone')
    area_codes = models.FloatField(blank=True, null=True, db_column='area_codes')
    latitude = models.FloatField(blank=True, null=True, db_column='latitude')
    longitude = models.FloatField(blank=True, null=True, db_column='longitude')
    world_region = models.CharField(max_length=255, blank=True, null=True, db_column='world_region')
    country = models.CharField(max_length=255, blank=True, null=True, db_column='country')

    def save(self, *args, **kwargs):
        raise PreventSaveException('cannot save read only model')

    def delete(self, *args, **kwargs):
        raise PreventDeleteException('cannot delete read only model')

    class Meta:
        managed = False
        db_table = 'zip_code_database'


#########################
# PAYMENT - CREDIT CARD #
#########################
class AbstractUserCreditCardModel(models.Model):
    id = models.AutoField(db_column='TBCustomerPaymentInfoLists_ID', primary_key=True)
    card_nickname = models.CharField(max_length=50,
                                     db_column='BillingCompanyName',
                                     blank=True,
                                     help_text='card nick name')
    first_name = models.CharField(max_length=30, db_column='BillingFirstName', blank=True)
    last_name = models.CharField(max_length=30, db_column='BillingLastName', blank=True)
    address1 = models.CharField(max_length=200, db_column='BillingAddress1', blank=True)
    address2 = models.CharField(max_length=200, db_column='BillingAddress2', blank=True)
    city = models.CharField(max_length=50, db_column='BillingCity', blank=True)
    state = models.CharField(max_length=50, db_column='BillingStateOrProvince', blank=True)
    zipcode = models.CharField(max_length=50, db_column='BillingZip', blank=True)
    country = models.CharField(max_length=50, db_column='BillingCountry', blank=True)
    phone_number = models.CharField(max_length=50, db_column='BillingPhone', blank=True)
    card_type = models.CharField(max_length=50, db_column='CardType', blank=True)
    card_number = models.CharField(max_length=4, db_column='CardNumber', blank=True)
    card_expire_month = models.CharField(max_length=2, db_column='CardExpireMonth', blank=True)
    card_expire_year = models.CharField(max_length=4, db_column='CardExpireYear', blank=True)
    is_default = models.BooleanField(max_length=1, db_column='nDefault', default=False)
    payment_profile_id = models.CharField(max_length=50, db_column='CustomerPaymentProfileID', unique=True, blank=True)
    is_valid = models.BooleanField(max_length=1, db_column='is_valid', default=True)
    created = models.DateTimeField(auto_now_add=True, db_column='StartingDateTime')
    modified = models.DateTimeField(auto_now=True, db_column='UpdatedDateTime')
    authorization_form = models.CharField(max_length=200, db_column='AuthorizationForm', blank=True)
    photo_id = models.CharField(max_length=200, db_column='PhotoID', blank=True)

    def __unicode__(self):
        return self.card_nickname

    @property
    def card_expire(self):
        return "%s/%s" % (self.card_expire_month, self.card_expire_year)

    @property
    def is_expired(self):
        if datetime.date.today() > datetime.date(
                int(self.card_expire_year), int(self.card_expire_month),
                calendar.monthrange(int(self.card_expire_year), int(self.card_expire_month))[1]):
            return True
        else:
            return False

    @property
    def formatted_address(self):
        return "%s %s %s, %s %s %s" % (self.address1, self.address2, self.city, self.state, self.zipcode, self.country)

    class Meta:
        abstract = True
        db_table = 'TBCustomerPaymentInfoLists'


class UserCreditCardModel(AbstractUserCreditCardModel):
    user = models.ForeignKey('meta_db.UserModel',
                             db_column='TBCustomer_ID',
                             max_length=8,
                             to_field='customer_id',
                             on_delete=models.DO_NOTHING,
                             related_name='credit_cards')

    @property
    def nick_name(self):
        return self.card_nickname

    class Meta(AbstractUserCreditCardModel.Meta):
        managed = False


class CreditCardAuthorizationFormModel(models.Model):
    id = models.OneToOneField('meta_db.UserCreditCardModel',
                              db_column='payment_profile_id',
                              to_field='payment_profile_id',
                              related_name='auth_docs',
                              primary_key=True,
                              on_delete=models.DO_NOTHING)
    customer_id = models.ForeignKey('meta_db.UserModel',
                                    db_column='customer_id',
                                    to_field='customer_id',
                                    on_delete=models.DO_NOTHING)
    authorization_form = models.FileField()
    cc_front = models.FilePathField()
    cc_back = models.FilePathField()
    photo_id = models.FilePathField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    confirmed = models.BooleanField(default=False)
    status = models.CharField(max_length=10, default='New', blank=True, null=True)
    reason = models.CharField(max_length=512, blank=True, null=True)
    review_item = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'TBCreditCardAuthorizationForm'


class LoginLog(models.Model):
    logid = models.AutoField(db_column=u'LogID', primary_key=True)
    companyid = models.BigIntegerField(null=True, db_column=u'CompanyID', blank=True, default=1)
    brand_id = models.CharField(max_length=3, db_column=u'onVendor_ID', blank=True, null=True)
    logtype = models.SmallIntegerField(null=True, db_column=u'LogType', blank=True, default=1)
    user_id = models.BigIntegerField(null=True, db_column=u'ID', blank=True)
    loginid = models.CharField(max_length=50, db_column=u'LoginID', blank=True)
    logindate = models.CharField(max_length=50, db_column=u'LoginDate', blank=True)
    logindatetime = models.DateTimeField(null=True, db_column=u'LoginDateTime', blank=True)
    computername = models.CharField(max_length=255, db_column=u'ComputerName', blank=True)
    ip_address = models.CharField(max_length=50, db_column=u'IP_Address', blank=True)
    ip_country = models.CharField(max_length=255, db_column=u'IP_Country', blank=True)
    user_agent = models.CharField(max_length=1000, db_column=u'User_Agent', blank=True)
    # ip_trace_country = models.CharField(max_length=255, db_column=u'IP_Trace_Country', blank=True)
    # ip_trace_country_code = models.CharField(max_length=10, db_column=u'IP_Trace_Country_Code', blank=True)
    # ip_trace_state_code = models.CharField(max_length=10, db_column=u'IP_Trace_State_Code', blank=True)
    # ip_trace_state = models.CharField(max_length=50, db_column=u'IP_Trace_State', blank=True)
    # ip_trace_city = models.CharField(max_length=255, db_column=u'IP_Trace_City', blank=True)
    # ip_trace_service = models.CharField(max_length=255, db_column=u'IP_Trace_Service', blank=True)
    # ip_trace_zip = models.CharField(max_length=10, db_column=u'IP_Trace_Zip', blank=True)
    # ip_trace_latitude = models.CharField(max_length=20, db_column=u'IP_Trace_Latitude', blank=True)
    # ip_trace_longitude = models.CharField(max_length=20, db_column=u'IP_Trace_Longitude', blank=True)
    # ip_trace_ip = models.CharField(max_length=50, db_column=u'IP_Trace_IP', blank=True)
    oniscustomer = models.CharField(max_length=1, db_column=u'OnisCustomer', blank=True, default='N')
    locationfromip = models.CharField(max_length=1000, db_column=u'LocationFromIP', blank=True)

    class Meta:
        managed = False
        db_table = u'LoginLog'
