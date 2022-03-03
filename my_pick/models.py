from __future__ import unicode_literals

import uuid
from django.db import models


class AbstractMyPickGroupModel(models.Model):
    id = models.CharField(max_length=40, primary_key=True)
    name = models.CharField(max_length=50, db_column='name')

    def save(self, *args, **kwargs):
        """
        should use update_or_create
        """
        if not self.pk:
            safe_id = True
            while safe_id:
                _id = uuid.uuid1().hex
                try:
                    MyPickGroupModel.objects.get(pk=_id)
                except MyPickGroupModel.DoesNotExist:
                    self.id = _id
                    safe_id = False
        super(AbstractMyPickGroupModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True
        ordering = ['name']
        db_table = 'TBMyPickGroup'


class MyPickGroupModel(AbstractMyPickGroupModel):
    user = models.ForeignKey('meta_db.UserModel', db_column='user_id', to_field='customer_id',
                             related_name='my_pick_groups', on_delete=models.DO_NOTHING)

    class Meta(AbstractMyPickGroupModel.Meta):
        managed = False


class AbstractMyPickModel(models.Model):
    id = models.CharField(max_length=40, primary_key=True)
    note = models.CharField(max_length=255, db_column='note', null=True, blank=True)
    modified = models.DateTimeField(db_column='modified', auto_now=True)
    created = models.DateTimeField(db_column='created', auto_now_add=True)

    def save(self, *args, **kwargs):
        """
        should use update_or_create
        """
        if not self.pk:
            safe_id = True
            while safe_id:
                _id = uuid.uuid1().hex
                try:
                    MyPickModel.objects.get(pk=_id)
                except MyPickModel.DoesNotExist:
                    self.id = _id
                    safe_id = False
        super(AbstractMyPickModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True
        ordering = ['-modified']
        db_table = 'TBMyPick'


class MyPickModel(AbstractMyPickModel):
    user = models.ForeignKey('meta_db.UserModel', db_column='user_id', to_field='customer_id', related_name='my_picks', on_delete=models.DO_NOTHING)
    item = models.ForeignKey('meta_db.ProductModel', db_column='item_id', on_delete=models.DO_NOTHING)
    group = models.ForeignKey('MyPickGroupModel', db_column='group_id', on_delete=models.CASCADE, null=True,
                              related_name='by_groups')

    class Meta(AbstractMyPickModel.Meta):
        managed = False
