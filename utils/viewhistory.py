import os
import sys
import django
sys.path.append("..")
django.setup()
from datetime import datetime, timedelta

from api.serializers.history import StyleViewSerializer

from apps.models.style_detail_models import StyleViewHistoryModel
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "os_search.settings")


def main(time_from_str, time_to_str, action_type="update"):
    time_from = datetime.strptime(time_from_str, "%Y%m%d%H%M%S")
    time_to = datetime.strptime(time_to_str, "%Y%m%d%H%M%S")
    print("[main] %s <= t < %s"% (time_from, time_to))

    _viewedHistory = StyleViewHistoryModel.objects.filter(
                    created_date__gte=time_from, created_date__lt=time_to
                ).order_by('created_date')[:2]
    print("[main] _viewedHistory (create): %d" % _viewedHistory.count())

    for idx, s in enumerate(_viewedHistory):
            try:
                #_hdr.create_or_update(s)
                data = StyleViewSerializer(s).data
                post_request_for_elastic ('stg-viewedhistory',data)
                print("[CREATE/UPDATED][%s] %s\t%s\t%s" % (idx, s.id, s.created_date, getattr(s, 'updated_date', '-')))
            except Exception as e:
                print("[CREATE/UPDATED][%s] %s\t%s\t%s (skipping)" % (
                idx, s.id, s.created_date, getattr(s, 'updated_date', '-')) , e)
                pass

time_from = "20000101000000"
time_to   = "20220201000000"

action_type = "recreate"
# action_type = "update"
main(time_from, time_to, action_type)