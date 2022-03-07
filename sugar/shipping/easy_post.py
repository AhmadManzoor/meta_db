import datetime
import easypost
from django.conf import settings
from django.db import IntegrityError
from sugar.sugars import Sugars

class EasyPost(object):
    UPS_CARRIER_ID = u'ca_b8170c2f18794b1198ea7e60e9767253'
    # USPS_CARRIER_ID = u'ca_d8c6c8b7e9a8494bb8a7df408ebb199d'
    FEDEX_CARRIER_ID = u'ca_5d7f05885ee44033bec727d936558bb4'

    def __init__(self):
        easypost.api_key = settings.EASY_POST_API_KEY

    def address(self, kwargs):
        keys = ['name', 'street1', 'street2', 'city', 'state', 'zip', 'country']
        for k in kwargs.keys():
            if k not in keys:
                raise KeyError('cannot accept %s' % k)
        try:
            addr = easypost.Address.create(
                verify=["delivery"],
                name=kwargs['name'],
                street1=kwargs['street1'],
                street2=kwargs['street2'],
                city=kwargs['city'],
                state=kwargs['state'],
                zip=kwargs['zip'],
                country=kwargs['country']
            )
            return addr
        except Exception as e:
            print(e)
            raise IntegrityError('fail to verify address')

    def validate_address(self, form_data=None):
        result = dict()
        try:
            _tmp_address = easypost.Address.create(
                verify=["delivery"],
                name="%s %s" % (form_data.get('first_name'), form_data.get('last_name')),
                street1=form_data.get('address1'),
                street2=form_data.get('address2'),
                city=form_data.get('city'),
                state=form_data.get('state'),
                zip=form_data.get('zipcode'),
                country=form_data.get('country')
            )
        except easypost.Error as e:
            print("[validate_address] Exception:: %s " % str(e))
            result['message'] = 'currently not unavailable. Please try again'
            return result, 500

        suggested_address = dict()
        suggested_address['address1'] = _tmp_address.street1
        suggested_address['address2'] = _tmp_address.street2
        suggested_address['city'] = _tmp_address.city
        suggested_address['state'] = _tmp_address.state
        suggested_address['zipcode'] = _tmp_address.zip
        result['suggested_address'] = suggested_address
        result['origin_address'] = form_data
        if _tmp_address.verifications.delivery.success:
            if form_data.get('address1').upper() == _tmp_address.street1.upper() and \
                form_data.get('address2').upper() == _tmp_address.street2.upper() and \
                form_data.get('city').upper() == _tmp_address.city.upper() and \
                form_data.get('state').upper() == _tmp_address.state.upper():
                result['type'] = 'same_with_suggest'
                form_data['address1'] = _tmp_address.street1
                form_data['address2'] = _tmp_address.street2
                form_data['city'] = _tmp_address.city
                form_data['state'] = _tmp_address.state
                form_data['zipcode'] = _tmp_address.zip
            else:
                result['type'] = 'suggested_address'

            return result, 200
        else:
            if _tmp_address.verifications.delivery.errors:
                result['message'] = _tmp_address.verifications.delivery.errors[0].message
                result['type'] = 'validation_error'

            return result, 200

    def get_shipping_method(self, sp_address, fulfillment, exp_shipout_date):
        if not sp_address or not fulfillment or not exp_shipout_date:
            return None

        _to_address, _from_address = self._get_addresses(sp_address, fulfillment)
        _parcel = self._create_parcel()
        return self._get_shipping_method(_to_address,
                                         _from_address,
                                         _parcel,
                                         exp_shipout_date)

    def _get_addresses(self, sp_address, fulfillment):
        to_address = None
        from_address = None

        if sp_address and fulfillment:
            try:
                to_address = easypost.Address.create(
                    name="%s %s" % (sp_address.first_name, sp_address.last_name),
                    street1=sp_address.address1,
                    street2=sp_address.address2,
                    city=sp_address.city,
                    state=sp_address.state,
                    zip=sp_address.zipcode,
                    country=sp_address.country
                )
                from_address = easypost.Address.create(
                    company=fulfillment.fulfillment,
                    street1=fulfillment.address1,
                    street2=fulfillment.address2,
                    city=fulfillment.city,
                    state=fulfillment.state,
                    zip=fulfillment.zipcode,
                    country=fulfillment.country
                )
            except easypost.Error as e:
                print("[EasyPost::_get_addresses] Exception - %s" % e)
                return None, None

        return to_address, from_address

    def _create_parcel(self):
        parcel = None
        try:
            parcel = easypost.Parcel.create(
                length=5.0,
                width=5.0,
                height=5.0,
                weight=20.0
            )
        except easypost.Error as e:
            print("[_create_parcel] Exception - %s (%s)" % (str(e), str(type(e))))
            raise e

        return parcel

    def _get_shipping_method(self, to_address, from_address, parcel, exp_shipout_date):
        _shipment = None

        try:
            carrier_account = [self.UPS_CARRIER_ID, self.FEDEX_CARRIER_ID]
            _shipment = easypost.Shipment.create(
                to_address=to_address,
                from_address=from_address,
                parcel=parcel,
                carrier_accounts=carrier_account
            )
        except Exception as e:
            print("[EasyPost::_get_shipping_method] Exception - %s (%s)" % (str(e), str(type(e))))
            return None

        _tmp_method_dict = dict()
        exp_shipout_date = datetime.datetime.strptime(exp_shipout_date, "%m/%d/%Y")
        if _shipment:
            for method in _shipment.rates:
                if method.service not in _tmp_method_dict:
                    exp_delivery_date = None
                    if type(method.delivery_days) == int and method.delivery_days > 0:
                        exp_delivery_date = Sugars.date_by_adding_business_days(
                            exp_shipout_date, method.delivery_days).strftime('%m/%d/%Y')
                    _tmp_method_dict[method.service] = {
                        "carrier": method.carrier,
                        "currency": method.currency,
                        # "rate": _rate,
                        "service": method.service,
                        "delivery_date": exp_delivery_date,
                        "delivery_days": method.delivery_days
                    }

        return _tmp_method_dict



