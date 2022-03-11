from dataclasses import field, fields
from pyexpat import model
from rest_framework import serializers
from meta_db.invoice.invoice_models import MasterInvoiceModel,SubInvoiceModel

class InvoiceSerializer(serializers.ModelSerializer):
    # viewed_id = serializers.IntegerField(source='id')
    color_id = serializers.SerializerMethodField()
    order_id = serializers.SerializerMethodField()
    vendor_id = serializers.SerializerMethodField()
    product_id = serializers.SerializerMethodField()
    sub_order_id = serializers.SerializerMethodField()
    

    def get_order_id(self,obj):
        return obj.id
    def get_sub_order_id(self,obj):
        soids = SubInvoiceModel.objects.filter(master_order=obj.invoice_master_id)
        res = [id.id for id in soids]
        return res


    def get_product_id(self,obj):
        soids = SubInvoiceModel.objects.filter(master_order=obj.invoice_master_id)
        res = [id.id for id in soids]
        return [SubInvoiceModel.objects.get(id=i).item.id for i in res]

       


    def get_vendor_id(self,obj):
        soids = SubInvoiceModel.objects.filter(master_order=obj.invoice_master_id)
        res = [id.id for id in soids]
        return [SubInvoiceModel.objects.get(id=i).brand.id for i in res]

    def get_color_id(self,obj):
        soids = SubInvoiceModel.objects.filter(master_order=obj.invoice_master_id)
        res = [id.id for id in soids]
        return [SubInvoiceModel.objects.get(id=i).color_id for i in res]
        

    class Meta():
        model = MasterInvoiceModel
        fields = ["user_id",
		"order_id",
		"order_status",
        "ordered_date",
        "sub_order_id",
        "product_id",
        "vendor_id",
        "color_id",
        ]
        read_only_fields =fields
    