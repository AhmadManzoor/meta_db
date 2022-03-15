import os
import sys
import django
import logging
import traceback

from datetime import datetime, timedelta

date_strftime_format = "%d-%b-%y %H:%M:%S"
message_format = "%(asctime)s - %(levelname)s - %(message)s"

logging.basicConfig(format= message_format, datefmt= date_strftime_format, level=logging.DEBUG,filename='os_migration.log') #
sys.path.append("..")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "os_search.settings")
django.setup()
from apps.models.style_detail_models import StyleModel
from api.serializers.detail import StyleDetailSerializer
from handler import post_request_for_elastic


def main(time_from_str, time_to_str, action_type="update"):
    time_from = datetime.strptime(time_from_str, "%Y%m%d%H%M%S")
    time_to = datetime.strptime(time_to_str, "%Y%m%d%H%M%S")
    logging.info("Import started %s <= t < %s"% (time_from, time_to))

    _styles = StyleModel.objects.select_related("brand","brand_category","os_category_master","os_category_sub").filter(
        origin_date__gte=time_from, origin_date__lt=time_to,
    ).order_by('origin_date')

    count = _styles.count()
    print("[main] _styles (create): %d" %count)
    
    for s in range(0,count,100):
        chunk_list=[]
        chunk = _styles[s:s+100]
        chunk_time = datetime.now()
        print(chunk.query)
        for ch in chunk:
            print(f'time taken:{datetime.now()-now} with query:')
            try:
                now=datetime.now()
                data = StyleDetailSerializer(ch).data
                print('time taken in serialization:', datetime.now()-now)

                if data['category'] != "" and data['brand_name']!='NOBRANDNAME':
                    chunk_list.append(data)                
                else:
                    logging.error("no category or brandname for {}".format(ch.id))                    
            except Exception as e:
                print(traceback.print_exc())
                logging.warning("there was an error {}".format(str(e)))
                pass
            
        print('time taken in overall serialization:', datetime.now()-chunk_time)



        if len(chunk_list) > 0 :
            try:
                # post_request_for_elastic(logging, 'os-product',chunk_list)           
                logging.info("{} records inserted".format(len(chunk_list)))
                print("{} records inserted".format(len(chunk_list)))
            except Exception as e:
                logging.critical("request failed for chunk {} with error {} ".format(s, str(e)))

        else:
            logging.info("500 records missed")
            print("500 records missed")




if __name__ == '__main__':
    """
    # 2014: 750
    # 2015: 3674
    # 2016: 6970
    # 2017: 15165
    # 2018: 52055
    # 2019: 106982
    # 2020: 199361
    # 2021-01: 26393
    # 2021-02: 26478
    # 2021-03: 33574
    # 2021-04: 35770
    # 2021-05: 39989
    # 2021-06: 65164
    # 2021-07: 78604
    # 2021-08: 65549 (current)
    """
    time_from = "20210101000000" #20211001000000
    time_to   = "20211001000000"

    action_type = "recreate"
    # action_type = "update"

    main(time_from, time_to, action_type)