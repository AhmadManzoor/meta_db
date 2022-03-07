from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from jsonfield import JSONField

from meta_db.style.style_list_models import StyleListModel
from meta_db.style.models import ProductModel


class TrendReportMasterModelManager(models.Manager):
    @property
    def os(self):
        return super().get_queryset().filter(site='OS')

    @property
    def cm(self):
        return super().get_queryset().filter(site='CM')

    def site(self, request):
        site_type = 'cm' if get_current_site(
            request).domain in settings.CM_SITES else 'os'
        return getattr(self, site_type)


class TrendReportMasterModel(models.Model):
    """
    READ ONLY MODEL
    """
    id = models.TextField(db_column='TBEventPageMaster_ID', primary_key=True)
    title = models.CharField(max_length=500, db_column='event_title')
    seo_path = models.CharField(unique=True,
                                max_length=50,
                                db_column='seopath')
    status = models.CharField(max_length=1, db_column='status')
    input_date = models.DateTimeField(db_column='input_date')
    published_date = models.DateTimeField(db_column='published_date')
    master_image = models.TextField(db_column='MasterImage',
                                    blank=True,
                                    null=True)
    sort = models.CharField(max_length=1,
                            blank=True,
                            null=True,
                            db_column='sort')
    list_image = models.TextField(blank=True, null=True, db_column='listimage')
    published = models.BooleanField()
    data = JSONField(db_column='data')
    site = models.CharField(max_length=10, db_column='site')
    objects = TrendReportMasterModelManager()

    @property
    def main_items(self):
        _main_items = self.data.get('main_items') if self.data.get(
            'main_items') else []

        return _main_items

    @property
    def published_month(self):
        return self.published_date

    def get_absolute_url(self):
        return '/events/%s/' % self.seo_path

    def save(self, *args, **kwargs):
        return

    def delete(self, *args, **kwargs):
        return

    class Meta:
        managed = False
        db_table = 'TBEventPageMaster'


class TrendReportSubModel(models.Model):
    """
    READ ONLY MODEL
    """
    id = models.TextField(db_column='TBEventPageSubmaster_ID',
                          primary_key=True)
    master = models.ForeignKey(TrendReportMasterModel,
                               db_column='TBEventPageMaster_ID',
                               related_name='sub_pages',
                               on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=500, db_column='eventsubtitle')
    order = models.CharField(max_length=5,
                             db_column='status',
                             help_text='ordering')
    input_date = models.DateTimeField(db_column='input_date')
    image = models.TextField(db_column='SubImage', blank=True, null=True)

    def save(self, *args, **kwargs):
        return

    def delete(self, *args, **kwargs):
        return

    class Meta:
        managed = False
        ordering = ['order']
        db_table = 'TBEventPageSubmaster'


class AbstractTrendReportItemModel(models.Model):
    """
    READ ONLY MODEL
    """
    id = models.TextField(db_column='TBEventItems_ID', primary_key=True)
    sub = models.ForeignKey(TrendReportSubModel,
                            db_column='TBEventPageSubmaster_ID',
                            related_name='items',
                            on_delete=models.DO_NOTHING)
    nick_name = models.CharField(db_column='Nickname', max_length=50)
    order = models.CharField(max_length=5,
                             db_column='status',
                             help_text='ordering')
    input_date = models.DateTimeField(db_column='input_date')

    def save(self, *args, **kwargs):
        return

    def delete(self, *args, **kwargs):
        return

    class Meta:
        abstract = True
        ordering = ['order', '-input_date']
        db_table = 'TBEventItems'


class TrendReportItemModel(AbstractTrendReportItemModel):
    """
    Model for Mobile
    """
    sub = models.ForeignKey(TrendReportSubModel,
                            db_column='TBEventPageSubmaster_ID',
                            related_name='items',
                            on_delete=models.DO_NOTHING)
    style = models.ForeignKey(StyleListModel,
                              db_column='TBItem_ID',
                              on_delete=models.DO_NOTHING)

    class Meta(AbstractTrendReportItemModel.Meta):
        managed = False


class TrendReportItemModelDesktop(AbstractTrendReportItemModel):
    """
    Model for Desktop
    """
    sub = models.ForeignKey(TrendReportSubModel,
                            db_column='TBEventPageSubmaster_ID',
                            related_name='items_d',
                            on_delete=models.DO_NOTHING)
    os_style = models.ForeignKey(ProductModel,
                                 db_column='TBItem_ID',
                                 on_delete=models.DO_NOTHING)

    class Meta(AbstractTrendReportItemModel.Meta):
        managed = False
