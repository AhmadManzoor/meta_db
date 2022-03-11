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
from meta_db.invoice.invoice_models import  MasterInvoiceModel
from handler import post_request_for_elastic
from api.serializers.invoice import InvoiceSerializer



def main(time_from_str, time_to_str, action_type="update"):
    logging.info("Initial migration of orders started")
    time_from = datetime.strptime(time_from_str, "%Y%m%d%H%M%S")
    time_to = datetime.strptime(time_to_str, "%Y%m%d%H%M%S")
    logging.info("[main] %s <= t < %s"% (time_from, time_to))

    _orders = MasterInvoiceModel.objects.filter(
                    created_date__gte=time_from, created_date__lt=time_to
                ).order_by('created_date')[2:4]
    logging.info("[main] _orders (create): %d" % _orders.count())

    for idx, s in enumerate(_orders):
            try:
                #_hdr.create_or_update(s)
                data = InvoiceSerializer(s).data
                temp = []
                for i in range (len(data['sub_order_id'])):
                    
                    temp.append({'user_id': data['user_id'], 'order_id': data['order_id'], 'ordered_date': data['ordered_date'],
                     'sub_order_id':data['sub_order_id'][i], 'vendor_id': data['vendor_id'][i], 'color_id': data['color_id'][i],
                     'product_id':data['product_id'][0] })
                    # print(temp)
                post_request_for_elastic (logging,'stg-orders',temp)
                logging.info("[CREATE/UPDATED][%s] %s\t%s\t%s" % (idx, s.id, s.created_date, getattr(s, 'updated_date', '-')))
            except Exception as e:
                logging.warning("[CREATE/UPDATED][%s] %s\t%s\t%s (skipping)" % (
                idx, s.id, s.created_date, getattr(s, 'updated_date', '-')) , str(e))
                pass

time_from = "20000101000000"
time_to   = "20220201000000"

action_type = "recreate"
# action_type = "update"
main(time_from, time_to, action_type)