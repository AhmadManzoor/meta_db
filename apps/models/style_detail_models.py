from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS

from meta_db.models import AbstractProductModel
from meta_db.models import AbstractSelectedShoeSizeChartModel
from meta_db.models import ColorSelectedModel
from apps.models.brand import BrandModel

# TODO: move StyleModel to meta_db


class StyleModel(AbstractProductModel):
    brand = models.ForeignKey(BrandModel,
                              db_column='TBVendor_ID',
                              on_delete=models.DO_NOTHING)
    brand_category = models.ForeignKey('meta_db.BrandCategoryModel',
                                       db_column='TBVendorOwnCategory_ID',
                                       help_text='brand own categories',
                                       on_delete=models.DO_NOTHING)
    os_category_master = models.ForeignKey(
        'meta_db.StyleCategoryMasterModel',
        db_column='TBStyleNo_OS_Category_Master_ID',
        on_delete=models.DO_NOTHING)
    os_category_sub = models.ForeignKey(
        'meta_db.StyleCategorySubModel',
        db_column='TBStyleNo_OS_Category_Sub_ID',
        on_delete=models.DO_NOTHING)
    os_collection = models.ForeignKey('meta_db.StyleCollectionModel',
                                      db_column='TBStyleNo_OS_Collection_ID',
                                      help_text='os style collection id',
                                      on_delete=models.DO_NOTHING)
    size_chart = models.ForeignKey('meta_db.SizeChartLabelModel',
                                   db_column='TBSizeChart_ID',
                                   on_delete=models.DO_NOTHING)
    pack = models.ForeignKey('meta_db.SizeChartQuantityModel',
                             db_column='TBPackNo_ID',
                             on_delete=models.DO_NOTHING)
    made_in = models.CharField(db_column='made_in',
                               max_length=50,
                               blank=True,
                               null=True)

    @property
    def grouped_items(self):
        return StyleModel.objects.filter(
            grouped_item_code=self.grouped_item_code, brand=self.brand)

    @property
    def colors(self):
        """
        all related colors including set bundle - do not exclude duplicates
        """
        return ColorSelectedModel.objects.all_active().filter(
            item__grouped_item_code=self.grouped_item_code,
            item__brand=self.brand)

    @property
    def colors_distinct_simplest(self):
        """
        all related colors including set bundle - excluding duplicates
        """
        return ColorSelectedModel.objects.all_active().only(
            'item_id', 'color_id', 'image_link', 'color__name').filter(
                item__grouped_item_code=self.grouped_item_code,
                item__brand=self.brand,
                item___is_active='Y',
                item___is_prepare='N',
                image_link__isnull=False).distinct().order_by('color__name')

    @property
    def colors_distinct(self):
        """
        all related colors including set bundle - excluding duplicates (desktop version algorithm considering bundles)
        """
        _gs = StyleModel.objects.values('id').filter(
            grouped_item_code=self.grouped_item_code, brand=self.brand, _is_active='Y', _is_prepare='N')
        _tmp_color_set = set([i['id'] for i in _gs])

        _tmp_colors = ColorSelectedModel.objects.all_active().values(
            'item_id', 'color_id', 'color__name',
            'image_link').filter(item_id__in=_tmp_color_set)

        # remove duplicated colors and sort by color name
        _tmp_dict = dict()
        for c in _tmp_colors:
            if not c.get('color_id') in _tmp_dict:
                _tmp_dict.setdefault(c.get('color_id'), c)
            else:
                try:
                    if c.get('item_id') == self.id:
                        _tmp_dict[c.get('color_id')] = c
                    elif not _tmp_dict.get(c.get('color_id')).get(
                            'image_link') and c.get('image_link'):
                        _tmp_dict[c.get('color_id')] = c
                except KeyError:
                    pass

        _color_set = sorted(_tmp_dict.values(),
                            key=lambda k: k.get('color__name'))
        return _color_set

    def is_own_available_color(self):
        return ColorSelectedModel.objects.all_active().filter(
            item_id=self.id).all().exists()

    @property
    def is_shoes(self):
        return True if self.os_category_master_id == 15 and self.shoe_size.exists(
        ) else False

    @property
    def is_plus(self):
        return True if self.os_category_master_id == 9 else False

    @property
    def price(self):
        return self.os_price

    @property
    def sale_price(self):
        return self.os_sale_price

    @property
    def pictures(self):
        _length = range(1, 10)
        return dict(
            tiny=[
                '{}/{}'.format(settings.BASE_STYLE_IMAGE_URL,
                               getattr(self, "pictures%s" % i))
                for i in _length if getattr(self, "picture%s" % i)
            ],
            medium=[
                '{}/{}'.format(settings.BASE_STYLE_IMAGE_URL,
                               getattr(self, "picture%s" % i)) for i in _length
                if getattr(self, "picture%s" % i)
            ],
            large=[
                '{}/{}'.format(settings.BASE_STYLE_IMAGE_URL,
                               getattr(self, "picturez%s" % i))
                for i in _length if getattr(self, "picture%s" % i)
            ],
        )

    class Meta(AbstractProductModel.Meta):
        managed = False


class SelectedShoeSizeChartModel(AbstractSelectedShoeSizeChartModel):
    item = models.ForeignKey(StyleModel,
                             db_column='TBItem_ID',
                             related_name='shoe_size',
                             on_delete=models.DO_NOTHING)
    shoe_size = models.ForeignKey('meta_db.ShoeSizeChartModel',
                                  db_column='TBVendorShoeSize_ID',
                                  on_delete=models.DO_NOTHING)

    def validate_unique(self, *args, **kwargs):
        if self.__class__.objects.filter(item=self.item,
                                         shoe_size=self.shoe_size).exists():
            raise ValidationError({
                NON_FIELD_ERRORS: [
                    'Shoe size chart already exists.',
                ],
            })

    def save(self, *args, **kwargs):
        self.validate_unique()
        super(AbstractSelectedShoeSizeChartModel, self).save(*args, **kwargs)

    class Meta(AbstractSelectedShoeSizeChartModel.Meta):
        managed = False


class StyleViewHistoryModel(models.Model):
    """
    To Record Item View History
    """
    id = models.AutoField(db_column='TBViewedHistory_ID', primary_key=True)
    item_id = models.CharField(max_length=8, db_column='TBItem_ID')
    customer_id = models.CharField(max_length=8, db_column='TBCustomer_ID')
    url = models.TextField(db_column='MenuURL')
    created_date = models.DateTimeField(db_column='nDate', auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'TBViewedHistory'
