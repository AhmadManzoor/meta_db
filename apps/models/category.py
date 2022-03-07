from django.db import models
from slugify import slugify

from meta_db.models import (
    GrandCategoryModel as GrandCategoryBaseModel,
    AbstractStyleCategoryMasterModel,
    AbstractStyleCategorySubModel,
    BrandCategoryModel as BrandCategoryBaseModel,
)


class GrandCategoryModel(GrandCategoryBaseModel):
    class Meta:
        proxy = True


class StyleCategoryMasterModel(AbstractStyleCategoryMasterModel):
    grand_category = models.ForeignKey(GrandCategoryModel,
                                       db_column='DisplayGroupOrder',
                                       related_name='master_categories',
                                       on_delete=models.DO_NOTHING)

    class Meta(AbstractStyleCategoryMasterModel.Meta):
        managed = False


class StyleCategorySubModel(AbstractStyleCategorySubModel):
    master_category = models.ForeignKey(
        'StyleCategoryMasterModel',
        db_column='TBStyleNo_OS_Category_Master_ID',
        related_name='sub_categories',
        blank=True,
        null=True,
        on_delete=models.DO_NOTHING
    )

    class Meta(AbstractStyleCategorySubModel.Meta):
        managed = False


class BrandCategoryModel(BrandCategoryBaseModel):
    def slug_name(self):
        return slugify(self.name)

    class Meta:
        proxy = True
