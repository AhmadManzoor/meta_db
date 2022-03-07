from django.db.models import Sum

from apps.cart.models import CartModel
from meta_db.models import CheckoutStepTraceModel


class CheckoutSugars(object):
    @staticmethod
    def trace_checkout_step(customer_id, step):
        try:
            cart_amount = CartModel.objects.all_active_and_checkout().filter(
                user_id=customer_id).aggregate(
                Sum('sub_total')).get('sub_total__sum')
        except CartModel.DoesNotExist:
            # log here
            cart_amount = 0.00

        try:
            CheckoutStepTraceModel(customer_id=customer_id,
                                   step=step,
                                   cart_amount=cart_amount).save()
        except CheckoutStepTraceModel.DoesNotExist:
            pass
