from __future__ import unicode_literals

from django.db import models
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS

from meta_db.exceptions import PreventDeleteException


##############
# SIZE CHART #
##############
class AbstractSizeChartQuantityModel(models.Model):
    """
        size chart information with number of size. EXCEPT SHOES
        NUMBER OF EACH SIZE
        List Length: 13
        Example: 1,2,3,4,0,0,0,0,0,0,0
        """
    id = models.AutoField(db_column='TBPackNo_ID', primary_key=True)
    name = models.CharField(max_length=10, db_column='dPackNoName')
    description = models.CharField(max_length=50,
                                   db_column='dPackNoDescription',
                                   blank=True)
    d1p = models.SmallIntegerField(db_column='d01P', default=0)
    d2p = models.SmallIntegerField(db_column='d02P', default=0)
    d3p = models.SmallIntegerField(db_column='d03P', default=0)
    d4p = models.SmallIntegerField(db_column='d04P', default=0)
    d5p = models.SmallIntegerField(db_column='d05P', default=0)
    d6p = models.SmallIntegerField(db_column='d06P', default=0)
    d7p = models.SmallIntegerField(db_column='d07P', default=0)
    d8p = models.SmallIntegerField(db_column='d08P', default=0)
    d9p = models.SmallIntegerField(db_column='d09P', default=0)
    d10p = models.SmallIntegerField(db_column='d010P', default=0)
    d11p = models.SmallIntegerField(db_column='d011P', default=0)
    d12p = models.SmallIntegerField(db_column='d012P', default=0)
    d13p = models.SmallIntegerField(db_column='d013P', default=0)

    # size_and_pack = models.CharField(max_length=50, db_column='SizeAndPack', blank=True)

    @property
    def qty_list(self):
        _tmp_list = [
            'd1p', 'd2p', 'd3p', 'd4p', 'd5p', 'd6p', 'd7p', 'd8p', 'd9p',
            'd10p', 'd11p', 'd12p', 'd13p'
        ]
        _qty_list = []
        for i in _tmp_list:
            if getattr(self, i) or not getattr(self, i) == '':
                try:
                    _qty_list.append(int(getattr(self, i)))
                except ValueError:
                    pass
        return _qty_list

    @qty_list.setter
    def qty_list(self, values):
        _tmp_list = [
            'd1p', 'd2p', 'd3p', 'd4p', 'd5p', 'd6p', 'd7p', 'd8p', 'd9p',
            'd10p', 'd11p', 'd12p', 'd13p'
        ]
        if len(values) > len(_tmp_list):
            raise ValueError('max size list is %s' % len(_tmp_list))
        for i in _tmp_list:
            setattr(self, i, 0)
        for i, v in zip(_tmp_list, values):
            setattr(self, i, int(v))

    def delete(self, *args, **kwargs):
        raise PreventDeleteException('cannot delete this model')

    class Meta:
        abstract = True
        db_table = 'TBPackNo'


class SizeChartQuantityModel(AbstractSizeChartQuantityModel):
    class Meta(AbstractSizeChartQuantityModel.Meta):
        managed = False


class AbstractSizeChartLabelModel(models.Model):
    """
    size chart information of size name. EXCEPT SHOES
    NAME OF EACH SIZE
    List Length: 13
    Example: S, M, L
    """
    id = models.AutoField(db_column='TBSizeChart_ID', primary_key=True)
    name = models.CharField(max_length=50, db_column='dSizeName')
    description = models.CharField(max_length=50,
                                   db_column='dSizeDescription',
                                   blank=True)
    d1s = models.CharField(max_length=10, db_column='d01S', blank=True)
    d2s = models.CharField(max_length=10, db_column='d02S', blank=True)
    d3s = models.CharField(max_length=10, db_column='d03S', blank=True)
    d4s = models.CharField(max_length=10, db_column='d04S', blank=True)
    d5s = models.CharField(max_length=10, db_column='d05S', blank=True)
    d6s = models.CharField(max_length=10, db_column='d06S', blank=True)
    d7s = models.CharField(max_length=10, db_column='d07S', blank=True)
    d8s = models.CharField(max_length=10, db_column='d08S', blank=True)
    d9s = models.CharField(max_length=10, db_column='d09S', blank=True)
    d10s = models.CharField(max_length=10, db_column='d010S', blank=True)
    d11s = models.CharField(max_length=10, db_column='d011S', blank=True)
    d12s = models.CharField(max_length=10, db_column='d012S', blank=True)
    d13s = models.CharField(max_length=10, db_column='d013S', blank=True)

    # size_and_pack = models.CharField(max_length=50, db_column='SizeAndPack', blank=True)

    @property
    def size_list(self):
        _tmp_list = [
            'd1s', 'd2s', 'd3s', 'd4s', 'd5s', 'd6s', 'd7s', 'd8s', 'd9s',
            'd10s', 'd11s', 'd12s', 'd13s'
        ]
        return [getattr(self, i) for i in _tmp_list if getattr(self, i)]

    @size_list.setter
    def size_list(self, values):
        _tmp_list = [
            'd1s', 'd2s', 'd3s', 'd4s', 'd5s', 'd6s', 'd7s', 'd8s', 'd9s',
            'd10s', 'd11s', 'd12s', 'd13s'
        ]
        if len(values) > len(_tmp_list):
            raise ValueError('max size list is %s' % len(_tmp_list))
        for i in _tmp_list:
            setattr(self, i, None)
        for i, v in zip(_tmp_list, values):
            setattr(self, i, v)

    def delete(self, *args, **kwargs):
        raise PreventDeleteException('cannot delete this model')

    class Meta:
        abstract = True
        db_table = 'TBSizeChart'


class SizeChartLabelModel(AbstractSizeChartLabelModel):
    class Meta(AbstractSizeChartLabelModel.Meta):
        managed = False


