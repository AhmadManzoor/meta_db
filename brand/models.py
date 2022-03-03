from __future__ import unicode_literals

from django.db import models
from meta_db.exceptions import PreventDeleteException


###########################
# Fulfillment - ship from #
###########################


class AbstractFulfillmentModel(models.Model):
    """
    FULFILLMENT MODEL as ship from
    """
    id = models.AutoField(db_column='id', primary_key=True)
    fulfillment = models.CharField(db_column='ShipFrom', unique=True, max_length=50)
    free_shipping_amt = models.DecimalField(db_column='FreeShippingAmount', max_digits=18,
                                            decimal_places=0, blank=True, null=True)
    discount_amt = models.IntegerField(db_column='AmountDiscount', blank=True, null=True)
    discount_percentage = models.IntegerField(db_column='AmountDiscountPercentage', blank=True, null=True)
    min_discount_amt = models.DecimalField(db_column='AmountDiscountMinimumAmount',
                                           max_digits=18, decimal_places=0, blank=True, null=True)
    min_order_amt = models.DecimalField(db_column='InvMinAmount', max_digits=18,
                                        decimal_places=0, blank=True, null=True)
    address1 = models.CharField(db_column='address1', max_length=1000, blank=True, null=True)
    address2 = models.CharField(db_column='address2', max_length=1000, blank=True, null=True)
    city = models.CharField(db_column='city', max_length=500, blank=True, null=True)
    state = models.CharField(db_column='state', max_length=10, blank=True, null=True)
    zipcode = models.CharField(db_column='zipcode', max_length=10, blank=True, null=True)
    country = models.CharField(db_column='countrycode', max_length=10, blank=True, null=True)
    telephone = models.TextField(db_column='tel', blank=True, null=True)
    is_active = models.BooleanField(db_column='is_active', default=True)

    def delete(self, *args, **kwargs):
        raise PreventDeleteException('cannot delete %s' % self)

    class Meta:
        abstract = True
        ordering = ('fulfillment',)
        db_table = 'TBShipFrom'


class FulfillmentModel(AbstractFulfillmentModel):
    pass

    class Meta(AbstractFulfillmentModel.Meta):
        managed = False


##################
# Brand Category #
##################


class AbstractBrandCategoryModelManager(models.Manager):
    def all_active(self):
        return super(AbstractBrandCategoryModelManager, self).get_queryset().filter(_is_deleted='N')


