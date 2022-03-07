from datetime import datetime
from elasticsearch_dsl import (
    DocType,
    Date,
    Float,
    Text,
    Keyword,
    Boolean,
)


class MetaStyle(DocType):
    id = Keyword()
    group_id = Keyword()
    style_number = Keyword()
    brand_id = Keyword()
    brand_name = Keyword()  # TODO: nested
    brand_web_name = Keyword()  # TODO: nested
    is_prevention = Boolean()
    style_name = Text()
    image = Text()
    price = Float()
    sale_price = Float()
    is_plus_size = Boolean()
    is_sale = Boolean()
    segment = Keyword()
    category = Keyword()
    sub_category = Keyword()
    created_date = Date()
    modified_date = Date()
    is_preorder = Boolean()
    preorder_available_date = Date()
    fulfillment = Keyword()
    url = Keyword()
    badges = Text(fields={'raw': Keyword()})
    colors = Text(fields={'raw': Keyword()})
    af_style = Text(fields={'raw': Keyword()})
    af_pattern = Text(fields={'raw': Keyword()})
    af_sleeve = Text(fields={'raw': Keyword()})

    def save(self, **kwargs):
        self.modified_date = datetime.now()
        return super().save(**kwargs)


class OSStyle(MetaStyle):
    class Index:
        name = 'os-styles'


class CMStyle(MetaStyle):
    class Index:
        name = 'cm-styles'
