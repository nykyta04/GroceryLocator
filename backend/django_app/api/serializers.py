from rest_framework import serializers
from .models import GroceryItem, Store, Item
from datetime import datetime

class StoreSerializers(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'

class GroceryItemSerializers(serializers.ModelSerializer):
    item_name  = serializers.CharField(source="item_id.name", read_only=True)
    store_name = serializers.CharField(source="store_id.name", read_only=True)
    price_display = serializers.SerializerMethodField()
    availability_display = serializers.SerializerMethodField()

    class Meta:
        model = GroceryItem
        fields = [
            "id",
            "name",
            "brand",
            "price",
            "availability",
            "item_id",
            "store_id",
            "item_name",
            "store_name",
            "price_display",
            "availability_display",
        ]

    def get_price_display(self, obj):
        return obj.price if obj.price is not None else "Not available"
    
    def get_availability_display(self, obj):
        if obj.availability is None:
            return "Not available"
        elif obj.availability == 0:
            return "Out of Stock"
        else:
            return f"In Stock ({obj.availability})"
    

class GroceryListSerializer(serializers.Serializer):
    items = serializers.ListField(child=serializers.CharField())


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

class StoreSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class meta:
        model = Store
        fields = ['id', 'name', 'zip', 'address', 'hour_open', 'status']

    def get_status(self, obj):
        """Return whether the store is currenlty open or closed."""
        now = datetime.now().time()
        if obj.hour_open and obj.hour_close:
            if obj.hour_open <= now <= obj.hour_close:
                return "Open"
            else:
                return "closed"
        return "Hours unavailable"
