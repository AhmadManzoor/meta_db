from datetime import datetime
from elasticsearch_dsl import (
    DocType,
    Date,
    Text,
    Keyword,
)


class StyleSearchHistory(DocType):
    customer_id = Keyword()
    queries = Text(fields={'raw': Keyword()})
    created_date = Date()

    class Meta:
        index = 'search_history'

    def save(self, **kwargs):
        self.created_date = datetime.now()
        return super().save(**kwargs)
