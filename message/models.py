import uuid
from django.db import models


class AbstractMessageTopicModel(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    name = models.CharField(max_length=30, db_column='name')
    is_active = models.BooleanField(db_column='is_active', default=True)

    class Meta:
        abstract = True
        db_table = 'TBMessageTopic'

class MessageTopicModel(AbstractMessageTopicModel):
    class Meta(AbstractMessageTopicModel.Meta):
        managed = False


class AbstractMessageThreadModel(models.Model):
    id = models.CharField(db_column='id', primary_key=True, max_length=40)
    title = models.CharField(max_length=50, db_column='title')
    reference_number = models.CharField(max_length=20, db_column='reference_num')
    is_active = models.BooleanField(db_column='is_active', default=True)  # TODO: help_text for this field
    created = models.DateTimeField(db_column='created', auto_now_add=True)
    status = models.CharField(max_length=1, db_column='os_status', default='O', help_text='flags for os staff')

    @property
    def message_count(self):
        return MessageModel.objects.filter(messagethread=self, is_active=True).count()

    class Meta:
        abstract = True
        ordering = ['-created']
        db_table = 'TBMessageThread'


class MessageThreadModel(AbstractMessageThreadModel):
    brand = models.ForeignKey('meta_db.BrandModel', db_column='vendor_id', on_delete=models.DO_NOTHING)
    customer = models.ForeignKey('meta_db.UserModel', db_column='customer_id', to_field='customer_id', related_name='message_threads', on_delete=models.DO_NOTHING)
    topic_type = models.ForeignKey(MessageTopicModel, db_column='reference_type', on_delete=models.DO_NOTHING)

    def save(self, *args, **kwargs):
        """
        should use update_or_create
        """
        if not self.pk:
            while True:
                _id = uuid.uuid1().hex
                try:
                    MessageThreadModel.objects.get(pk=_id)
                except MessageThreadModel.DoesNotExist:
                    self.id = _id
                    break
        super(MessageThreadModel, self).save(*args, **kwargs)

    class Meta(AbstractMessageThreadModel.Meta):
        managed = False


class AbstractMessageModel(models.Model):
    id = models.CharField(db_column='id', primary_key=True, max_length=40)
    body = models.CharField(max_length=2000, db_column='body', blank=True, null=True)
    is_brand_sent = models.BooleanField(db_column='is_vendor_sent', default=False, help_text='')  # TODO: check purpose
    is_read = models.BooleanField(db_column='is_read', default=False)
    notification_status = models.BooleanField(db_column='is_noti_status', default=False)
    created = models.DateTimeField(db_column='created', auto_now_add=True)
    image_url = models.CharField(max_length=100, db_column='image_link', blank=True, null=True)
    sender_id = models.CharField(max_length=50, db_column='sender_id', blank=True, null=True, help_text='brand or os staff id')
    sender_name = models.CharField(max_length=50, db_column='sender_name', blank=True, null=True, help_text='brand or os staff name')

    class Meta:
        abstract = True
        ordering = ['-created']
        db_table = 'TBMessage'


class MessageModel(AbstractMessageModel):
    thread = models.ForeignKey('meta_db.MessageThreadModel', db_column='messagethread_id', related_name='messages', on_delete=models.DO_NOTHING)

    def save(self, *args, **kwargs):
        """
        should use update_or_create
        """
        if not self.pk:
            while True:
                _id = uuid.uuid1().hex
                try:
                    MessageModel.objects.get(pk=_id)
                except MessageModel.DoesNotExist:
                    self.id = _id
                    break
        super(MessageModel, self).save(*args, **kwargs)

    class Meta(AbstractMessageModel.Meta):
        managed = False
