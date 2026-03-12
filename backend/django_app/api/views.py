from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.decorators import action  # Added for @action
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q  # Added for Q
from .models import Store, GroceryItem, Item
from .serializers import StoreSerializers, GroceryItemSerializers, GroceryListSerializer, ItemSerializer
from math import radians, sin, cos, sqrt, atan2
import pgeocode # Added for geocoding and distance calculation 

# Haversine distance in miles 
def haversine_distance(lat1, lon1, lat2, lon2):
    R = 3958.8  # Earth radius in miles
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c 

# Create your views here.
class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializers
    
    # Find the closest store to a Zip code
    @action(detail=False, methods=['get'], url_path='nearest')
    def nearest(self, request):
        """
         Return the single closest store to a given ZIP.
        GET /api/stores/nearest/?zip=28223
        """
        zip_code = request.query_params.get('zip')
        if not zip_code or len(zip_code) != 5:
            return Response({"message": "Provide a valid 5-digit zip."},
                            status=status.HTTP_400_BAD_REQUEST)

        nomi = pgeocode.Nominatim('us')
        loc = nomi.query_postal_code(zip_code)
        if loc is None or loc.latitude is None or loc.longitude is None:
            return Response({"message": "ZIP not found."}, status=status.HTTP_404_NOT_FOUND)

        lat, lon = float(loc.latitude), float(loc.longitude)

        candidates = []
        for s in Store.objects.all():
            if s.latitude is not None and s.longitude is not None:
                dist = haversine_distance(lat, lon, float(s.latitude), float(s.longitude))
                candidates.append((dist, s))

        if not candidates:
            return Response({"message": "No stores with coordinates available."},
                            status=status.HTTP_200_OK)

        candidates.sort(key=lambda x: x[0])
        dist, store = candidates[0]

        data = self.get_serializer(store).data
        data["distance_mi"] = round(dist, 2)
        return Response({"closest": data}, status=status.HTTP_200_OK)
    
    # List all stores from ZIP
    @action(detail=False, methods=['get'], url_path='nearby')
    def nearby(self, request):
        """
        Story 10: Return all stores sorted by distance for a given ZIP,
        filtered by radius (miles).
        GET /api/stores/nearby/?zip=28223&radius=10
        If radius is excluded, returns all sorted.
        """
        zip_code = request.query_params.get('zip')
        radius = request.query_params.get('radius')  # optional

        if not zip_code or len(zip_code) != 5:
            return Response({"message": "Provide a valid 5-digit zip."},
                            status=status.HTTP_400_BAD_REQUEST)

        nomi = pgeocode.Nominatim('us')
        loc = nomi.query_postal_code(zip_code)
        if loc is None or loc.latitude is None or loc.longitude is None:
            return Response({"message": "ZIP not found."}, status=status.HTTP_404_NOT_FOUND)

        lat, lon = float(loc.latitude), float(loc.longitude)
        try:
            radius = float(radius) if radius is not None else None
        except ValueError:
            return Response({"message": "radius must be a number (miles)."},
                            status=status.HTTP_400_BAD_REQUEST)

        rows = []
        for s in Store.objects.all():
            if s.latitude is None or s.longitude is None:
                continue
            dist = haversine_distance(lat, lon, float(s.latitude), float(s.longitude))
            if radius is None or dist <= radius:
                rows.append({
                    **self.get_serializer(s).data,
                    "distance_mi": round(dist, 2)
                })

        rows.sort(key=lambda x: x["distance_mi"])
        return Response({
            "count": len(rows),
            "zip": zip_code,
            "radius": radius,
            "stores": rows,
            "closest": rows[0] if rows else None
        }, status=status.HTTP_200_OK)


    def list(self, request, *args, **kwargs):
        """Show all stores with hours and open/closed status."""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def retrieve(self, request, *args, **kwargs):
        """Show single store detail with hours and status."""
        store = self.get_object()
        serializer = self.get_serializer(store)
        return Response(serializer.data, status = status.HTTP_200_OK)

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class GroceryItemViewSet(viewsets.ModelViewSet):
    queryset = GroceryItem.objects.all()
    serializer_class = GroceryItemSerializers

    def get_queryset(self):
        """
        Handle sorting for the list endpoint (/api/grocery-items/).
        Supports ?sort=brand for ascending or ?sort=-brand for descending.
        """
        queryset = super().get_queryset()
        sort = self.request.query_params.get('sort', None)
        if sort == 'brand':
            queryset = queryset.order_by('brand')
        elif sort == '-brand':
            queryset = queryset.order_by('-brand')
        elif sort == 'price':
            queryset = queryset.order_by('price')
        elif sort == '-price':
            queryset = queryset.order_by('-price')
        return queryset

    @action(detail=False, methods=['get'])
    def search(self, request):
        """
        Search grocery items by name or brand with optional sorting.
        Example: /api/grocery-items/search/?q=milk&sort=brand
        """
        query = request.query_params.get('q', '')
        sort = request.query_params.get('sort', None)
        
        if query:
            items = GroceryItem.objects.filter(
                Q(name__icontains=query) | Q(brand__icontains=query)
            )
        else:
            items = GroceryItem.objects.all()
        
        # Apply sorting if specified
        if sort == 'brand':
            items = items.order_by('brand')
        elif sort == '-brand':
            items = items.order_by('-brand')
        elif sort == 'price':
            items = items.order_by('price')
        elif sort == '-price':
            items = items.order_by('-price')
        
        serializer = self.get_serializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail = False, methods = ['get'], url_path = 'by-store/(?P<store_id>[^/.]+)')
    def by_store(self, request, store_id = None):
        """
        Display grocery items filtered by selected store.
        Example: /api/grocery-items/by-store/1/
        """
        try:
            store = Store.objects.get(pk = store_id)
        except Store.DoesNotExist:
            return Response(
                {"Message": "Selected store does not exist."},
                status = status.HTTP_404_NOT_FOUND
            )
        items = GroceryItem.objects.filter(store_id = store)

        if not items.exists():
            return Response(
                {
                    "Message": f"Price data for {store.name} is not available.", 
                    "store_selected": store.name,
                    "data": "Previous store data remains visible."
                },
                status = status.HTTP_200_OK
            )
        
        serializer = self.get_serializer(items, many = True)
        return Response(
            {
                "Message": f"Now viewing prices from {store.name}.",
                "store_selected": store.name,
                "data": serializer.data
            },
            status = status.HTTP_200_OK
        )

 
