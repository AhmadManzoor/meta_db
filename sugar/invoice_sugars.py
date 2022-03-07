import re

from datetime import datetime, timedelta
from apps.orders.models.master_invoice_models import MasterInvoiceModel


class InvoiceSugars(object):
    # @staticmethod
    # def send_order_confirmation(inv=None):
    #     if order.__class__.__name__ != 'MasterInvoiceModel':
    #         raise ValueError("input Master Invoice object")

    # TODO: modulate and refactoring are needed
    def get_fraud_score(self, order):
        if order.__class__.__name__ not in [
                'MasterInvoiceModel', 'MasterPOModel'
        ]:
            raise ValueError("input Master Invoice object")
        if order.payment_method_id == 'WH20':
            return 4

        elif order.payment_method_id != 'WH1':
            return None

        user = order.user
        payment_profile_id = order.payment_profile_id

        mail_state = order.mail_state
        mail_address = "%s %s %s %s" % (
            order.mail_city.strip(), order.mail_state.strip(),
            order.mail_zipcode.strip()[:5], order.mail_country.strip())
        bill_state = order.bill_state
        bill_address = "%s %s %s %s" % (
            order.bill_city.strip(), order.bill_state.strip(),
            order.bill_zipcode.strip()[:5], order.bill_country.strip())
        is_matching_street = False
        if order.mail_address1.strip().upper() == order.bill_address1.strip(
        ).upper():
            is_matching_street = True
        else:
            # check if mail street number == billing street number
            p = re.compile('^\d+')
            mail_street_num = p.search(order.mail_address1.strip()).group() \
                if order.mail_address1 and p.search(order.mail_address1.strip()) else ""

            bill_street_num = p.search(order.bill_address1.strip()).group() \
                if order.bill_address1 and p.search(order.bill_address1.strip()) else ""

            if mail_street_num and bill_street_num and \
                            mail_street_num == bill_street_num:
                # print("[_get_fraud_score] street num matching : %s, %s" %
                #       (order.mail_address1, order.bill_address1))
                is_matching_street = True

        fraud_score = 0
        if user and payment_profile_id:
            contact_full_name = "{} {}".format(
                user.first_name if user.first_name else '',
                user.last_name if user.last_name else '').strip().lower()
            bill_full_name = "{} {}".format(
                order.bill_first_name if order.bill_first_name else '',
                order.bill_last_name
                if order.bill_last_name else '').strip().lower()

            if self._is_fraud_score_5(user, payment_profile_id):
                fraud_score = 5
            elif mail_address.upper() == bill_address.upper() and is_matching_street and \
                    contact_full_name == bill_full_name:
                fraud_score = 4
            elif mail_state.upper() != bill_state.upper():
                fraud_score = 1
            elif self._is_fraud_score_3(user, payment_profile_id):
                fraud_score = 3
            else:
                fraud_score = 2

            # add one star if customer purchased before three months
            if fraud_score < 5 and self._is_customer_purchased_before_three_month(
                    user):
                fraud_score = fraud_score + 1

            # make 3, if this card has been confirmed before.
            if fraud_score == 2 and order.auth_form_confirmed:
                fraud_score = 3
        return fraud_score

    def _is_fraud_score_5(self, user, payment_profile_id):
        start_date = datetime.now() - timedelta(730)
        end_date = datetime.now() - timedelta(75)
        filter = dict(user_id=user.customer_id,
                      payment_profile_id=payment_profile_id,
                      invoice_status__in=(
                          4,
                          12,
                          13,
                      ),
                      ordered_date__range=(start_date, end_date))
        if MasterInvoiceModel.objects.filter(**filter).exists():
            return True
        else:
            return False

    def _is_fraud_score_3(self, user, payment_profile_id):
        start_date = datetime.now() - timedelta(75)
        end_date = datetime.now() - timedelta(10)
        filter = dict(user_id=user.customer_id,
                      payment_profile_id=payment_profile_id,
                      invoice_status__in=(
                          4,
                          12,
                          13,
                      ),
                      ordered_date__range=(start_date, end_date))
        if MasterInvoiceModel.objects.filter(**filter).exists():
            return True
        else:
            return False

    def _is_customer_purchased_before_three_month(self, user):
        before_six_month_date = datetime.now() - timedelta(91)
        filter = dict(user_id=user.customer_id,
                      invoice_status__in=(
                          4,
                          12,
                          13,
                      ),
                      ordered_date__lte=(before_six_month_date))
        if MasterInvoiceModel.objects.filter(**filter).exists():
            return True
        else:
            return False