class AbstractShoeSizeChartModel(models.Model):
    """
    Shoes size chart scaffold
    List Length: 16
    Example: [1, 0, 0, 0, 1, 1, 3, 4, 7, 1, 2, 0, 0, 0, 0, 1]
    """
    id = models.AutoField(db_column='TBVendorShoeSize_ID', primary_key=True)
    name = models.CharField(max_length=50,
                            db_column='ShoeSizeName',
                            blank=True)
    description = models.CharField(max_length=50,
                                   db_column='Description',
                                   blank=True)
    s5 = models.SmallIntegerField(db_column='S5', default=0)
    s5h = models.SmallIntegerField(db_column='S5h', default=0)
    s6 = models.SmallIntegerField(db_column='S6', default=0)
    s6h = models.SmallIntegerField(db_column='S6h', default=0)
    s7 = models.SmallIntegerField(db_column='S7', default=0)
    s7h = models.SmallIntegerField(db_column='S7h', default=0)
    s8 = models.SmallIntegerField(db_column='S8', default=0)
    s8h = models.SmallIntegerField(db_column='S8h', default=0)
    s9 = models.SmallIntegerField(db_column='S9', default=0)
    s9h = models.SmallIntegerField(db_column='S9h', default=0)
    s10 = models.SmallIntegerField(db_column='S10', default=0)
    s10h = models.SmallIntegerField(db_column='S10h', default=0)
    s11 = models.SmallIntegerField(db_column='S11', default=0)
    s11h = models.SmallIntegerField(db_column='S11h', default=0)
    s12 = models.SmallIntegerField(db_column='S12', default=0)
    s12h = models.SmallIntegerField(db_column='S12h', default=0)

    @property
    def shoe_size_chart_label(self):
        return [
            '5', '5.5', '6', '6.5', '7', '7.5', '8', '8.5', '9', '9.5', '10',
            '10.5', '11', '11.5', '12', '12.5'
        ]

    @property
    def shoe_size_chart(self):
        _tmp_list = [
            's5', 's5h', 's6', 's6h', 's7', 's7h', 's8', 's8h', 's9', 's9h',
            's10', 's10h', 's11', 's11h', 's12', 's12h'
        ]
        _size_list = []
        for i in _tmp_list:
            try:
                _size_list.append(int(getattr(self, i)))
            except ValueError:
                _size_list.append(0)
        return _size_list

    @shoe_size_chart.setter
    def shoe_size_chart(self, values):
        _tmp_list = [
            's5', 's5h', 's6', 's6h', 's7', 's7h', 's8', 's8h', 's9', 's9h',
            's10', 's10h', 's11', 's11h', 's12', 's12h'
        ]
        if len(values) != len(self.shoe_size_chart_label):
            raise ValueError('shoe size run list length is %s' %
                             (len(self.shoe_size_chart_label), ))
        for i, v in zip(_tmp_list, values):
            setattr(self, i, v)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.validate_unique()
        super(AbstractShoeSizeChartModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # PLEASE CHECK CONDITION
        raise PreventDeleteException('cannot delete this model')

    class Meta:
        abstract = True
        db_table = 'TBVendorShoeSize'


class ShoeSizeChartModel(AbstractShoeSizeChartModel):
    brand = models.ForeignKey('meta_db.BrandModel',
                              db_column='TBVendor_ID',
                              blank=True,
                              on_delete=models.DO_NOTHING,
                              related_name='brand_all_shoe_size')

    def validate_unique(self, exclude=None):
        if self.__class__.objects.filter(name=self.name,
                                         brand=self.brand).exists():
            raise ValidationError({
                NON_FIELD_ERRORS: [
                    'Shoe size chart name already exists.',
                ],
            })

    class Meta(AbstractShoeSizeChartModel.Meta):
        managed = False


class AbstractSelectedShoeSizeChartModel(models.Model):
    """
    Shoes Size Chart selected by style
    ManyToMany model of ShoeSizeChartModel and ProductModel
    """
    id = models.AutoField(db_column='TBVendorShoeSizeSelect_ID',
                          primary_key=True)
    item = models.ForeignKey('meta_db.ProductModel',
                             db_column='TBItem_ID',
                             on_delete=models.DO_NOTHING)

    class Meta:
        abstract = True
        db_table = 'TBVendorShoeSizeSelect'


class SelectedShoeSizeChartModel(AbstractSelectedShoeSizeChartModel):
    class Meta(AbstractSelectedShoeSizeChartModel.Meta):
        managed = False


##########################################
# COLLECTION AND OTHER STYLE INFORMATION #
##########################################
# COLLECTION
class AbstractStyleCollectionModel(models.Model):
    """
    OS COLLECTION MODEL
    used to define collection on style and brand
    DO NOT HAVE SELECTION TABLE used as inline filed on os style table
    SHOULD CHANGE TO USE COLLECTION SELECTED TABLE
    """
    id = models.AutoField(db_column='TBStyleNo_OS_Collection_ID',
                          primary_key=True)
    name = models.CharField(db_column='CollectionName', max_length=50)
    description = models.CharField(db_column='Description',
                                   max_length=300,
                                   blank=True,
                                   null=True)
    is_active = models.BooleanField(db_column='Active', default=True)

    def delete(self, *args, **kwargs):
        self.is_active = False
        super(AbstractStyleCollectionModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True
        db_table = 'TBStyleNo_OS_Collection'


class StyleCollectionModel(AbstractStyleCollectionModel):
    class Meta(AbstractStyleCollectionModel.Meta):
        managed = False


# STYLE
class AbstractProductInfoStyleModel(models.Model):
    """
    for advanced filter and describe products
    DELETE POLICY
    """
    id = models.AutoField(db_column='TBStyleNo_OS_Style_ID', primary_key=True)
    name = models.CharField(db_column='StyleName',
                            max_length=50,
                            blank=True,
                            null=True)
    description = models.CharField(db_column='Description',
                                   max_length=50,
                                   blank=True,
                                   null=True)
    is_active = models.NullBooleanField(db_column='Active')

    def delete(self, *args, **kwargs):
        raise PreventDeleteException('cannot delete this model')

    class Meta:
        abstract = True
        db_table = 'TBStyleNo_OS_Style'


class ProductInfoStyleModel(AbstractProductInfoStyleModel):
    class Meta(AbstractProductInfoStyleModel.Meta):
        managed = False


class AbstractProductInfoStyleSelectedModel(models.Model):
    """
    PRODUCT STYLE SELECTION
    """
    id = models.AutoField(db_column='TBStyleNo_OS_StyleSelect_ID',
                          primary_key=True)

    # nadd = models.CharField(db_column='nAdd', max_length=1, blank=True, null=True)
    # ndelete = models.CharField(db_column='nDelete', max_length=1, blank=True, null=True)

    class Meta:
        abstract = True
        db_table = 'TBStyleNo_OS_StyleSelect'


class ProductInfoStyleSelectedModel(AbstractProductInfoStyleSelectedModel):
    item = models.ForeignKey('meta_db.StyleListModel',
                             db_column='TBItem_ID',
                             max_length=8,
                             on_delete=models.DO_NOTHING,
                             related_name='pi_style_item')
    style = models.ForeignKey('ProductInfoStyleModel',
                              db_column='TBStyleNo_OS_Style_ID',
                              on_delete=models.DO_NOTHING,
                              related_name='pi_style')

    class Meta(AbstractProductInfoStyleSelectedModel.Meta):
        managed = False


# PATTERN
class AbstractProductInfoPatternModel(models.Model):
    id = models.AutoField(db_column='TBStyleNo_OS_Pattern_ID',
                          primary_key=True)
    name = models.CharField(db_column='PatternName',
                            max_length=50,
                            blank=True,
                            null=True)
    description = models.CharField(db_column='Description',
                                   max_length=50,
                                   blank=True,
                                   null=True)
    is_active = models.NullBooleanField(db_column='Active')

    class Meta:
        abstract = True
        db_table = 'TBStyleNo_OS_Pattern'


class ProductInfoPatternModel(AbstractProductInfoPatternModel):
    class Meta(AbstractProductInfoPatternModel.Meta):
        managed = False


class AbstractProductInfoPatternSelectedModel(models.Model):
    id = models.AutoField(db_column='TBStyleNo_OS_PatternSelect_ID',
                          primary_key=True)

    # nadd = models.CharField(db_column='nAdd', max_length=1, blank=True, null=True)
    # ndelete = models.CharField(db_column='nDelete', max_length=1, blank=True, null=True)

    class Meta:
        abstract = True
        db_table = 'TBStyleNo_OS_PatternSelect'


class ProductInfoPatternSelectedModel(AbstractProductInfoPatternSelectedModel):
    item = models.ForeignKey('ProductModel',
                             db_column='TBItem_ID',
                             max_length=8,
                             on_delete=models.DO_NOTHING,
                             related_name='pi_pattern_item')
    pattern = models.ForeignKey('ProductInfoPatternModel',
                                db_column='TBStyleNo_OS_Pattern_ID',
                                on_delete=models.DO_NOTHING,
                                related_name='pi_pattern')

    class Meta(AbstractProductInfoPatternSelectedModel.Meta):
        managed = False


# SLEEVE
class AbstractProductInfoSleeveModel(models.Model):
    id = models.AutoField(db_column='TBStyleNo_OS_Sleeve_ID', primary_key=True)
    name = models.CharField(db_column='SleeveName',
                            max_length=50,
                            blank=True,
                            null=True)
    description = models.CharField(db_column='Description',
                                   max_length=50,
                                   blank=True,
                                   null=True)
    is_active = models.NullBooleanField(db_column='Active')

    class Meta:
        abstract = True
        db_table = 'TBStyleNo_OS_Sleeve'


class ProductInfoSleeveModel(AbstractProductInfoSleeveModel):
    class Meta(AbstractProductInfoSleeveModel.Meta):
        managed = False


class AbstractProductInfoSleeveSelectedModel(models.Model):
    id = models.AutoField(db_column='TBStyleNo_OS_SleeveSelect_ID',
                          primary_key=True)

    # nadd = models.CharField(db_column='nAdd', max_length=1, blank=True, null=True)
    # ndelete = models.CharField(db_column='nDelete', max_length=1, blank=True, null=True)

    class Meta:
        abstract = True
        db_table = 'TBStyleNo_OS_SleeveSelect'


class ProductInfoSleeveSelectedModel(AbstractProductInfoSleeveSelectedModel):
    item = models.ForeignKey('ProductModel',
                             db_column='TBItem_ID',
                             max_length=8,
                             on_delete=models.DO_NOTHING,
                             related_name='pi_sleeve_item')
    sleeve = models.ForeignKey('ProductInfoSleeveModel',
                               db_column='TBStyleNo_OS_Sleeve_ID',
                               on_delete=models.DO_NOTHING,
                               related_name='pi_sleeve')

    class Meta(AbstractProductInfoSleeveSelectedModel.Meta):
        managed = False


############
# OS STYLE #
############
class AbstractProductModelManager(models.Manager):
    def all_active(self):
        return super(AbstractProductModelManager,
                     self).get_queryset().filter(_is_active='Y')
    # @property
    # def os(self):
    #     return super().get_queryset().filter(is_cm=False)

    # @property
    # def cm(self):
    #     return super().get_queryset().filter(is_cm=True)




class AbstractProductModel(models.Model):
    id = models.CharField(max_length=8,
                          db_column='TBItem_ID',
                          primary_key=True)
    style_name = models.CharField(max_length=40,
                                  db_column='nStyleName',
                                  blank=True)
    grouped_item_code = models.CharField(max_length=12,
                                         db_column='nVendorBarItem',
                                         blank=True)
    os_style_number = models.CharField(max_length=30,
                                       db_column='nOurStyleNo',
                                       blank=True,
                                       help_text='style number for os')
    brand_style_number = models.CharField(max_length=30,
                                          db_column='nVendorStyleNo',
                                          blank=True,
                                          help_text='brand style number')
    # style_color_id = models.BigIntegerField(db_column='TBStyleNo_Color_ID', blank=True, null=True)
    # style_style_id = models.CharField(max_length=10, db_column='TBStyleNo_Style_ID',
    #                                   blank=True, help_text='depreciated. os_style_select')
    description = models.TextField(db_column='nItemDescription', blank=True)
    _is_active = models.CharField(max_length=1,
                                  db_column='nActive',
                                  default='Y')
    # _is_brand_active = models.CharField(max_length=1, db_column='nVendorActive', blank=True)
    _is_prepare = models.CharField(max_length=1,
                                   db_column='nPrepare',
                                   default='Y')
    purchase_price = models.DecimalField(
        decimal_places=2,
        null=True,
        max_digits=19,
        db_column='nPurchasePrice',
        blank=True,
        help_text='purchased priced from brand')
    os_price = models.DecimalField(decimal_places=2,
                                   null=True,
                                   max_digits=19,
                                   db_column='nPrice2',
                                   blank=True)
    _is_sale = models.CharField(max_length=1, db_column='nOnSale', default='N')
    os_sale_price = models.DecimalField(decimal_places=2,
                                        null=True,
                                        max_digits=19,
                                        db_column='nSalePrice2',
                                        blank=True)
    brand_shop_price = models.DecimalField(decimal_places=2,
                                           max_digits=19,
                                           db_column='nPrice1',
                                           default=0.00,
                                           help_text='brand shop price')
    brand_shop_sale_price = models.DecimalField(
        decimal_places=2,
        max_digits=19,
        db_column='nSalePrice1',
        default=0.00,
        help_text='brand shop sale price')
    sub_invoice_sale_price = models.DecimalField(
        decimal_places=2,
        null=True,
        max_digits=19,
        db_column='nSalePrice',
        blank=True,
        help_text=
        'if item is sale, input this number to sub invoice purchase price')
    created = models.DateTimeField(null=True,
                                   db_column='nDate',
                                   blank=True,
                                   auto_now_add=True)
    updated = models.DateTimeField(null=True,
                                   db_column='nModifyDate',
                                   blank=True,
                                   auto_now=True)
    # _is_sold_out = models.CharField(max_length=1, db_column='nSoldOut', default='N')
    # sold_out_updated = models.DateTimeField(null=True, db_column='nSoldOutUpdateDate', blank=True, auto_now=True)
    _is_restock = models.CharField(max_length=1,
                                   db_column='nReStock',
                                   default='N',
                                   help_text='restock item')
    restock_date = models.DateTimeField(null=True,
                                        db_column='nReStockDate',
                                        blank=True)
    _is_preorder = models.CharField(max_length=1,
                                    db_column='nPreOrder',
                                    default='N')
    preorder_available_date = models.DateTimeField(
        null=True, db_column='nPreOrderAvailableDate', blank=True)
    is_brand_only = models.BooleanField(
        db_column='is_brand_only',
        default=False,
        help_text='only sales in brand shop.if true, is_active should be false'
    )
    is_brand_only_active = models.BooleanField(
        db_column='is_brand_only_active',
        default=False,
        help_text='is brand only item active')
    pictures1 = models.CharField(max_length=100,
                                 db_column='PictureS1',
                                 blank=True)
    pictures2 = models.CharField(max_length=100,
                                 db_column='PictureS2',
                                 blank=True)
    pictures3 = models.CharField(max_length=100,
                                 db_column='PictureS3',
                                 blank=True)
    pictures4 = models.CharField(max_length=100,
                                 db_column='PictureS4',
                                 blank=True)
    pictures5 = models.CharField(max_length=100,
                                 db_column='PictureS5',
                                 blank=True)
    pictures6 = models.CharField(max_length=100,
                                 db_column='PictureS6',
                                 blank=True)
    pictures7 = models.CharField(max_length=100,
                                 db_column='PictureS7',
                                 blank=True)
    pictures8 = models.CharField(max_length=100,
                                 db_column='PictureS8',
                                 blank=True)
    pictures9 = models.CharField(max_length=100,
                                 db_column='PictureS9',
                                 blank=True)
    picturer1 = models.CharField(max_length=100,
                                 db_column='PictureR1',
                                 blank=True)
    picturer2 = models.CharField(max_length=100,
                                 db_column='PictureR2',
                                 blank=True)
    picturer3 = models.CharField(max_length=100,
                                 db_column='PictureR3',
                                 blank=True)
    picturer4 = models.CharField(max_length=100,
                                 db_column='PictureR4',
                                 blank=True)
    picturer5 = models.CharField(max_length=100,
                                 db_column='PictureR5',
                                 blank=True)
    picturer6 = models.CharField(max_length=100,
                                 db_column='PictureR6',
                                 blank=True)
    picturer7 = models.CharField(max_length=100,
                                 db_column='PictureR7',
                                 blank=True)
    picturer8 = models.CharField(max_length=100,
                                 db_column='PictureR8',
                                 blank=True)
    picturer9 = models.CharField(max_length=100,
                                 db_column='PictureR9',
                                 blank=True)
    picture1 = models.CharField(max_length=100,
                                db_column='Picture1',
                                blank=True)
    picture2 = models.CharField(max_length=100,
                                db_column='Picture2',
                                blank=True)
    picture3 = models.CharField(max_length=100,
                                db_column='Picture3',
                                blank=True)
    picture4 = models.CharField(max_length=100,
                                db_column='Picture4',
                                blank=True)
    picture5 = models.CharField(max_length=100,
                                db_column='Picture5',
                                blank=True)
    picture6 = models.CharField(max_length=100,
                                db_column='Picture6',
                                blank=True)
    picture7 = models.CharField(max_length=100,
                                db_column='Picture7',
                                blank=True)
    picture8 = models.CharField(max_length=100,
                                db_column='Picture8',
                                blank=True)
    picture9 = models.CharField(max_length=100,
                                db_column='Picture9',
                                blank=True)
    picturez1 = models.CharField(max_length=100,
                                 db_column='PictureZ1',
                                 blank=True)
    picturez2 = models.CharField(max_length=100,
                                 db_column='PictureZ2',
                                 blank=True)
    picturez3 = models.CharField(max_length=100,
                                 db_column='PictureZ3',
                                 blank=True)
    picturez4 = models.CharField(max_length=100,
                                 db_column='PictureZ4',
                                 blank=True)
    picturez5 = models.CharField(max_length=100,
                                 db_column='PictureZ5',
                                 blank=True)
    picturez6 = models.CharField(max_length=100,
                                 db_column='PictureZ6',
                                 blank=True)
    picturez7 = models.CharField(max_length=100,
                                 db_column='PictureZ7',
                                 blank=True)
    picturez8 = models.CharField(max_length=100,
                                 db_column='PictureZ8',
                                 blank=True)
    picturez9 = models.CharField(max_length=100,
                                 db_column='PictureZ9',
                                 blank=True)
    picturev1 = models.CharField(max_length=100,
                                 db_column='PictureV1',
                                 blank=True)
    picturev2 = models.CharField(max_length=100,
                                 db_column='PictureV2',
                                 blank=True)
    picturev3 = models.CharField(max_length=100,
                                 db_column='PictureV3',
                                 blank=True)
    picturev4 = models.CharField(max_length=100,
                                 db_column='PictureV4',
                                 blank=True)
    picturev5 = models.CharField(max_length=100,
                                 db_column='PictureV5',
                                 blank=True)
    picturev6 = models.CharField(max_length=100,
                                 db_column='PictureV6',
                                 blank=True)
    picturev7 = models.CharField(max_length=100,
                                 db_column='PictureV7',
                                 blank=True)
    picturev8 = models.CharField(max_length=100,
                                 db_column='PictureV8',
                                 blank=True)
    picturev9 = models.CharField(max_length=100,
                                 db_column='PictureV9',
                                 blank=True)
    popular_point = models.SmallIntegerField(db_column='popular_point',
                                             help_text='popular point')
    view_point = models.SmallIntegerField(db_column='view_point',
                                          help_text='most viewed')
    sales_point = models.SmallIntegerField(db_column='sales_point',
                                           help_text='most sales')
    _is_hidden = models.CharField(
        db_column='nHidden',
        blank=True,
        max_length=1,
        default='N',
        help_text='sold out and vendor want to hide items. technically deleted.'
    )
    origin_date = models.DateTimeField(db_column='OriginDate',
                                       null=True,
                                       blank=True,
                                       auto_now_add=True)
    publish_date = models.DateTimeField(db_column='PublishDate',
                                        null=True,
                                        blank=True)
    wait_callback = models.BooleanField(
        db_column='WaitCallback',
        default=False,
        help_text='true if waiting for callback for finishing style')
    is_broken_pack = models.BooleanField(db_column='is_broken_pack',
                                         blank=True,
                                         default=False)
    min_broken_pack_order_qty = models.SmallIntegerField(
        db_column='min_broken_pack_order_qty ',
        default=0,
        help_text='min qty for broken pack')
    objects = AbstractProductModelManager()
    # tbstylenocategory1_id = models.BigIntegerField(null=True, db_column='TBStyleNoCategory1_ID', blank=True)
    # tbstylenocategory2_id = models.BigIntegerField(null=True, db_column='TBStyleNoCategory2_ID', blank=True)
    # tbvendorcollection_id = models.BigIntegerField(null=True, db_column='TBVendorCollection_ID', blank=True)
    # tbrealvendor_id = models.CharField(max_length=3, db_column='TBRealVendor_ID', blank=True)
    # nourstyleno2 = models.CharField(max_length=30, db_column='nOurStyleNo2', blank=True)
    # nreportyesorno = models.CharField(max_length=3, db_column='nReportYesOrNo', blank=True)
    # npurchasediscountprice = models.DecimalField(decimal_places=2, null=True,
    #                                              max_digits=19, db_column='nPurchaseDiscountPrice', blank=True)
    # nmsrp = models.DecimalField(decimal_places=2, null=True, max_digits=19, db_column='nMSRP', blank=True)
    # nprice1 = models.DecimalField(decimal_places=2, null=True, max_digits=19, db_column='nPrice1', blank=True)
    # nprice3 = models.DecimalField(decimal_places=2, null=True, max_digits=19, db_column='nPrice3', blank=True)
    # nsaleprice1 = models.DecimalField(decimal_places=2, null=True, max_digits=19, db_column='nSalePrice1', blank=True)
    # nsaleprice3 = models.DecimalField(decimal_places=2, null=True, max_digits=19, db_column='nSalePrice3', blank=True)
    # navgprice = models.DecimalField(decimal_places=2, null=True, max_digits=19, db_column='nAvgPrice', blank=True)
    # nfirstpdate = models.DateTimeField(null=True, db_column='nFirstPDate', blank=True)
    # nlastpdate = models.DateTimeField(null=True, db_column='nLastPDate', blank=True)
    # nfirstsdate = models.DateTimeField(null=True, db_column='nFirstSDate', blank=True)
    # nlastsdate = models.DateTimeField(null=True, db_column='nLastSDate', blank=True)
    # nfirstpprice = models.DecimalField(decimal_places=2, null=True, max_digits=19, db_column='nFirstPPrice', blank=True)
    # nlastpprice = models.DecimalField(decimal_places=2, null=True, max_digits=19, db_column='nLastPPrice', blank=True)
    # nfirstsaleprice = models.DecimalField(decimal_places=2, null=True, max_digits=19, db_column='nFirstSalePrice', blank=True)
    # nlastsaleprice = models.DecimalField(decimal_places=2, null=True, max_digits=19, db_column='nLastSalePrice', blank=True)
    # navgcost = models.DecimalField(decimal_places=2, null=True, max_digits=19, db_column='nAvgCost', blank=True)
    # ndisc = models.CharField(max_length=5, db_column='nDISC', blank=True)
    # nbdiscountyesorno = models.NullBooleanField(null=True, db_column='nBDiscountYesOrNo', blank=True)
    # nfirstsaleprice1 = models.DecimalField(decimal_places=2, null=True, max_digits=19, db_column='nFirstSalePrice1', blank=True)
    # nfirstsaleprice2 = models.DecimalField(decimal_places=2, null=True, max_digits=19, db_column='nFirstSalePrice2', blank=True)
    # nfirstsaleprice3 = models.DecimalField(decimal_places=2, null=True, max_digits=19, db_column='nFirstSalePrice3', blank=True)
    # nweight = models.FloatField(null=True, db_column='nWeight', blank=True)
    # ncustomerreadcount = models.IntegerField(null=True, db_column='nCustomerReadCount', blank=True)
    # nisallpack = models.CharField(max_length=1, db_column='nIsAllPack', blank=True)
    # nsaledate = models.DateTimeField(null=True, db_column='nSaleDate', blank=True)
    # nvendorsaleprice = models.DecimalField(decimal_places=2, null=True, max_digits=19, db_column='nVendorSalePrice', blank=True)
    # nhotitem100_1 = models.CharField(max_length=1, db_column='nHotItem100_1', blank=True)
    # nhotitem20_1 = models.CharField(max_length=1, db_column='nHotItem20_1', blank=True)
    # nhotitem100_2 = models.CharField(max_length=1, db_column='nHotItem100_2', blank=True)
    # nhotitem20_2 = models.CharField(max_length=1, db_column='nHotItem20_2', blank=True)
    # nhotitem100_3 = models.CharField(max_length=1, db_column='nHotItem100_3', blank=True)
    # nhotitem20_3 = models.CharField(max_length=1, db_column='nHotItem20_3', blank=True)
    # nhotitem100_4 = models.CharField(max_length=1, db_column='nHotItem100_4', blank=True)
    # nhotitem20_4 = models.CharField(max_length=1, db_column='nHotItem20_4', blank=True)
    # nhotitem100_2m = models.CharField(max_length=1, db_column='nHotItem100_2M', blank=True)
    # nhotitem20_2m = models.CharField(max_length=1, db_column='nHotItem20_2M', blank=True)
    # nhotitem100_1sorting = models.IntegerField(null=True, db_column='nHotItem100_1Sorting', blank=True)
    # nhotitem20_1sorting = models.IntegerField(null=True, db_column='nHotItem20_1Sorting', blank=True)
    # nhotitem100_2sorting = models.IntegerField(null=True, db_column='nHotItem100_2Sorting', blank=True)
    # nhotitem20_2sorting = models.IntegerField(null=True, db_column='nHotItem20_2Sorting', blank=True)
    # nhotitem100_3sorting = models.IntegerField(null=True, db_column='nHotItem100_3Sorting', blank=True)
    # nhotitem20_3sorting = models.IntegerField(null=True, db_column='nHotItem20_3Sorting', blank=True)
    # nhotitem100_4sorting = models.IntegerField(null=True, db_column='nHotItem100_4Sorting', blank=True)
    # nhotitem20_4sorting = models.IntegerField(null=True, db_column='nHotItem20_4Sorting', blank=True)
    # nhotitem100_2msorting = models.IntegerField(null=True, db_column='nHotItem100_2MSorting', blank=True)
    # nhotitem20_2msorting = models.IntegerField(null=True, db_column='nHotItem20_2MSorting', blank=True)
    # pcolorid1 = models.CharField(max_length=2, db_column='PColorID1', blank=True)
    # pcolorid2 = models.CharField(max_length=2, db_column='PColorID2', blank=True)
    # pcolorid3 = models.CharField(max_length=2, db_column='PColorID3', blank=True)
    # pcolorid4 = models.CharField(max_length=2, db_column='PColorID4', blank=True)
    # pcolorid5 = models.CharField(max_length=2, db_column='PColorID5', blank=True)
    # pcolorid6 = models.CharField(max_length=2, db_column='PColorID6', blank=True)
    # pcolorid7 = models.CharField(max_length=2, db_column='PColorID7', blank=True)
    # pcolorid8 = models.CharField(max_length=2, db_column='PColorID8', blank=True)
    # pcolorid9 = models.CharField(max_length=2, db_column='PColorID9', blank=True)
    # pictures1temp = models.CharField(max_length=100, db_column='PictureS1Temp', blank=True)
    # pictures2temp = models.CharField(max_length=100, db_column='PictureS2Temp', blank=True)
    # pictures3temp = models.CharField(max_length=100, db_column='PictureS3Temp', blank=True)
    # pictures4temp = models.CharField(max_length=100, db_column='PictureS4Temp', blank=True)
    # pictures5temp = models.CharField(max_length=100, db_column='PictureS5Temp', blank=True)
    # pictures6temp = models.CharField(max_length=100, db_column='PictureS6Temp', blank=True)
    # pictures7temp = models.CharField(max_length=100, db_column='PictureS7Temp', blank=True)
    # pictures8temp = models.CharField(max_length=100, db_column='PictureS8Temp', blank=True)
    # pictures9temp = models.CharField(max_length=100, db_column='PictureS9Temp', blank=True)
    # picturer1temp = models.CharField(max_length=100, db_column='PictureR1Temp', blank=True)
    # picturer2temp = models.CharField(max_length=100, db_column='PictureR2Temp', blank=True)
    # picturer3temp = models.CharField(max_length=100, db_column='PictureR3Temp', blank=True)
    # picturer4temp = models.CharField(max_length=100, db_column='PictureR4Temp', blank=True)
    # picturer5temp = models.CharField(max_length=100, db_column='PictureR5Temp', blank=True)
    # picturer6temp = models.CharField(max_length=100, db_column='PictureR6Temp', blank=True)
    # picturer7temp = models.CharField(max_length=100, db_column='PictureR7Temp', blank=True)
    # picturer8temp = models.CharField(max_length=100, db_column='PictureR8Temp', blank=True)
    # picturer9temp = models.CharField(max_length=100, db_column='PictureR9Temp', blank=True)
    # picture1temp = models.CharField(max_length=100, db_column='Picture1Temp', blank=True)
    # picture2temp = models.CharField(max_length=100, db_column='Picture2Temp', blank=True)
    # picture3temp = models.CharField(max_length=100, db_column='Picture3Temp', blank=True)
    # picture4temp = models.CharField(max_length=100, db_column='Picture4Temp', blank=True)
    # picture5temp = models.CharField(max_length=100, db_column='Picture5Temp', blank=True)
    # picture6temp = models.CharField(max_length=100, db_column='Picture6Temp', blank=True)
    # picture7temp = models.CharField(max_length=100, db_column='Picture7Temp', blank=True)
    # picture8temp = models.CharField(max_length=100, db_column='Picture8Temp', blank=True)
    # picture9temp = models.CharField(max_length=100, db_column='Picture9Temp', blank=True)
    # nmatched = models.CharField(max_length=1, db_column='nMatched', blank=True)
    # nupdate = models.CharField(max_length=1, db_column='nUpdate', blank=True)
    # nvendorbestseller = models.CharField(max_length=1, db_column='nVendorBestSeller', blank=True)
    # nvendorbestsellermanual = models.CharField(max_length=1, db_column='nVendorBestSellerManual', blank=True)
    # nabschoice = models.CharField(max_length=1, db_column='nABSChoice', blank=True)
    # nadd = models.CharField(max_length=1, db_column='nAdd', blank=True)
    # nselfadd = models.CharField(max_length=1, db_column='nSelfAdd', blank=True)
    # tbstyleno_category_master_id = models.BigIntegerField(null=True, db_column='TBStyleNo_Category_Master_ID', blank=True)
    # tbstyleno_category_sub_id = models.BigIntegerField(null=True, db_column='TBStyleNo_Category_Sub_ID', blank=True)
    # tbstyleno_patterndetail_id = models.CharField(max_length=140, db_column='TBStyleNo_PatternDetail_ID', blank=True)
    # tbstyleno_department_id = models.IntegerField(null=True, db_column='TBStyleNo_Department_ID', blank=True)
    # nsortingno = models.IntegerField(null=True, db_column='nSortingNO', blank=True)
    # ongroupby_active = models.CharField(max_length=1, db_column='onGroupBy_Active', blank=True)
    # ongroupby_maxpack = models.IntegerField(null=True, db_column='onGroupBy_MaxPack', blank=True)
    # ongroupby_choosepackqty = models.IntegerField(null=True, db_column='onGroupBy_ChoosePackQTY', blank=True)
    # oniscustomer = models.CharField(max_length=1, db_column='OnisCustomer', blank=True)
    # picturez1temp = models.CharField(max_length=100, db_column='PictureZ1Temp', blank=True)
    # picturez2temp = models.CharField(max_length=100, db_column='PictureZ2Temp', blank=True)
    # picturez3temp = models.CharField(max_length=100, db_column='PictureZ3Temp', blank=True)
    # picturez4temp = models.CharField(max_length=100, db_column='PictureZ4Temp', blank=True)
    # picturez5temp = models.CharField(max_length=100, db_column='PictureZ5Temp', blank=True)
    # picturez6temp = models.CharField(max_length=100, db_column='PictureZ6Temp', blank=True)
    # picturez7temp = models.CharField(max_length=100, db_column='PictureZ7Temp', blank=True)
    # picturez8temp = models.CharField(max_length=100, db_column='PictureZ8Temp', blank=True)
    # picturez9temp = models.CharField(max_length=100, db_column='PictureZ9Temp', blank=True)
    # picturefulllocation = models.CharField(max_length=1000, db_column='PictureFullLocation', blank=True)
    # picturev1temp = models.CharField(max_length=100, db_column='PictureV1Temp', blank=True)
    # picturev2temp = models.CharField(max_length=100, db_column='PictureV2Temp', blank=True)
    # picturev3temp = models.CharField(max_length=100, db_column='PictureV3Temp', blank=True)
    # picturev4temp = models.CharField(max_length=100, db_column='PictureV4Temp', blank=True)
    # picturev5temp = models.CharField(max_length=100, db_column='PictureV5Temp', blank=True)
    # picturev6temp = models.CharField(max_length=100, db_column='PictureV6Temp', blank=True)
    # picturev7temp = models.CharField(max_length=100, db_column='PictureV7Temp', blank=True)
    # picturev8temp = models.CharField(max_length=100, db_column='PictureV8Temp', blank=True)
    # picturev9temp = models.CharField(max_length=100, db_column='PictureV9Temp', blank=True)
    # pictureelocation = models.CharField(max_length=200, db_column='PictureELocation', blank=True)
    # picturellocation = models.CharField(max_length=200, db_column='PictureLLocation', blank=True)
    # picturevlocation = models.CharField(max_length=200, db_column='PictureVLocation', blank=True)
    # picturezlocation = models.CharField(max_length=200, db_column='PictureZLocation', blank=True)
    # picturetestr1 = models.CharField(max_length=100, db_column='PictureTestR1', blank=True)
    # groupbuyseries = models.CharField(max_length=1, db_column='GroupBuySeries', blank=True)
    # tbgroupbuystyleno_id = models.BigIntegerField(null=True, db_column='TBGroupBuyStyleNo_ID', blank=True)
    # groupno_id = models.CharField(max_length=50, db_column='GroupNO_ID', blank=True)
    # nstylenameupdated = models.CharField(max_length=1, db_column='nStyleNameUpdated', blank=True)
    # searchfield = models.TextField(db_column='SearchField', blank=True)
    # pageidx = models.BigIntegerField(null=True, db_column='PageIDX', blank=True)

    @property
    def is_active(self):
        return True if self._is_active == 'Y' else False

    @is_active.setter
    def is_active(self, value):
        self._is_active = 'Y' if value else 'N'

    @property
    def is_preorder(self):
        return True if self._is_preorder == 'Y' else False

    @is_preorder.setter
    def is_preorder(self, value):
        self._is_preorder = 'Y' if value else 'N'

    @property
    def is_restock(self):
        return True if self._is_restock == 'Y' else False

    @is_restock.setter
    def is_restock(self, value):
        self._is_restock = 'Y' if value else 'N'

    @property
    def is_sale(self):
        return True if self._is_sale == 'Y' else False

    @is_sale.setter
    def is_sale(self, value):
        self._is_sale = 'Y' if value else 'N'

    @property
    def pictures(self):
        _length = range(1, 10)
        return dict(
            tiny=[
                getattr(self, "pictures%s" % i) for i in _length
                if getattr(self, "picture%s" % i)
            ],
            medium=[
                getattr(self, "picture%s" % i) for i in _length
                if getattr(self, "picture%s" % i)
            ],
            large=[
                getattr(self, "picturez%s" % i) for i in _length
                if getattr(self, "picture%s" % i)
            ],
        )

    @pictures.setter
    def pictures(self, values):
        _length = range(1, 10)
        _scaffold = dict(large="picturez", medium="picture", tiny="pictures")
        if not type(dict()) is type(values) or not any(
                map(lambda l: l in list(_scaffold.keys()), list(
                    values.keys()))):
            # raise ValueError('not acceptable pictures')
            raise ValueError(list(_scaffold.keys()), list(values.keys()))
        for k, v in values.items():
            if len(v) > 9:
                raise ValueError('max picture set is %s' % (_length, ))
            for p in _length:
                try:
                    setattr(self, _scaffold.get(k) + str(p), v[p - 1])
                except IndexError:
                    setattr(self, _scaffold.get(k) + str(p), None)

    @property
    def is_hidden(self):
        return True if self._is_hidden == 'Y' else False

    @is_hidden.setter
    def is_hidden(self, value):
        self._is_hidden = 'Y' if value else 'N'

    def delete(self, *args, **kwargs):
        raise PreventDeleteException('cannot delete product')

    def save(self, *args, **kwargs):
        if not self.id:
            _new_id = int(self.__class__.objects.last().id) + 1
            self.id = '%08d' % _new_id
            self.grouped_item_code = "G%s" % _new_id
        super(AbstractProductModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True
        ordering = ['id']
        db_table = 'TBStyleNo'


class ProductModel(AbstractProductModel):
    brand = models.ForeignKey('meta_db.BrandModel',
                              db_column='TBVendor_ID',
                              on_delete=models.DO_NOTHING)
    brand_category = models.ForeignKey('meta_db.BrandCategoryModel',
                                       db_column='TBVendorOwnCategory_ID',
                                       on_delete=models.DO_NOTHING,
                                       help_text='brand own categories')
    os_category_master = models.ForeignKey(
        'meta_db.StyleCategoryMasterModel',
        db_column='TBStyleNo_OS_Category_Master_ID',
        on_delete=models.DO_NOTHING)
    os_category_sub = models.ForeignKey(
        'meta_db.StyleCategorySubModel',
        db_column='TBStyleNo_OS_Category_Sub_ID',
        on_delete=models.DO_NOTHING)
    os_collection = models.ForeignKey('StyleCollectionModel',
                                      db_column='TBStyleNo_OS_Collection_ID',
                                      on_delete=models.DO_NOTHING,
                                      help_text='os style collection id')
    size_chart = models.ForeignKey('SizeChartLabelModel',
                                   db_column='TBSizeChart_ID',
                                   on_delete=models.DO_NOTHING)
    pack = models.ForeignKey('SizeChartQuantityModel',
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
            item__brand=self.brand)

    @property
    def is_shoes(self):
        return True if self.os_category_master_id == 15 and SelectedShoeSizeChartModel.objects.filter(
            item_id=self.id).exists() else False

    class Meta(AbstractProductModel.Meta):
        managed = False


##########
# COLORS #
##########
class AbstractColorModelManager(models.Manager):
    def all_active(self, **kwargs):
        return super(AbstractColorModelManager,
                     self).get_queryset().filter(is_active=True, **kwargs)


class AbstractColorModel(models.Model):
    id = models.CharField(max_length=10,
                          db_column='TBColor_ID',
                          primary_key=True)
    name = models.CharField(max_length=30, db_column='cColorName')
    description = models.CharField(max_length=50,
                                   db_column='cColorDescription',
                                   blank=True)
    is_active = models.BooleanField(db_column='cActive',
                                    default=True,
                                    help_text='T/F')
    _is_added = models.CharField(max_length=1,
                                 db_column='cAdd',
                                 default='Y',
                                 help_text='for ARA Y/N')
    _is_deleted = models.CharField(max_length=1,
                                   db_column='cDelete',
                                   default='N',
                                   help_text='for ARA Y/N')
    objects = AbstractColorModelManager()

    @property
    def is_added(self):
        return True if self._is_added == 'Y' else False

    @is_added.setter
    def is_added(self, value):
        self._is_added = 'Y' if value else 'N'

    @property
    def is_deleted(self):
        return True if self._is_deleted == 'Y' else False

    @is_deleted.setter
    def is_deleted(self, value):
        self._is_deleted = 'Y' if value else 'N'

    def delete(self, *args, **kwargs):
        """
        CURRENTLY, ACTUALLY DELETE COLOR
        SHOULD CHANGE LOGIC
        """
        self.is_active = False
        self.is_deleted = True
        super(AbstractColorModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True
        db_table = 'TBColor'


class ColorModel(AbstractColorModel):
    brand = models.ForeignKey('meta_db.BrandModel',
                              db_column='TBVendor_ID',
                              on_delete=models.DO_NOTHING)

    def save(self, *args, **kwargs):
        """
        SHOULD REVISE ID GENERATOR AS AUTO INCREMENT
        """
        if not self.pk:
            _id = 100
            _pre = ColorModel.objects.filter(brand=self.brand)
            if _pre.count() > 0:
                _id = int(_pre.last().id.split('_')[-1]) + 1
            self.id = "%s_%04d" % (self.brand.id, _id)
        super(ColorModel, self).save(*args, **kwargs)

    class Meta(AbstractColorModel.Meta):
        managed = False


class AbstractColorSelectedModelManager(models.Manager):
    def all_active(self, **kwargs):
        return super(AbstractColorSelectedModelManager,
                     self).get_queryset().filter(_is_active='Y', **kwargs)


class AbstractColorSelectedModel(models.Model):
    id = models.AutoField(db_column='TBColorSelect_ID', primary_key=True)
    _is_active = models.CharField(max_length=1,
                                  db_column='Active',
                                  default='Y',
                                  help_text='active Y/N')
    updated_date = models.DateTimeField(db_column='nUpdatedDate',
                                        auto_now=True)
    image_link = models.CharField(max_length=50,
                                  db_column='ImageLink',
                                  blank=True)
    objects = AbstractColorSelectedModelManager()
    # is_add = models.CharField(max_length=1, db_column='nAdd', blank=True, help_text='for ARA Y/N')
    # is_update = models.CharField(max_length=1, db_column='nUpdate', blank=True, help_text='for ARA Y/N')
    # is_delete = models.CharField(max_length=1, db_column='nDelete', blank=True, help_text='for ARA Y/N')
    # transferred_to_brand = models.CharField(max_length=1, db_column='nTransferedToVendor', blank=True)

    @property
    def is_active(self):
        return True if self._is_active == 'Y' else False

    @is_active.setter
    def is_active(self, value):
        self._is_active = 'Y' if value else 'N'

    class Meta:
        abstract = True
        db_table = 'TBColorSelect'


class ColorSelectedModel(AbstractColorSelectedModel):
    item = models.ForeignKey(
        'meta_db.ProductModel',
        db_column='TBItem_ID',
        related_name='only_colors',
        on_delete=models.DO_NOTHING,
        help_text=
        'colors only belong to an item. Excluding set bundle or set docking ')
    color = models.ForeignKey('ColorModel',
                              db_column='TBColor_ID',
                              on_delete=models.DO_NOTHING)

    class Meta(AbstractColorSelectedModel.Meta):
        managed = False
