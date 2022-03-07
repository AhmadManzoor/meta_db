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
