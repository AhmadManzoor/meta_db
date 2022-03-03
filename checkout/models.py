from __future__ import unicode_literals

import uuid
from django.db import models
from meta_db.exceptions import PreventSaveException, PreventDeleteException

class AbstractCheckoutStepTraceModel(models.Model):
    """
    READ AND INSERT ONLY
    DO NOT MODIFY OR DELETE
    """
    id = models.TextField(db_column='TBCheckoutHistory_ID', primary_key=True, help_text='uuid', unique=True)
    customer_id = models.CharField(db_column='TBCustomer_ID', max_length=8)
    step = models.IntegerField(db_column='Step')
    marked_date = models.DateTimeField(db_column='InputDate', auto_now_add=True)
    cart_amount = models.DecimalField(db_column='CartAMT', max_digits=19, decimal_places=4, default=0.00)

    # onvendorid = models.CharField(db_column='onVendorID', max_length=3, blank=True, null=True)
    # tadd = models.CharField(db_column='TAdd', max_length=1, blank=True, null=True, help_text='mark for ARA')

    def save(self, *args, **kwargs):
        if not self.pk:
            self.id = str(uuid.uuid1()).upper()
            super(AbstractCheckoutStepTraceModel, self).save(*args, **kwargs)
        else:
            raise PreventSaveException('cannot update checkout step')

    def delete(self, using=None, keep_parents=False):
        raise PreventDeleteException('cannot delete checkout step')

    class Meta:
        abstract = True
        ordering = ['marked_date', '-step']
        db_table = 'TBCheckoutHistory'


class CheckoutStepTraceModel(AbstractCheckoutStepTraceModel):
    class Meta(AbstractCheckoutStepTraceModel.Meta):
        managed = False
