from django.db import models


class BrandListModel(models.Model):
    total_performance = models.IntegerField(db_column='total_performance')
    average_total_score = models.FloatField(db_column='avg_total_score')
    count_review = models.IntegerField(db_column='count_review')
    vendor_name_starts_with = models.CharField(db_column='vendor_name_starts_with', max_length=1)

    id = models.CharField(max_length=3, db_column='TBVendor_ID', primary_key=True)
    name = models.CharField(max_length=50, db_column='VDName', help_text='brand name')

    brand_image = models.CharField(max_length=255, db_column='Brand_Rep_Image')
    web_name = models.CharField(max_length=50, db_column='VDWebName')
    active_date = models.DateTimeField(db_column='VDActiveDate')

    def save(self, *args, **kwargs):
        return

    def delete(self, *args, **kwargs):
        return

    class Meta:
        managed = False
        db_table = 'vw_BrandList'


class BrandListSegmentModel(models.Model):
    id = models.AutoField(primary_key=True)
    brand = models.ForeignKey(BrandListModel,
                              db_column='TBVendor_ID',
                              related_name='brand_list_segments',
                              on_delete=models.DO_NOTHING)
    category_name = models.CharField(db_column='category_name', max_length=50)
    product_count = models.IntegerField(db_column='product_count')

    def save(self, *args, **kwargs):
        return

    def delete(self, *args, **kwargs):
        return

    class Meta:
        managed = False
        db_table = 'TBVendor_Category'
        unique_together = ('brand', 'category_name')


class PopularBrandListModel(models.Model):
    id = models.OneToOneField(BrandListModel,
                              db_column='TBVendor_ID',
                              primary_key=True,
                              related_name='popular_brand_list',
                              on_delete=models.DO_NOTHING)
    name = models.CharField(db_column='VDName', max_length=50)
    category = models.CharField(db_column='VDCategory', max_length=50)
    point = models.IntegerField(db_column='total_performance')

    def save(self, *args, **kwargs):
        return

    def delete(self, *args, **kwargs):
        return

    class Meta:
        managed = False
        db_table = 'vOSBrandPopularity'
