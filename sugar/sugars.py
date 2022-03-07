import datetime
import re
import pytz
import uuid
import datetime
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from bs4 import BeautifulSoup
from meta_db.models import ZipCodeListModel
from decimal import Decimal, ROUND_HALF_UP
from random import randrange


class Sugars(object):
    def __init__(self):
        self.alphabet_options = [
            '#', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
            'U', 'V', 'W', 'X', 'Y', 'Z'
        ]

    @staticmethod
    def to_utc(_time):
        _tz = pytz.timezone(settings.TIME_ZONE)
        _time = _tz.localize(_time)
        return _time.astimezone(pytz.utc)

    @staticmethod
    def is_cm_site(request=None):
        return request and get_current_site(request).domain in settings.CM_SITES

    @staticmethod
    def is_approved(request=None, brand_id=''):
        """
        return if the brand (brand_id) approved the customer to see the price and check-in or not
        :param request: request
        :param brand_id: the brand (brand_id) in interest
        :return: approved (True) or not approved (False)
        """
        if request and brand_id:
            if brand_id not in request.session.get('approved_brands', []):
                return False
        return True

    @staticmethod
    def get_ip_address(request):
        """
        get ip address from user client
        :param request:
        :return: ip
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    @staticmethod
    def remove_emoji_from_registration_form(form_data: dict):
        import emoji
        emoji_re = emoji.get_emoji_regexp()
        for k, v in form_data.items():
            if k in ('company_name', 'first_name', 'last_name'):
                try:
                    form_data[k] = emoji_re.sub(r'', v)
                except Exception as e:
                    print("REGISTER ERROR ", e)
        return form_data

    @staticmethod
    def is_california_zipcode(form_data=None):
        if form_data.get('country').code == u'US' and Sugars.validate_zipcode(form_data.get('zip_code')).get(
                'state', '') == u'CA':
            return True
        else:
            return False

    @staticmethod
    def validate_zipcode(zipcode=None):
        try:
            return ZipCodeListModel.objects.get(pk=zipcode)
        except ZipCodeListModel.DoesNotExist:
            return None

    @staticmethod
    def clean_me(html):
        """
        remove line script and javascript
        """
        soup = BeautifulSoup(html, "html.parser")  # create a new bs4 object from the html data loaded
        for tag in soup():
            for attribute in ["class", "id", "name", "style", "javascript"]:
                del tag[attribute]
        return str(soup)

    @staticmethod
    def uuid(length=32):
        return uuid.uuid4().hex[:length]

    @staticmethod
    def camel_to_snake(obj):
        if isinstance(obj, str):
            s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', obj)
            return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
        if isinstance(obj, list):
            _tmp = []
            for o in obj:
                s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', o)
                _tmp.append(re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower())
            return _tmp
        if isinstance(obj, dict):
            _tmp = {}
            for k, v in obj.items():
                s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', k)
                _tmp[re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()] = v
            return _tmp
        return obj

    @staticmethod
    def extract_domain_from_email(email=''):
        extracted = ''
        if email:
            t = email.split('@')
            if len(t) == 2:
                extracted = t[1]
        return extracted

    @staticmethod
    def date_by_adding_business_days(from_date, add_days, holidays=[]):
        business_days_to_add = add_days
        current_date = from_date
        while business_days_to_add > 0:
            current_date += datetime.timedelta(days=1)
            weekday = current_date.weekday()
            if weekday >= 5:  # sunday = 6
                continue
            if current_date in holidays:
                continue
            business_days_to_add -= 1
        return current_date

    @staticmethod
    def round_half_up(number, exp=Decimal('.01')):
        return Decimal(str(number)).quantize(exp, rounding=ROUND_HALF_UP)

    def get_random_alphabet_or_number_option(self):
        return self.alphabet_options

    def get_random_alphabet_or_number(self, options: set):
        if options:
            random_alphabet = randrange(len(options))
        else:
            random_alphabet = randrange(27)
        return self.alphabet_options[random_alphabet]

    @staticmethod
    def remove_multiple_characters(original_string, characters_to_remove):
        """
        :param characters_to_remove: Put the multiple characters that will be removed in one string.
        """
        pattern = "[" + characters_to_remove + "]"
        return re.sub(pattern, "", original_string)
