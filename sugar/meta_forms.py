from django import forms


class MetaForm(forms.Form):
    pass

    def __init__(self, *args, **kwargs):
        # TODO: python2.x compatibility
        super().__init__(*args, **kwargs)
        # custom required message
        # self.fields['name'].error_messages = {'required': 'custom required message'}

        for field in self.fields.values():
            field.error_messages = {'required': '{fieldname} is required'.format(
                fieldname=field.label)}


class UserDataMetaForm(MetaForm):
    pass

    def __init__(self, *args, **kwargs):
        # TODO: python2.x compatibility
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.error_messages = {'required': '{fieldname} is required'.format(
                fieldname=field.label)}
