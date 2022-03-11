import os
import sys
import django

import logging

date_strftime_format = "%d-%b-%y %H:%M:%S"
message_format = "%(asctime)s - %(levelname)s - %(message)s"

logging.basicConfig(format= message_format, datefmt= date_strftime_format, filename='Initialmigration_orders.log',level=logging.DEBUG)


sys.path.append("..")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "os_search.settings")
django.setup()

from datetime import datetime, timedelta
from meta_db.user.models import  UserModel
from handler import post_request_for_elastic
from api.serializers.user import UserSerializer



def main(time_from_str, time_to_str, action_type="update"):
    time_from = datetime.strptime(time_from_str, "%Y%m%d%H%M%S")
    time_to = datetime.strptime(time_to_str, "%Y%m%d%H%M%S")
    logging.info("[main] %s <= t < %s"% (time_from, time_to))

    _users = UserModel.objects.filter(
                    date_joined__gte=time_from, date_joined__lt=time_to
                ).order_by('date_joined')
    logging.info("[main] _users (create): %d" % _users.count())

    for idx, s in enumerate(_users):
            try:
                #_hdr.create_or_update(s)
                data = UserSerializer(s).data
                print(data)
                # post_request_for_elastic ('stg-viewedhistory',data)
                print("[CREATE/UPDATED][%s] %s\t%s\t%s" % (idx, s.id, s.date_joined, getattr(s, 'date_joined', '-')))
            except Exception as e:
                print("[CREATE/UPDATED][%s] %s\t%s\t%s (skipping)" % (
                idx, s.id, s.date_joined, getattr(s, 'date_joined', '-')) , e)
                pass

time_from = "20000101000000"
time_to   = "20220201000000"

action_type = "recreate"
# action_type = "update"
main(time_from, time_to, action_type)