class AbstractBrandCategoryModel(models.Model):
    """
    BRAND CATEGORY MODEL
    brand set their own categories
    should change id as auto increment - change DB
    """
    id = models.AutoField(db_column='TBVendorOwnCategory_ID', primary_key=True)
    name = models.CharField(max_length=50, db_column='CategoryName', blank=True)
    sorting_order = models.IntegerField(db_column='SortingNoOnBrand', blank=True, null=True,
                                        help_text='ordering for brand')
    _is_added = models.CharField(max_length=1, db_column='nAdd', blank=True, help_text='for ARA')
    _is_updated = models.CharField(max_length=1, db_column='nUpdate', blank=True, help_text='for ARA')
    _is_deleted = models.CharField(max_length=1, db_column='nDelete', blank=True, help_text='for ARA')
    objects = AbstractBrandCategoryModelManager()

    # brand_collection = models.ForeignKey('os_db.StyleCollectionModel', db_column='TBVendorCollection_ID',
    #                                      blank=True, null=True)
    # style_category_id_1 = models.BigIntegerField(null=True, db_column='TBStyleNoCategory1_ID', blank=True)
    # style_category_id_2 = models.BigIntegerField(null=True, db_column='TBStyleNoCategory2_ID', blank=True)
    # style_os_collection_id = models.BigIntegerField(null=True, db_column='TBStyleNo_OS_Collection_ID', blank=True)

    @property
    def is_added(self):
        return True if self._is_added == 'Y' else False

    @is_added.setter
    def is_added(self, value):
        self._is_added = 'Y' if value else 'N'

    @property
    def is_updated(self):
        return True if self._is_updated == 'Y' else False

    @is_updated.setter
    def is_updated(self, value):
        self._is_updated = 'Y' if value else 'N'

    @property
    def is_deleted(self):
        return True if self._is_deleted == 'Y' else False

    @is_deleted.setter
    def is_deleted(self, value):
        self._is_deleted = 'Y' if value else 'N'

    def save(self, *args, **kwargs):
        """
        for ara, override save. SHOULD REMOVE LATER
        """
        if not self.pk:
            self._is_added = 'Y'
        else:
            self._is_updated = 'Y'
        super(AbstractBrandCategoryModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # TODO: for ara, override save. SHOULD REMOVE LATER
        if self.productmodel_set.exists():
            raise PreventDeleteException('cannot delete because one or more styles are assigned')
        else:
            self.is_deleted = True
            super(AbstractBrandCategoryModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True
        ordering = ('sorting_order', 'name',)
        unique_together = (('brand', 'name'),)
        db_table = 'TBVendorOwnCategory'


class BrandCategoryModel(AbstractBrandCategoryModel):
    brand = models.ForeignKey('BrandModel', db_column='TBVendor_ID', blank=True, related_name='brand_categories', on_delete=models.DO_NOTHING)
    os_master_category = models.ForeignKey('meta_db.StyleCategoryMasterModel',
                                           db_column='TBStyleNo_OS_Category_Master_ID',
                                           null=True, blank=True, help_text='matched it from os category', on_delete=models.DO_NOTHING)
    os_sub_category = models.ForeignKey('meta_db.StyleCategorySubModel', db_column='TBStyleNo_OS_Category_Sub_ID',
                                        null=True, blank=True, help_text='matched it from os category', on_delete=models.DO_NOTHING)

    class Meta(AbstractBrandCategoryModel.Meta):
        managed = False


#########
# Brand #
#########


class AbstractBrandModelManager(models.Manager):
    def all_active(self):
        return super(AbstractBrandModelManager, self).get_queryset().filter(_is_active='Y')


class AbstractBrandModel(models.Model):
    # _sql_id = models.IntegerField(db_column='TBVendor_SQL_ID')
    id = models.CharField(max_length=3, db_column='TBVendor_ID', primary_key=True)
    # size_chart_id = models.BigIntegerField(null=True, db_column='TBSizeChart_ID', blank=True)
    # pack_id = models.BigIntegerField(null=True, db_column='TBPackNo_ID', blank=True)
    name = models.CharField(max_length=50, db_column='VDName', help_text='brand name')
    brand_code = models.CharField(max_length=50, db_column='VDName2', help_text='to use user style name')
    web_name = models.CharField(max_length=50, db_column='VDWebName', blank=True, help_text='slug name')
    address = models.CharField(max_length=200, db_column='VDAddress', blank=True)
    address2 = models.CharField(max_length=200, db_column='VDAddress2', blank=True)
    city = models.CharField(max_length=50, db_column='VDCity', blank=True)
    state = models.CharField(max_length=15, db_column='VDState', blank=True)
    zipcode = models.CharField(max_length=12, db_column='VDZip', blank=True)
    phone = models.CharField(max_length=30, db_column='VDPhone', blank=True)
    fax = models.CharField(max_length=30, db_column='VDFax', blank=True)
    # email = models.CharField(max_length=50, db_column='VDEMail', blank=True, help_text='unknown')
    contact = models.CharField(max_length=30, db_column='VDContact', blank=True,
                               help_text='represent name')
    _is_active = models.CharField(db_column='VDActive', max_length=1, default='N')
    joined_date = models.DateTimeField(db_column='VDRegisterDate', auto_now_add=True, blank=True, null=True)
    brand_domain = models.CharField(max_length=100, db_column='TBVendor_Domain', blank=True,
                                    help_text='brand own website url')
    # contact_us = models.TextField(db_column='VDContactUs', blank=True) #This field type is a guess.
    email = models.CharField(max_length=50, db_column='VDVendorEmail', blank=True,
                             help_text='brand represent email')
    brand_url = models.CharField(db_column='VDVendorURL', blank=True, max_length=100, help_text='brand website')
    _brand_image = models.CharField(max_length=255, db_column='Brand_Rep_Image', blank=True, null=True)
    _bannerimg1 = models.TextField(db_column='BannerImg1', blank=True)
    _bannerimg2 = models.TextField(db_column='BannerImg2', blank=True)
    _bannerimg3 = models.TextField(db_column='BannerImg3', blank=True)
    _bannerimg4 = models.TextField(db_column='BannerImg4', blank=True)
    _bannerimg5 = models.TextField(db_column='BannerImg5', blank=True)
    _bannerimg6 = models.TextField(db_column='BannerImg6', blank=True, help_text='wide banner')
    _bannerimg7 = models.TextField(db_column='BannerImg7', blank=True)
    min_order_amt = models.DecimalField(decimal_places=4, null=True, max_digits=19,
                                        db_column='OSminOrderAMT', blank=True,
                                        help_text='minimum order at orangeshine.com')
    brand_segment = models.CharField(max_length=50, db_column='VDCategory',
                                     blank=True, help_text='brand products segment. just text')
    copy_prevention = models.BooleanField(db_column='copyprevention', default=1,
                                          help_text='hide items for anonymous')
    brand_description = models.TextField(db_column='OSDescription', blank=True)
    brand_price_range = models.IntegerField(null=True, db_column='VDPriceLevel', blank=True,
                                            help_text='brand price range')
    manufacture = models.CharField(max_length=50, db_column='VDMadeIn', blank=True,
                                   help_text='manufacture location')
    _is_paid_home = models.CharField(max_length=1, db_column='VDPaidDetail', blank=True,
                                     help_text='paid brand\'s home')
    brand_head_title = models.CharField(max_length=100, db_column='VDH1Tag', blank=True,
                                        help_text='brand title h1 table title')

    _joined_os_free_shipping = models.CharField(max_length=1, db_column='VDFSB', blank=True,
                                                help_text='join free shipping promotion on OS')
    os_commission = models.FloatField(null=True, db_column='VDDiscountFee', blank=True, default=0.0,
                                      help_text='OS Commission Rate')
    merchant_fee = models.FloatField(null=True, db_column='VDMerchantFee', blank=True, default=0.0,
                                     help_text='Credit Card & Paypal Fee Rate')
    objects = AbstractBrandModelManager()
    # vdcontactpreference = models.CharField(max_length=50, db_column='VDContactPreference', blank=True)
    # upsacct = models.CharField(max_length=50, db_column='UPSAcct', blank=True)
    # vdwhoshipping = models.CharField(max_length=50, db_column='VDWhoShipping', blank=True)
    # vdorderemail = models.CharField(max_length=1, db_column='VDOrderEmail', blank=True)
    # picturefee = models.DecimalField(decimal_places=4, null=True, max_digits=19, db_column='PictureFee', blank=True)
    # colorswatchfee = models.DecimalField(decimal_places=4, null=True, max_digits=19, db_column='ColorSwatchFee', blank=True)
    # vdpreorderactive = models.CharField(max_length=1, db_column='VDPreOrderActive', blank=True)
    # tbbrandvendor_id = models.CharField(max_length=3, db_column='TBBrandVendor_ID', blank=True)
    # tbmajormarket_id = models.CharField(max_length=50, db_column='TBMajorMarket_ID', blank=True)
    # africanamerican = models.CharField(max_length=1, db_column='AfricanAmerican', blank=True)
    # asianethnicities = models.CharField(max_length=1, db_column='AsianEthnicities', blank=True)
    # caucasian = models.CharField(max_length=1, db_column='Caucasian', blank=True)
    # latinamerican = models.CharField(max_length=1, db_column='LatinAmerican', blank=True)
    # middleeasternethnicity = models.CharField(max_length=1, db_column='MiddleEasternEthnicity', blank=True)
    # nativeamerican = models.CharField(max_length=1, db_column='NativeAmerican', blank=True)
    # pacificislandethnicity = models.CharField(max_length=1, db_column='PacificIslandEthnicity', blank=True)
    # vdconttitle = models.CharField(max_length=15, db_column='VDContTitle', blank=True)
    # fterm = models.CharField(max_length=10, db_column='fTerm', blank=True)
    # vdosvendor = models.CharField(max_length=1, db_column='VDOSVendor', blank=True)
    # vdrate1 = models.FloatField(null=True, db_column='VDRate1', blank=True)
    # vdrate2 = models.FloatField(null=True, db_column='VDRate2', blank=True)
    # vdrate3 = models.FloatField(null=True, db_column='VDRate3', blank=True)
    # vdcrate1 = models.FloatField(null=True, db_column='VDCRate1', blank=True)
    # vdcrate2 = models.FloatField(null=True, db_column='VDCRate2', blank=True)
    # vdcrate3 = models.FloatField(null=True, db_column='VDCRate3', blank=True)
    # vdimagefrontmain = models.CharField(max_length=200, db_column='VDImageFrontMain', blank=True)
    # vdimagevendormain = models.CharField(max_length=200, db_column='VDImageVendorMain', blank=True)
    # vdlogoimage = models.CharField(max_length=200, db_column='VDLogoImage', blank=True)
    # vdfrontimage = models.CharField(max_length=200, db_column='VDFrontImage', blank=True)
    # vdintroduction = models.TextField(db_column='VDIntroduction', blank=True) This field type is a guess.
    # vdfrontdescription = models.TextField(db_column='VDFrontDescription', blank=True) This field type is a guess.
    # vdwebusing = models.CharField(max_length=1, db_column='VDWebUsing', blank=True)
    # vdadminusing = models.CharField(max_length=1, db_column='VDAdminUsing', blank=True)
    # vdwebusingdomain = models.CharField(max_length=1, db_column='VDWebUsingDomain', blank=True)
    # vdowndomain = models.CharField(max_length=1, db_column='VDOwnDomain', blank=True)
    # tsalescounting = models.IntegerField(null=True, db_column='TSalesCounting', blank=True)
    # tnewarrivalcounting1 = models.IntegerField(null=True, db_column='TNewArrivalCounting1', blank=True)
    # tnewarrivalcounting2 = models.IntegerField(null=True, db_column='TNewArrivalCounting2', blank=True)
    # tnewarrivalcounting3 = models.IntegerField(null=True, db_column='TNewArrivalCounting3', blank=True)
    # tnewarrivalcounting4 = models.IntegerField(null=True, db_column='TNewArrivalCounting4', blank=True)
    # tbownwebsitemanage = models.CharField(max_length=1, db_column='TBOwnWebSiteManage', blank=True)
    # vdprivacypolicy = models.TextField(db_column='VDPrivacyPolicy', blank=True) This field type is a guess.
    # vdreturnpolicy = models.TextField(db_column='VDReturnPolicy', blank=True) This field type is a guess.
    # vdtermsofuse = models.TextField(db_column='VDTermsOfUse', blank=True) This field type is a guess.
    # vdyoutubeusing = models.TextField(db_column='VDYoutubeUsing', blank=True)
    # vdyoutubeurl = models.TextField(db_column='VDYoutubeURL', blank=True)
    # vdablogoon = models.TextField(db_column='VDABLogoOn', blank=True)
    # minimum_order_amount = models.DecimalField(decimal_places=2, null=True, max_digits=19,
    #                                            db_column='VDMinimumOrderAmount', blank=True)
    # vdwatermarkpositionx = models.CharField(max_length=50, db_column='VDWatermarkPositionx', blank=True)
    # vdwatermarkpositiony = models.CharField(max_length=50, db_column='VDWatermarkPositiony', blank=True)
    # vdwatermarktext = models.CharField(max_length=50, db_column='VDWatermarkText', blank=True)
    # vdwatermarkimage = models.CharField(max_length=50, db_column='VDWatermarkImage', blank=True)
    # vdwatermarkfont = models.CharField(max_length=50, db_column='VDWatermarkFont', blank=True)
    # vdwatermarkselect = models.CharField(max_length=50, db_column='VDWatermarkSelect', blank=True)
    # ndownload = models.CharField(max_length=1, db_column='nDownload', blank=True)
    # oniscustomer = models.CharField(max_length=1, db_column='OnisCustomer', blank=True)
    # vdregisteremailtitle = models.CharField(max_length=200, db_column='VDRegisterEmailTitle', blank=True)
    # vdregisteremailcontent = models.TextField(db_column='VDRegisterEmailContent', blank=True) This field type is a guess.
    # vdforgotemailtitle = models.CharField(max_length=200, db_column='VDForgotEmailTitle', blank=True)
    # vdforgotemailcontent = models.TextField(db_column='VDForgotEmailContent', blank=True) This field type is a guess.
    # vdpurchaseemailtitle = models.CharField(max_length=200, db_column='VDPurchaseEmailTitle', blank=True)
    # vdpurchaseemailcontent = models.TextField(db_column='VDPurchaseEmailContent', blank=True) This field type is a guess.
    # vdshipoutemailtitle = models.CharField(max_length=200, db_column='VDShipoutEmailTitle', blank=True)
    # vdshipoutemailcontent = models.TextField(db_column='VDShipoutEmailContent', blank=True) This field type is a guess.
    # vdapprovedemailtitle = models.CharField(max_length=200, db_column='VDApprovedEmailTitle', blank=True)
    # vdapprovedemailcontent = models.TextField(db_column='VDApprovedEmailContent', blank=True) This field type is a guess.
    # nallowsendosemail = models.CharField(max_length=1, db_column='nAllowSendOSEmail', blank=True)
    # vdownmanageorder = models.CharField(max_length=1, db_column='VDOwnManageOrder', blank=True)
    # tupdate = models.CharField(max_length=1, db_column='TUpdate', blank=True)
    # vdclass = models.CharField(max_length=1, db_column='VDClass')
    # authloginname = models.CharField(max_length=20, db_column='AuthLoginName', blank=True)
    # authtransactionkey = models.CharField(max_length=30, db_column='AuthTransactionKey', blank=True)
    # nhomepagelayout = models.CharField(max_length=1, db_column='nHomePageLayout', blank=True)
    # headbannerimagea_1 = models.CharField(max_length=100, db_column='HeadBannerImageA_1', blank=True)
    # headbannerimagea_2 = models.CharField(max_length=100, db_column='HeadBannerImageA_2', blank=True)
    # headbannerimagea_3 = models.CharField(max_length=100, db_column='HeadBannerImageA_3', blank=True)
    # headbannerimagea_4 = models.CharField(max_length=100, db_column='HeadBannerImageA_4', blank=True)
    # bannera_image1 = models.CharField(max_length=100, db_column='BannerA_Image1', blank=True)
    # bannera_image2 = models.CharField(max_length=100, db_column='BannerA_Image2', blank=True)
    # bannera_image3 = models.CharField(max_length=100, db_column='BannerA_Image3', blank=True)
    # bannerb_image1 = models.CharField(max_length=100, db_column='BannerB_Image1', blank=True)
    # bannerb_image2 = models.CharField(max_length=100, db_column='BannerB_Image2', blank=True)
    # ncolorscheme = models.CharField(max_length=1, db_column='nColorScheme', blank=True)
    # headbannerimagec_1 = models.CharField(max_length=100, db_column='HeadBannerImageC_1', blank=True)
    # ccverifycode = models.CharField(max_length=50, db_column='CCVerifyCode', blank=True)
    # enabledownloadpicture = models.CharField(max_length=1, db_column='EnableDownloadPicture')
    # featuredbrand = models.CharField(max_length=1, db_column='FeaturedBrand')

    def __unicode__(self):
        return "%s %s" % (self.id, self.name)

    @property
    def is_active(self):
        return True if self._is_active != 'N' else False

    @is_active.setter
    def is_active(self, value):
        self._is_active = 'Y' if value else 'N'

    @property
    def banners(self):
        """
        Brand banners. SHOULD CHANGE KEYS
        """
        return dict(
            brand=self._brand_image,
            banner1=self._bannerimg1,
            banner2=self._bannerimg2,
            banner3=self._bannerimg3,
            banner4=self._bannerimg4,
            banner5=self._bannerimg5,
            banner6=self._bannerimg6,
            banner7=self._bannerimg7,
        )

    @property
    def is_paid_home(self):
        return True if self._is_paid_home == 'Y' else False

    @is_paid_home.setter
    def is_paid_home(self, value):
        self._is_paid_home = 'Y' if value else 'N'

    @property
    def joined_os_free_shipping(self):
        return True if self._joined_os_free_shipping == 'Y' else False

    @joined_os_free_shipping.setter
    def joined_os_free_shipping(self, value):
        self._joined_os_free_shipping = 'Y' if value else 'N'

    def delete(self, *args, **kwargs):
        raise PreventDeleteException('cannot delete brand')

    class Meta:
        abstract = True
        db_table = 'TBVendor'


class BrandModel(AbstractBrandModel):
    fulfillment = models.ForeignKey('FulfillmentModel', db_column='ShippedFrom', to_field='fulfillment', blank=True, on_delete=models.DO_NOTHING)
    style_collection = models.ForeignKey('meta_db.StyleCollectionModel', db_column='TBStyleNo_OS_Collection_ID',
                                         help_text='style collection for item but use brand as well', blank=True,
                                         null=True, on_delete=models.DO_NOTHING)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.id = '%02d' % (int(BrandModel.objects.order_by('id').last().pk) + 1,)
        super(AbstractBrandModel, self).save(*args, **kwargs)

    class Meta(AbstractBrandModel.Meta):
        managed = False
        ordering = ['name']
