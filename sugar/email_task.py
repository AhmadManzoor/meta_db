import simplejson as json
import requests
from datetime import datetime
from django.conf import settings
# from django.contrib.sites.shortcuts import get_current_site
from sugar.simple_crypto import SimpleCrypto


class EmailTask(object):
    ATTRIBUTES = {
        'os': {
            'logo_url':
                'https://os-media-files.s3.amazonaws.com/os.com/email/assets/wide_logo.png',
            'site_name': 'OrangeShine.com',
            'from_name': 'OrangeShine.com',
            'from_email': 'no-reply@orangeshine.com',
            'fax': '213-745-3009',
            'phone': '213-745-3001',
        },
        'cm': {
            'logo_url':
                'https://www.chermuse.com/static/img/logoSimpleBlack.svg',
            'site_name': 'Chermuse.com',
            'from_name': 'Chermuse.com',
            'from_email': 'no-reply@chermuse.com',
            'fax': '213-545-4542',
            'phone': '213-545-4542',
        }
    }

    def __init__(self, request):
        self.request = request
        self.url = self.request.get_host()

        # if get_current_site(request).domain in settings.CM_SITES:
        #     self.logo_url = "https://os-media-files.s3.amazonaws.com/cm.com/email/assets/wide_logo.png"
        #     self._site_prefix = 'cm/'
        #     self.site_name = "CHERMUSE.com"
        #     self.from_name = "CHERMUSE.com"
        #     self.from_email = "no-reply@chermuse.com"
        #     self.fax = "213-545-4542"
        #     self.phone = "213-545-4542"
        # else:
        #     self.logo_url = "https://os-media-files.s3.amazonaws.com/os.com/email/assets/wide_logo.png"
        #     self._site_prefix = ''
        #     self.site_name = "OrangeShine.com"
        #     self.from_name = "OrangeShine.com"
        #     self.from_email = "no-reply@orangeshine.com"
        #     self.fax = "213-745-3009"
        #     self.phone = "213-745-3001"

        self.site = 'cm' if self.url in settings.CM_SITES else 'os'
        self._site_prefix = 'cm/' if self.url in settings.CM_SITES else ''
        self._api_version = '-v2' if self._site_prefix == '' else ''
        for k, v in self.ATTRIBUTES.get(self.site).items():
            setattr(self, k, v)

        # TODO: add api key on api
        self.API_KEY = ""
        self.HEADERS = {'Authorization': "Token %s" % self.API_KEY}

        self.EMAIL_TASK_URL = settings.OS_TASK_URL

    def request_reset_password(self, user_email, user_status='', token=''):
        """
        Request reset password
        """
        context = {
            'token':
                token,
            'user_status':
                user_status,
            'company_name':
                getattr(self.request.user, 'company_name', ''),
            'reset_req_date':
                "%s (PDT)" % datetime.now().strftime('%Y-%m-%dT%H:%M:%S%z')
        }
        subject = "Reset your %s Password" % self.site_name
        email_type = "{}os-reset-password".format(self._site_prefix)
        self._send_email_to_os_tasks(email_type, context, subject, user_email)

    def changed_password(self, user_email=None):
        """
        Inform user password has been changed
        """
        if user_email:
            email_type = '{}os-update-password'.format(self._site_prefix)
            subject = 'Your %s Password has been changed' % self.site_name
            context = {
                'company_name':
                    getattr(self.request.user, 'company_name', ''),
                'updated_timestamp':
                    "%s (PDT)" % datetime.now().strftime('%Y-%m-%dT%H:%M:%S%z')
            }
            self._send_email_to_os_tasks(email_type, context, subject,
                                         user_email)
        else:
            return None

    def order_confirmation(self, email_data, email_target):
        _map = {
            'buyer': 'os-order-confirmation',
            'brand': 'brand-order-confirmation',
            'in-stock': 'instock',
            'pre-order': 'preorder',
            'paypal': 'paypal',
            'credit_card': 'credit-card',
        }
        context, subject, receiver_email = email_data['context'], email_data[
            'subject'], email_data['receiver_email']
        if context['payment'] in ['paypal', 'credit_card']:
            _email_type = None
            if email_target == 'buyer':
                _email_type = '{}{}-{}-{}{}'.format(self._site_prefix,
                                                    _map['buyer'],
                                                    _map[context['order_type']],
                                                    _map[context['payment']],
                                                    self._api_version)
            elif email_target == 'brand':
                _email_type = '{}{}-{}{}'.format(self._site_prefix,
                                                 _map['brand'],
                                                 _map[context['order_type']],
                                                 self._api_version)
            if _email_type:
                self._send_email_to_os_tasks(_email_type, context, subject,
                                             receiver_email)

    def additional_invoice_payment_confirmation(self, email_data):
        _map = {
            'brand': 'brand-additional-invoice-payment',
        }
        context, subject, receiver_email = email_data['context'], email_data[
            'subject'], email_data['receiver_email']
        _email_type = '{}{}{}'.format(self._site_prefix,
                                      _map['brand'],
                                      self._api_version)
        self._send_email_to_os_tasks(_email_type, context, subject, receiver_email)

    def held_order_for_review(self, email_data):
        context, subject, receiver_email = email_data['context'], email_data[
            'subject'], email_data['receiver_email']
        email_type = '{}os-request-auth-form'.format(self._site_prefix)
        self._send_email_to_os_tasks(email_type, context, subject,
                                     receiver_email)

    def hold_for_review_resubmit(self, email_data):
        context, subject, receiver_email = email_data['context'], email_data[
            'subject'], email_data['receiver_email']
        email_type = '{}hold-for-review-resubmit'.format(self._site_prefix)
        self._send_email_to_os_tasks(email_type, context, subject,
                                     receiver_email)

    def email_address_verify(self, email_data):
        receiver_email = email_data['email']
        crypted_email = SimpleCrypto().encrypt(receiver_email)
        if self.site == 'cm':
            subject = 'Complete Your Registration for {}'.format(
                self.site_name)
            context = {
                'verify_url':
                    '{}/verify-email/?vk={}'.format(settings.CM_DOMAIN,
                                                    crypted_email),
                'company_name':
                    email_data.get('company_name', ''),
            }
        else:
            subject = 'Verify your email address'
            context = {
                'verify_url':
                    'https://{}/verify-email/?vk={}'.format(
                        self.url, crypted_email),
                'company_name':
                    email_data.get('company_name', ''),
            }
        email_type = '{}os-email-verify'.format(self._site_prefix)
        self._send_email_to_os_tasks(email_type, context, subject,
                                     receiver_email)

    def change_signin_email(self, email_data):
        receiver_email = email_data['new_email']
        security_key = email_data['security_key']
        subject = 'Change Sign-in Email',
        context = {
            'security_key': security_key,
            'company_name':
                email_data.get('company_name', ''),
        }
        email_type = '{}os-change-signin-email'.format(self._site_prefix)
        self._send_email_to_os_tasks(email_type, context, subject,
                                     receiver_email)

    def registration_approve(self, email_data):
        subject = 'Your new Orangeshine account is approved!'
        receiver_email = email_data['email']
        context = {
            'subject': subject,
        }
        email_type = '{}os-welcome-email'.format(self._site_prefix)
        self._send_email_to_os_tasks(email_type, context, subject, receiver_email)

    def payment_confirmation(self, email_data, email_target):
        _email_type = None
        context, subject, receiver_email = email_data['context'], email_data[
            'subject'], email_data['receiver_email']
        if email_target == 'brand':
            _email_type = '{}brand-payment-confirmation-v2'.format(self._site_prefix,
                                                                   self._api_version)
        elif email_target == 'buyer':
            _email_type = '{}os-payment-confirmation'.format(self._site_prefix)
        self._send_email_to_os_tasks(_email_type, context, subject,
                                     receiver_email)

    def void_confirmation(self, email_target='buyer', **kwargs):
        if email_target == 'buyer':
            _email_type = '{}os-void-by-buyer-instock'.format(
                self._site_prefix)
        elif email_target == 'brand':
            pass
        self._send_email_to_os_tasks(**kwargs)

    def accept_void_request(self, email_target='buyer', **kwargs):
        if email_target == 'buyer':
            pass
        elif email_target == 'brand':
            pass
        self._send_email_to_os_tasks(**kwargs)

    def email_return_request(self, email_target, email_data):
        context, subject, receiver_email = email_data['context'], email_data[
            'subject'], email_data['receiver_email']

        if email_target == 'buyer':
            _email_type = 'return-request-received'
        elif email_target == 'brand':
            _email_type = 'brand-return-request'
        self._send_email_to_os_tasks(_email_type, context, subject,
                                     receiver_email)

    def decline_void_request(self, email_target='buyer', **kwargs):
        if email_target == 'buyer':
            pass
        elif email_target == 'brand':
            pass
        self._send_email_to_os_tasks(**kwargs)

    def message_to_brand(self, context, subject, receiver_email):
        _email_type = 'message-to-brand'
        self._send_email_to_os_tasks(_email_type, context, subject,
                                     receiver_email)

    def _send_email_to_os_tasks(self, email_type, context, subject,
                                receiver_email):
        if not context or not subject or not receiver_email:
            print("[send email] missing information!")
            return False

        url = "%s/email-tasks/transactional/%s/" % (self.EMAIL_TASK_URL,
                                                    email_type)

        if settings.DEBUG:
            receiver_email = settings.DEBUG_TO_EMAIL

        for to_email in receiver_email.split(','):
            try:
                requests.post(url=url,
                              data={
                                  'context': json.dumps(context,
                                                        use_decimal=True),
                                  'subject': subject,
                                  'receiver_email': to_email
                              },
                              headers=self.HEADERS)
                # print("[_send_email_to_os_tasks] POST: url=%s, subject=%s, receiver_email=%s" % (url, subject, to_email))
            except requests.exceptions.RequestException as e:
                print("[_send] POST: url=%s, RequestException - %s (%s)" %
                      (url, str(e), str(type(e))))
                pass
            except Exception as e:
                print("[_send] POST: url=%s, send Exception - %s (%s)" %
                      (url, str(e), str(type(e))))
                pass
