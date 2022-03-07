from __future__ import unicode_literals

from django.db import models


class ProductInfoFabricModel(models.Model):
    id = models.AutoField(db_column='TBStyleNo_OS_Fabric_ID', primary_key=True)
    name = models.CharField(db_column='FabricName',
                            max_length=50,
                            blank=True,
                            null=True)
    description = models.CharField(db_column='Description',
                                   max_length=50,
                                   blank=True,
                                   null=True)
    is_active = models.NullBooleanField(db_column='Active')
    kind = models.CharField(db_column='FabricKind',
                            max_length=50,
                            blank=True,
                            null=True)

    class Meta:
        managed = False
        db_table = 'TBStyleNo_OS_Fabric'


class ProductInfoFabricSelectedModel(models.Model):
    id = models.AutoField(db_column='TBStyleNo_OS_FabricSelect_ID',
                          primary_key=True)
    item = models.ForeignKey('meta_db.ProductModel',
                             db_column='TBItem_ID',
                             max_length=8,
                             related_name='pi_fabric_item',
                             on_delete=models.DO_NOTHING)
    fabric = models.ForeignKey('meta_db.ProductInfoFabricModel',
                               db_column='TBStyleNo_OS_Fabric_ID',
                               related_name='pi_fabric',
                               on_delete=models.DO_NOTHING)
    percent = models.CharField(max_length=10,
                               db_column='FabricPercent',
                               blank=True,
                               null=True)
    nadd = models.CharField(db_column='nAdd',
                            max_length=1,
                            blank=True,
                            null=True)
    ndelete = models.CharField(db_column='nDelete',
                               max_length=1,
                               blank=True,
                               null=True)

    class Meta:
        managed = False
        db_table = 'TBStyleNo_OS_FabricSelect'
