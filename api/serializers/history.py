from dataclasses import field, fields
from pyexpat import model
from rest_framework import serializers
from apps.models.style_detail_models  import StyleViewHistoryModel

class StyleViewSerializer(serializers.ModelSerializer):
    viewed_id = serializers.IntegerField(source='id')
    product_id = serializers.CharField(source='item_id')
    user_id =serializers.CharField(source='customer_id')
    nDate = serializers.CharField(source='created_date')

    class Meta():
        model = StyleViewHistoryModel
        fields = ['viewed_id','product_id','user_id', 'nDate' ]
        read_only_fields =fields