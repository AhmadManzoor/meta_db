from django.db import IntegrityError
from apps.styles.models.style_detail_models import StyleViewHistoryModel


class StyleSugars(object):
    @staticmethod
    def save_view_history(item_id, customer_id, url):
        try:
            StyleViewHistoryModel.objects.create(
                item_id=item_id,
                customer_id=customer_id,
                url=url
            )
        except IntegrityError as e:
            print(e)
            pass