class SortListView(APIView):
    queryset = Store.objects.all()

    """
        When a user clicks the calculate button, their current list will be evaulated and the name of each grocery
        item on the list will be stored in an array. This array will be sent in the request body of a post request
        from the frontend React app and received by the backend at the SortListView Django view. This view accepts
        the array of grocey item names as a grocery list, and will calulcate the total of that grocery list at each 
        relevant store. After calculating the total of the grocery list at each store, the total price of each store 
        will be evaulated to sort the stores by total price in ascending order. After sorting, an array containing
        each store's information will be returned to the frontend.
    """
    def post(self, request):
        serializer = GroceryListSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Extract the array of item names from the serilaizer and store in items array
        items = serializer.validated_data['items']

        """ 
            This array, store_totals, will hold objects representing each store. Each object will consist of the store name, 
            address and store total. After each store total has been determined, this array will be sorted by store total in
            ascending order by store total, leaving the cheapest store at the top of the array.

        """
        store_totals = []

        """
            Store.objects.all() gets all stores currently in the database. An enhanced for loop is used to perform the below
            operations on each of the stores in the database.
        """
        for store in Store.objects.all():
            total = 0 # Each store's total price for the grocery list
            missing_items = False # Set to false. If any grocery item cannot be found for this store, set to true
            item_breakdown = []

            """
                A enhanced for loop is used to perform a query for each grocery item on the grocery list. For each item in
                items, get the item from the database. Using this item's id field and the current store's id field, get the grocery
                item associated with this store and item. After retrieving the grocery item which contains the grocery item price,
                add the price to total to keep track of the store total. This will be repeated for every item on the grocery list.
                After all items have been found and added to the total, an object will be created containg the store's name, address
                and total for the gorcery list. This object will then be added to the store_totals array.
            """
            for item_name in items:
                try:
                    # Get item from database.
                    item = Item.objects.get(name=item_name)

                    # Used the item's id field and current store's id field to get the associated grocery item from database.
                    grocery_item = GroceryItem.objects.get(store_id=store.id, item_id=item.id)

                    # Add grocery item price to total.
                    total += grocery_item.price
                    
                     # Build availability display
                    availability = grocery_item.availability
                    if availability is None:
                        availability_display = "Not available"
                    elif availability == 0:
                        availability_display = "Out of Stock"
                    else:
                        availability_display = f"In Stock ({availability})"

                    # Add row to breakdown list
                    item_breakdown.append({
                        "item_name": item.name,
                        "price": float(grocery_item.price),
                        "availability": availability,
                        "availability_display": availability_display,
                    })




                # If no associated item exists, then set missing_items to true and break for loop.
                except(GroceryItem.DoesNotExist):
                    missing_items = True
                    break
            
            # If missing_items is still false, that means all items have been found and this store is an option for the user to get their grocery list.
            if not missing_items:

                # If all items have been found, create an object represnting this store and append it to the store_totals array.
                store_totals.append({
                    "store_id": store.id,
                    'store': store.name,
                    'address': store.address,
                    "total_price": float(total),
                    "items": item_breakdown,
                })
        # After determing the totals for all relevent store, Use a lambda function to sort the store objects by total_price.
        sorted_totals = sorted(store_totals, key=lambda x: x['total_price'])
        
        # Return the sorted array to the frontend.
        return Response(sorted_totals)
    
