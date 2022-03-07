from __future__ import unicode_literals

from django.db import models
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from meta_db.exceptions import PreventDeleteException
from django.template.defaultfilters import slugify


#####################
# OS STYLE CATEGORY #
#####################
class AbstractGrandCategoryModel(models.Model):
    id = models.IntegerField(db_column='id',
                             primary_key=True,
                             help_text='ordering of grouped for showing')
    name = models.CharField(db_column='group_name',
                            max_length=50,
                            help_text='grouped for showing.')
    ordering = models.IntegerField(db_column='ordering')

    @property
    def slug_name(self):
        return slugify(self.name)

    class Meta:
        abstract = True
        ordering = ['ordering']
        db_table = 'vGrandCategory'


class GrandCategoryModel(AbstractGrandCategoryModel):
    class Meta(AbstractGrandCategoryModel.Meta):
        managed = False


class AbstractStyleCategoryMasterModelManager(models.Manager):
    def all_active(self, **kwargs):
        return super(AbstractStyleCategoryMasterModelManager,
                     self).get_queryset().filter(is_active=True, **kwargs)


class AbstractStyleCategoryMasterModel(models.Model):
    """
    OS Style Master Category
    DO NOT DELETE. JUST MAKE IT INACTIVE.
    """
    id = models.AutoField(db_column='TBStyleNo_OS_Category_Master_ID',
                          primary_key=True)
    name = models.CharField(db_column='CategoryMasterName', max_length=50)
    description = models.TextField(db_column='Description',
                                   blank=True,
                                   null=True)
    short_description = models.TextField(db_column='Description50',
                                         blank=True,
                                         null=True,
                                         help_text='short description')
    ordering = models.IntegerField(db_column='DisplayOrder', default=0)
    display_group = models.CharField(
        db_column='DisplayGroup',
        max_length=50,
        help_text='grouped for showing. matches with vGrandCategory group_name'
    )
    display_group_order = models.ForeignKey(
        GrandCategoryModel,
        db_column='DisplayGroupOrder',
        related_name='master_categories',
        help_text='ordering of grouped for showing',
        on_delete=models.DO_NOTHING
    )
    slug_name = models.CharField(db_column='url',
                                 max_length=50,
                                 unique=True,
                                 help_text='slug style name')
    seo_title = models.CharField(db_column='seo_title',
                                 max_length=500,
                                 blank=True,
                                 null=True)

    is_active = models.BooleanField(db_column='Active', default=True)
    objects = AbstractStyleCategoryMasterModelManager()

    def delete(self, *args, **kwargs):
        raise PreventDeleteException('cannot delete this model')

    class Meta:
        abstract = True
        ordering = ['ordering']
        unique_together = (('name', 'display_group_order'), )
        db_table = 'TBStyleNo_OS_Category_Master'


class StyleCategoryMasterModel(AbstractStyleCategoryMasterModel):
    class Meta(AbstractStyleCategoryMasterModel.Meta):
        managed = False


class AbstractStyleCategorySubModelManager(models.Manager):
    def all_active(self, **kwargs):
        return super(AbstractStyleCategorySubModelManager,
                     self).get_queryset().filter(is_active=True, **kwargs)


class AbstractStyleCategorySubModel(models.Model):
    """
    OS Style Sub Category
    DO NOT DELETE. JUST MAKE IT INACTIVE.
    """
    id = models.AutoField(db_column='TBStyleNo_OS_Category_Sub_ID',
                          primary_key=True)
    name = models.CharField(db_column='CategorySubName', max_length=50)
    slug_name = models.CharField(db_column='url',
                                 max_length=50,
                                 help_text='slug name')
    short_description = models.TextField(db_column='Description50',
                                         blank=True,
                                         null=True,
                                         help_text='short description')
    description = models.CharField(db_column='Description',
                                   max_length=500,
                                   blank=True,
                                   null=True)
    seo_title = models.CharField(db_column='seo_title',
                                 max_length=500,
                                 blank=True,
                                 null=True)

    is_active = models.BooleanField(db_column='Active', default=True)
    objects = AbstractStyleCategorySubModelManager()

    def save(self, *args, **kwargs):
        self.validate_unique()
        super(AbstractStyleCategorySubModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise PreventDeleteException('cannot delete sub categories')

    class Meta:
        abstract = True
        db_table = 'TBStyleNo_OS_Category_Sub'
        ordering = ['name']


class StyleCategorySubModel(AbstractStyleCategorySubModel):
    master_category = models.ForeignKey(
        'StyleCategoryMasterModel',
        db_column='TBStyleNo_OS_Category_Master_ID',
        related_name='sub_categories',
        blank=True,
        null=True,
        on_delete=models.DO_NOTHING)

    def validate_unique(self, exclude=None):
        if self.__class__.objects.filter(master_category=self.master_category,
                                         slug_name=self.slug_name).exists():
            raise ValidationError({
                NON_FIELD_ERRORS: [
                    'Sub category already exists.',
                ],
            })

    class Meta(AbstractStyleCategorySubModel.Meta):
        managed = False
