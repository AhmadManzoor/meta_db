import os
import sys
import django
import logging
import csv


from datetime import datetime, timedelta

date_strftime_format = "%d-%b-%y %H:%M:%S"
message_format = "%(asctime)s - %(levelname)s - %(message)s"

logging.basicConfig(format= message_format, datefmt= date_strftime_format, filename='Initialmigration_products.log',level=logging.DEBUG)

sys.path.append("..")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "os_search.settings")
django.setup()
# from api.serializers.style import StyleListSerializer
# from apps.models.style import StyleListModel, ProductModel
from apps.models.style_detail_models import StyleModel

from api.serializers.detail import StyleDetailSerializer

from elasticsearch_dsl import Q
from search.handler import SearchHandler
from handler import post_request_for_elastic

f = open('nocategory.csv', 'w')
writer = csv.writer(f)


def initialize_es():
    ##################################################
    # instead call this:
    # $ curl -X DELETE 'http://10.10.67.198:9200/_all'
    # {"acknowledged":true}
    ##################################################
    print("[initialize_es]")
    site = "os"
    # _hdr = SearchHandler(site=site)
    # _all = _hdr.get_all()     # TBD
    # _resp = _all.delete()
    print("[initialize_es] curl -X DELETE http://10.10.67.198:9200/_all")


def main(time_from_str, time_to_str, action_type="update"):
    """
    [CREATE/UPDATED][0] 00012460    2010-05-18 00:00:00     2020-03-13 09:23:00
    [CREATE/UPDATED][65546] 93380677        2021-08-22 01:01:00     2021-08-22 01:02:00
    [CREATE/UPDATED][65547] 93380678        2021-08-22 01:02:00     2021-08-22 01:02:00
    [CREATE/UPDATED][65548] 93380679        2021-08-22 01:05:00     2021-08-22 01:05:00
    """
    print("[main]")

    site = "os"
    # _hdr = SearchHandler(site=site)

    time_from = datetime.strptime(time_from_str, "%Y%m%d%H%M%S")
    time_to = datetime.strptime(time_to_str, "%Y%m%d%H%M%S")
    # print("[main] %s <= t < %s"% (time_from, time_to))
    logging.info("Import started %s <= t < %s"% (time_from, time_to))


    if action_type == "recreate":
        initialize_es()
        # _styles = getattr(StyleModel.objects, site).filter(
        #     created_date__gte=time_from, created_date__lt=time_to
        # ).order_by('created_date')
        # print("[main] _styles (create): %d" % _styles.count())
        _styles = StyleModel.objects.filter(
            origin_date__gte=time_from, origin_date__lt=time_to
        ).order_by('origin_date')
        # print("[main] _styles (create): %d" % _styles.count())
        logging.info("[main] _styles (create): %d" % _styles.count())
    else:
        # _styles = getattr(StyleModel.objects, site).filter(
        #    updated_date__gte=time_from, updated_date__lt=time_to
        # ).order_by('updated_date')
        # print("[main] _styles (create): %d" % _styles.count())
        _styles = StyleModel.objects.filter(
                    updated__gte=time_from, updated__lt=time_to
                ).order_by('updated')
        print("[main] _styles (create): %d" % _styles.count())
        _deletes = (
            ProductModel.objects.filter(brand__site=site.upper())
            .values_list("id", flat=True)
            .filter(updated__gte=time_from, updated__lte=time_to, _is_active="N")
        )
        print("[main] _styles (delete): %d" % _deletes.count())

        for idx in _deletes:
            s = _hdr.get(id=idx)
            if s:
                try:
                    s.delete()
                    print("[DELETED][%s] %s\t%s\t%s" % (idx, s.id, s.created, getattr(s, 'updated', '-')))
                except:
                    print("[DELETED][%s] %s\t%s\t%s (skipping)" % (
                    idx, s.id, s.created, getattr(s, 'updated', '-')))

    for idx, s in enumerate(_styles):
        try:
            #_hdr.create_or_update(s)
            data = StyleDetailSerializer(s).data
            if data['category'] != "":
                post_request_for_elastic(logging, 'stg-product',data)
                logging.info("[CREATE/UPDATED][%s] %s\t%s\t%s" % (idx, s.id, s.created, getattr(s, 'updated', '-')))
            else:
                writer.writerow(data['product_id'])

        except Exception as e:
            # print(e)
            logging.warning("[CREATE/UPDATED][%s] %s\t%s\t%s\t %s(skipping)" % (idx, s.id, s.created, getattr(s, 'updated', '-'),str(e)))
            # logging.WARNING(str(e))
            pass


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
    time_from = "20000101000000"
    time_to   = "20220201000000"

    action_type = "recreate"
    # action_type = "update"
    main(time_from, time_to, action_type)
