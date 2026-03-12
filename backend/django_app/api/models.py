from django.db import models
  
class Store(models.Model):
    name = models.CharField(max_length=100)
    zip = models.IntegerField()
    address = models.CharField(max_length=50)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    hour_open = models.TimeField()
    hour_close = models.TimeField()

    class Meta:
        db_table = 'api_store'  
    def __str__(self):
        return self.name
    
class Item(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
 

class GroceryItem(models.Model):
    store_id = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='items')
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    brand = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Updated
    availability = models.PositiveIntegerField()

    class Meta:
        db_table = 'api_groceryitem'  # Ensure table name matches MySQL

    def __str__(self):
        return self.name
 
