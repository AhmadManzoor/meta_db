from django.db import models
from meta_db.models import AbstractBrandModel


class BrandModel(AbstractBrandModel):
    fulfillment = models.ForeignKey('meta_db.FulfillmentModel',
                                    db_column='ShippedFrom',
                                    to_field='fulfillment',
                                    blank=True,
                                    on_delete=models.DO_NOTHING)
    style_collection = models.ForeignKey(
        'meta_db.StyleCollectionModel',
        db_column='TBStyleNo_OS_Collection_ID',
        help_text='style collection for item but use brand as well',
        blank=True,
        null=True,
        on_delete=models.DO_NOTHING)
    site = models.CharField(db_column='Site', max_length=10, default='OS')

    def save(self, *args, **kwargs):
        if not self.pk:
            self.id = '%02d' % (
                int(BrandModel.objects.order_by('id').last().pk) + 1, )
        super(AbstractBrandModel, self).save(*args, **kwargs)

    class Meta(AbstractBrandModel.Meta):
        managed = False
        ordering = ['name']



class FavoriteBrandModel(models.Model):
    id = models.AutoField(db_column='TBMyFavoriteVendor_SQL_ID', primary_key=True)
    brand = models.ForeignKey(BrandModel,
                              db_column='TBVendor_ID',
                              related_name='favorite_brand',
                              on_delete=models.DO_NOTHING)
    customer_id = models.CharField(db_column='TBCustomer_ID', max_length=8)
    created_date = models.DateTimeField(db_column='InputDate', auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'TBMyFavoriteVendor'
        unique_together = ('brand', 'customer_id')


class BrandAverageOrderReviewModel(models.Model):
    vendor_id = models.OneToOneField(
        BrandModel,
        to_field='id',
        db_column='TBVendor_ID',
        related_name='brand_average_review',
        primary_key=True,
        on_delete=models.DO_NOTHING,
    )
    five_star_percentage = models.IntegerField(db_column='pct_5_stars')
    four_star_percentage = models.IntegerField(db_column='pct_4_stars')
    three_star_percentage = models.IntegerField(db_column='pct_3_stars')
    two_star_percentage = models.IntegerField(db_column='pct_2_stars')
    one_star_percentage = models.IntegerField(db_column='pct_1_stars')

    average_total_score = models.FloatField(db_column='avg_total_score')
    average_product_quality = models.FloatField(db_column='avg_product_quality')
    average_shipping_time = models.FloatField(db_column='avg_shipping_time')
    average_handling_shipping_fee = models.FloatField(db_column='avg_handling_shipping_fee')
    average_communication = models.FloatField(db_column='avg_communication')

    class Meta:
        managed = False
        db_table = 'vw_AvgOrderReview'
