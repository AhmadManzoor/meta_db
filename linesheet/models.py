import uuid
from django.db import models


class AbstractVendorLinesheetSendModel(models.Model):
    id = models.CharField(max_length=40, primary_key=True)
    brand_id = models.CharField(max_length=3, db_column='vendor_id')
    linesheet_name = models.CharField(max_length=128, db_column='linesheet_name')
    display_options = models.CharField(max_length=20, db_column='display_options')

    def save(self, *args, **kwargs):
        if not self.pk:
            while True:
                _id = uuid.uuid1().hex
                try:
                    VendorLinesheetSendModel.objects.get(pk=_id)
                except VendorLinesheetSendModel.DoesNotExist:
                    self.id = _id
                    break
        super(AbstractVendorLinesheetSendModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True
        db_table = 'TBVendorLinesheetSend'


class VendorLinesheetSendModel(AbstractVendorLinesheetSendModel):
    class Meta(AbstractVendorLinesheetSendModel.Meta):
        managed = False


class AbstractVendorLinesheetScheduledModel(models.Model):
    # Choices
    RECIPIENT_TYPE_CHOICES = (
        ('G', 'Group'),
        ('I', 'Individual'),
    )
    STATUS_CHOICES = (
        ('S', 'Scheduled'),
        ('P', 'Paused'),
        ('F', 'Finished'),
        ('D', 'Deleted'),
    )
    # Fields
    id = models.CharField(max_length=40, primary_key=True)
    email_title = models.CharField(max_length=128, db_column='email_title', blank=True)
    message = models.CharField(max_length=128, db_column='message',
                               blank=True)
    schedule_date = models.DateTimeField(db_column='schedule_date', blank=True)
    recipient_type = models.CharField(max_length=1, db_column='recipient_type',
                                      default='G', choices=RECIPIENT_TYPE_CHOICES)
    sent_count = models.IntegerField(db_column='sent_count', default=0)
    sent_date = models.DateTimeField(db_column='sent_date', blank=True)
    status = models.CharField(max_length=1, db_column='status', default='P',
                              choices=STATUS_CHOICES)
    created = models.DateTimeField(db_column='created', auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            while True:
                _id = uuid.uuid1().hex
                try:
                    VendorLinesheetScheduledModel.objects.get(pk=_id)
                except VendorLinesheetScheduledModel.DoesNotExist:
                    self.id = _id
                    break
        super(AbstractVendorLinesheetScheduledModel, self).save(*args, **kwargs)

    @property
    def is_scheduled(self):
        return True if self.status == 'S' else False

    @is_scheduled.setter
    def is_scheduled(self, value):
        if type(value) == bool and value:
            self.status = 'S'

    @property
    def is_paused(self):
        return True if self.status == 'P' else False

    @is_paused.setter
    def is_paused(self, value):
        if type(value) == bool and value:
            self.status = 'P'

    @property
    def is_sent(self):
        return True if self.status == 'F' else False

    @is_sent.setter
    def is_sent(self, value):
        if type(value) == bool and value:
            self.status = 'F'

    @property
    def is_deleted(self):
        return True if self.status == 'D' else False

    @is_deleted.setter
    def is_deleted(self, value):
        if type(value) == bool and value:
            self.status = 'D'

    @property
    def sent_to(self):
        contactgroup_list = VendorContactGroupModel.objects.filter(by_contactgroup__linesheetscheduled=self.id)
        sent_to_list = []
        for contactgroup in contactgroup_list:
            if contactgroup.name != "":
                sent_to_list.append(contactgroup.name)
            else:
                contacts = contactgroup.by_groups.all()
                for contact in contacts:
                    sent_to_list.append(contact.contactemail.email)
        return sent_to_list

    @property
    def sent_to_list(self):
        contactgroup_list = VendorContactGroupModel.objects.filter(
            by_contactgroup__linesheetscheduled=self.id)
        sent_to_list = []
        for contactgroup in contactgroup_list:
            if contactgroup.name != "":
                sent_to_list.append(contactgroup.id)
            else:
                contacts = contactgroup.by_groups.all()
                for contact in contacts:
                    sent_to_list.append(contact.contactemail.email)

        sent_to_list_str = ','.join([str(x) for x in sent_to_list])
        return sent_to_list_str

    class Meta:
        abstract = True
        ordering = ['-schedule_date']
        db_table = 'TBVendorLinesheetScheduled'


class VendorLinesheetScheduledModel(AbstractVendorLinesheetScheduledModel):
    linesheetsend = models.ForeignKey('VendorLinesheetSendModel', db_column='linesheetsend_id', related_name='by_linesheetsend', on_delete=models.DO_NOTHING)

    class Meta(AbstractVendorLinesheetScheduledModel.Meta):
        managed = False


class AbstractVendorLinesheetItemScheduledModel(models.Model):
    id = models.CharField(max_length=40, primary_key=True)
    selected_pictures = models.CharField(max_length=300, db_column='selected_pictures', null=True, blank=True)
    created = models.DateTimeField(db_column='created', auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            while True:
                _id = uuid.uuid1().hex
                try:
                    VendorLinesheetItemScheduledModel.objects.get(pk=_id)
                except VendorLinesheetItemScheduledModel.DoesNotExist:
                    self.id = _id
                    break
        super(AbstractVendorLinesheetItemScheduledModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True
        ordering = ['-created']
        db_table = 'TBVendorLinesheetItemScheduled'


class VendorLinesheetItemScheduledModel(AbstractVendorLinesheetItemScheduledModel):
    linesheetsend = models.ForeignKey('VendorLinesheetSendModel', db_column='linesheetsend_id', related_name='by_linesheetitem', on_delete=models.DO_NOTHING)
    item = models.ForeignKey('meta_db.ProductModel', db_column='item_id', on_delete=models.DO_NOTHING)

    class Meta(AbstractVendorLinesheetItemScheduledModel.Meta):
        managed = False


class AbstractVendorLinesheetContactGroupModel(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    is_sent = models.CharField(max_length=1, db_column='is_sent', default='N')
    created = models.DateTimeField(db_column='created', auto_now_add=True)

    class Meta:
        abstract = True
        db_table = 'TBVendorLinesheetContactGroup'


class VendorLinesheetContactGroupModel(AbstractVendorLinesheetContactGroupModel):
    linesheetscheduled = models.ForeignKey('VendorLinesheetScheduledModel', db_column='linesheetscheduled_id', related_name='by_linesheetscheduled', on_delete=models.DO_NOTHING)
    contactgroup = models.ForeignKey('VendorContactGroupModel', db_column='contactgroup_id', related_name='by_contactgroup', on_delete=models.DO_NOTHING)

    class Meta(AbstractVendorLinesheetContactGroupModel.Meta):
        managed = False


class AbstractVendorContactGroupModel(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    brand_id = models.CharField(max_length=3, db_column='vendor_id')
    name = models.CharField(max_length=50, db_column='name')
    created = models.DateTimeField(db_column='created', auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ['-created']
        db_table = 'TBVendorContactGroup'


class VendorContactGroupModel(AbstractVendorContactGroupModel):
    class Meta(AbstractVendorContactGroupModel.Meta):
        managed = False


class AbstractVendorContactModel(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    name = models.CharField(max_length=50, db_column='name')
    company = models.CharField(max_length=50, db_column='company')
    created = models.DateTimeField(db_column='created', auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ['-created']
        db_table = 'TBVendorContact'


class VendorContactModel(AbstractVendorContactModel):
    contactgroup = models.ForeignKey('VendorContactGroupModel', db_column='contactgroup_id', on_delete=models.CASCADE, related_name='by_groups')
    contactemail = models.ForeignKey('VendorContactEmailModel', db_column='contactemail_id', related_name='by_contacts', on_delete=models.DO_NOTHING)

    class Meta(AbstractVendorContactModel.Meta):
        managed = False


class AbstractVendorContactEmailModel(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    brand_id = models.CharField(max_length=3, db_column='vendor_id')
    email = models.CharField(max_length=100, db_column='email')
    verified = models.CharField(max_length=1, db_column='verified', default='P')
    subscribed = models.CharField(max_length=1, db_column='subscribed', default='Y')
    modified = models.DateTimeField(db_column='modified', auto_now=True)
    created = models.DateTimeField(db_column='created', auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ['-created']
        db_table = 'TBVendorContactEmail'


class VendorContactEmailModel(AbstractVendorContactEmailModel):
    class Meta(AbstractVendorContactEmailModel.Meta):
        managed = False


class AbstractVendorLinesheetSentLogModel(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    email = models.CharField(max_length=100, db_column='email')
    created = models.DateTimeField(db_column='created', auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ['-created']
        db_table = 'TBVendorLinesheet_Sent_Log'


class VendorLinesheetSentLogModel(AbstractVendorLinesheetSentLogModel):
    linesheetscheduled = models.ForeignKey('VendorLinesheetScheduledModel', db_column='linesheetscheduled_id', on_delete=models.DO_NOTHING)
    class Meta(AbstractVendorLinesheetSentLogModel.Meta):
        managed = False


class AbstractVendorSchedulerModel(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    day = models.IntegerField(db_column='day')
    time = models.TimeField(db_column='time')
    _is_active = models.CharField(max_length=1, db_column='is_active',
                                  default='Y')
    created = models.DateTimeField(db_column='created', auto_now_add=True)

    @property
    def is_active(self):
        return True if self._is_active == 'Y' else False

    class Meta:
        abstract = True
        db_table = 'TBVendorScheduler'


class VendorSchedulerModel(AbstractVendorSchedulerModel):
    brand = models.ForeignKey('meta_db.BrandModel', db_column='vendor_id', on_delete=models.DO_NOTHING)

    class Meta(AbstractVendorSchedulerModel.Meta):
        managed = False


class AbstractVendorSchedulerTitleModel(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    email_title = models.CharField(max_length=100, db_column='email_title')
    _is_add_date = models.CharField(max_length=1, db_column='is_add_date',
                                    default='N')
    created = models.DateTimeField(db_column='created', auto_now_add=True)

    @property
    def is_add_date(self):
        return True if self._is_add_date == 'Y' else False

    class Meta:
        abstract = True
        ordering = ['created']
        db_table = 'TBVendorScheduler_title'


class VendorSchedulerTitleModel(AbstractVendorSchedulerTitleModel):
    scheduler = models.ForeignKey('VendorSchedulerModel', db_column='scheduler_id', on_delete=models.DO_NOTHING)
    class Meta(AbstractVendorSchedulerTitleModel.Meta):
        managed = False


class AbstractVendorSchedulerSentHistoryModel(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    email_title = models.CharField(max_length=110, db_column='email_title')
    item_id_list = models.CharField(max_length=512, db_column='item_id_list')
    sent_count = models.IntegerField(db_column='sent_count', default=0)
    sent_date = models.DateTimeField(db_column='sent_date', auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ['-sent_date']
        db_table = 'TBVendorScheduler_sent_history'


class VendorSchedulerSentHistoryModel(AbstractVendorSchedulerSentHistoryModel):
    scheduler = models.ForeignKey('VendorSchedulerModel', db_column='scheduler_id', on_delete=models.DO_NOTHING)

    class Meta(AbstractVendorSchedulerSentHistoryModel.Meta):
        managed = False