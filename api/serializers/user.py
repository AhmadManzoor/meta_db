from dataclasses import field, fields
from pyexpat import model
from rest_framework import serializers
from meta_db.user.models import  UserModel
from meta_db.my_pick.models import  MyPickModel
from apps.models.brand import FavoriteBrandModel

class UserSerializer(serializers.ModelSerializer):
    user_id = serializers.SerializerMethodField()
    my_picks = serializers.SerializerMethodField()
    favorite_vendors = serializers.SerializerMethodField()

    def get_my_picks(self, obj):
        my_pick_list = MyPickModel.objects.filter(id=obj.customer_id)
        print(obj.customer_id)
        # print(my_pick_list.query)
        return [mypick.item_id for mypick in my_pick_list] 


    def get_favorite_vendors(self,obj) :
        my_vendor_list = FavoriteBrandModel.objects.filter(customer_id='WB1044')
        return [favoriteVendor.brand.id for favoriteVendor in my_vendor_list] 
    
    def get_user_id(self ,obj):
        return obj.customer_id


    class Meta():
            model = UserModel
            fields = ['user_id','my_picks','favorite_vendors' ]
            read_only_fields =fields



