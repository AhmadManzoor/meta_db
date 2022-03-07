import certifi
from django.conf import settings
from search.docs.style import OSStyle, CMStyle
from search.docs.search_history import StyleSearchHistory
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl.query import MoreLikeThis
from elasticsearch import Elasticsearch
from api.serializers.style import StyleListSerializer


class SearchHandler(object):
    def __init__(self, site, page_number=1, page_size=48):
        if not site:
            raise Exception("No site type")
        self.style_object = CMStyle if site == "cm" else OSStyle
        # connections.create_connection(hosts=settings.ELASTIC_SEARCH_HOSTS, timeout=30)
        # self.client = Elasticsearch()
        self.client = Elasticsearch(hosts=['https://orangeshine.es.us-central1.gcp.cloud.es.io:9243'],
                                    use_ssl=True,
                                    ca_certs=certifi.where(),
                                    http_auth=settings.ELASTIC_CLOUD_AUTH,
                                    timeout=30
                                    )
        try:
            connections.create_connection(hosts=['https://orangeshine.es.us-central1.gcp.cloud.es.io:9243'],
                                          http_auth=settings.ELASTIC_CLOUD_AUTH,
                                          use_ssl=True,
                                          ca_certs=certifi.where())
        except Exception as e:
            print("connection error = ", e)
        self.page_size = page_size
        self.page_number = page_number

    def get(self, id):
        return self.style_object.get(id=id, ignore=404)

    def get_all(self):
        return self.style_object.search()

    def create_or_update(self, obj):
        doc = StyleListSerializer(obj).data
        style = self.style_object(**doc)
        style.meta.id = obj.pk
        try:
            style.save()
        except Exception as err:
            print("ERROR: \n\n", err)

    def search(self, queries):
        # id
        # style number: must, match
        # style name
        # brand name
        # category
        # colors
        # style, pattern, sleeve
        # badges
        _query = self.style_object.search()
        for q in queries:
            _query = _query.query(q)
        s = self.pagination(_query)
        result = s.execute()
        # elasticsearch 7.X: hits.total return as an object with a `value` and a `relation`.
        if isinstance(result.hits.total, dict) and result.hits.total.get('value'):
            total = result.hits.total.get('value')
        else:
            total = result.hits.total
        return {
            'total': total,
            'docs': [hit.to_dict() for hit in result.hits],
        }

    def more_like_style(self, pk, query, size=8):
        s = self.style_object.search()
        s = s.query(
            MoreLikeThis(
                like=query,
                fields=[
                    "brand_name",
                    "segment",
                    "category",
                    "sub_category",
                    "style_name",
                    "colors",
                ],
                min_term_freq=1,
                max_query_terms=12,
            )
        )
        s = s.exclude("match", id=pk)
        s = s[:size]
        result = s.execute()
        return {
            "total": result.hits.total,
            "docs": [hit.to_dict() for hit in result.hits],
        }

    def pagination(self, search):
        _start = (self.page_number - 1) * self.page_size
        _end = _start + self.page_size
        return search[_start:_end]

    @staticmethod
    def save_query(query):
        try:
            doc = {
                "queries": query.split(" "),
            }
            q = StyleSearchHistory(**doc)
            q.save()
        except Exception as e:
            print("[SAVE QUERY] ", e)
            pass

    def delete_inactive_brand(self, brand_id):
        s = self.style_object.search()
        _query = s.query("match", brand_id=brand_id)
        _ = _query.delete()
