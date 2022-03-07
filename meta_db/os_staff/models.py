from django.db import models


class OSStaffModel(models.Model):
    """
    OS Admin USER MODEL
    """
    id = models.AutoField(db_column='AdminIndex', primary_key=True)
    first_name = models.CharField(max_length=50, db_column='FirstName')
    last_name = models.CharField(max_length=50, db_column='LastName')
    email = models.CharField(max_length=100, db_column='Email')
    image = models.CharField(max_length=150,
                             db_column='Image',
                             blank=True,
                             null=True)
    phone_number = models.CharField(max_length=30,
                                    db_column='PhoneNumber',
                                    blank=True,
                                    null=True)

    def save(self, *args, **kwargs):
        return

    def delete(self, *args, **kwargs):
        return

    class Meta:
        managed = False
        db_table = 'WebsiteAdministrators'
