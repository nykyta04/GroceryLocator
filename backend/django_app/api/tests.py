from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from .models import Store, GroceryItem, Item
from datetime import time
from unittest.mock import patch
from types import SimpleNamespace
from .models import Store, Item, GroceryItem

class StoreCRUDTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.store_data = {"name": "Test Store", "zip": 12345, "address": "1234 First St.", "latitude": 11.46966, "longitude": -146.63588, "hour_open": "06:00:00", "hour_close": "10:00:00"}
        self.store = Store.objects.create(**self.store_data)
        self.store_url = reverse('store-list')

    def test_create_store(self):
        new_store_data = {"name": "New Store", "zip": 11111, "address": "123 Second St.", "latitude": 21.33050, "longitude": 135.06505, "hour_open": "05:00:00", "hour_close": "11:00:00"}
        response = self.client.post(self.store_url, new_store_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Store.objects.count(), 2)

    def test_read_store_list(self):
        response = self.client.get(self.store_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Test Store", str(response.data))

    def test_update_store(self):
        update_url = reverse('store-detail', kwargs={'pk': self.store.pk})
        updated_data = self.store_data.copy()
        updated_data["name"] = "Updated Store"
        response = self.client.put(update_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.store.refresh_from_db()
        self.assertEqual(self.store.name, "Updated Store")

    def test_delete_store(self):
        delete_url = reverse('store-detail', kwargs={'pk': self.store.pk})
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Store.objects.count(), 0)


class ItemCRUDTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.item_data = {"name": "Test Item"}
        self.item = Item.objects.create(**self.item_data)
        self.item_url = reverse('item-list')

    def test_create_item(self):
        new_item_data = {"name": "New Item"}
        response = self.client.post(self.item_url, new_item_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Item.objects.count(), 2)

    def test_read_item_list(self):
        response = self.client.get(self.item_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Test Item", str(response.data))

    def test_update_item(self):
        update_url = reverse('item-detail', kwargs={'pk': self.item.pk})
        updated_data = self.item_data.copy()
        updated_data["name"] = "Updated Item"
        response = self.client.put(update_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.item.refresh_from_db()
        self.assertEqual(self.item.name, "Updated Item")

    def test_delete_item(self):
        delete_url = reverse('item-detail', kwargs={'pk': self.item.pk})
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Item.objects.count(), 0)

class GroceryItemCRUDTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.store = Store.objects.create(name ="Store 1", zip = 12345, address = "123 First St.", latitude = 11.46966, longitude = -146.63588, hour_open = "06:00:00", hour_close = "10:00:00")
        self.pear = Item.objects.create(name="Pear")
        self.peach = Item.objects.create(name="Peach")
        self.grocery_item_data = {"store_id": self.store, "item_id": self.pear, "price": 2.0, "name": "Pear", "availability": 15, "brand": "Test Brand"}
        self.grocery_item = GroceryItem.objects.create(**self.grocery_item_data)
        self.grocery_item_url = reverse('groceryitem-list')

    def test_create_grocery_item(self):
        new_grocery_item_data = {"store_id": self.store.id, "item_id": self.peach.id, "price": 1.0, "name": "Peach", "availability": 15, "brand": "Test Brand"}
        response = self.client.post(self.grocery_item_url, new_grocery_item_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(GroceryItem.objects.count(), 2)
    
    def test_read_grocery_item_list(self):
        response = self.client.get(self.grocery_item_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Pear", str(response.data))

    def test_update_grocery_item(self):
        update_url = reverse('groceryitem-detail', kwargs={'pk': self.grocery_item.pk})
        updated_data = self.grocery_item_data.copy()
        updated_data['name'] = "Updated Grocery Item"
        updated_data['store_id'] = self.store.id
        updated_data['item_id'] = self.pear.id
        response = self.client.put(update_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.grocery_item.refresh_from_db()
        self.assertEqual(self.grocery_item.name, "Updated Grocery Item")

    def test_delete_grocery_item(self):
        delete_url = reverse('groceryitem-detail', kwargs={'pk': self.grocery_item.pk})
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(GroceryItem.objects.count(), 0)


class SortListViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create test items
        self.pear = Item.objects.create(name="Pear")
        self.peach = Item.objects.create(name="Peach")
        # Create test stores
        self.store_1 = Store.objects.create(name ="Store 1", zip = 12345, address = "123 First St.", latitude = 11.46966, longitude = -146.63588, hour_open = "06:00:00", hour_close = "10:00:00")
        self.store_2 = Store.objects.create(name = "Store 2", zip =  11111, address = "123 Second St.", latitude = 21.33050, longitude = 135.06505, hour_open = "05:00:00", hour_close = "11:00:00")
        # Create test grocery item data
        grocery_item_data_1 = {"store_id": self.store_1, "item_id": self.pear, "price": 2.0, "name": "Pear", "availability": 15, "brand": "Test Brand"}
        grocery_item_data_2 = {"store_id": self.store_1, "item_id": self.peach, "price": 1.0, "name": "Peach", "availability": 15, "brand": "Test Brand"}
        grocery_item_data_3 = {"store_id": self.store_2, "item_id": self.pear, "price": 3.0, "name": "Pear", "availability": 15, "brand": "Test Brand"}
        grocery_item_data_4 = {"store_id": self.store_2, "item_id": self.peach, "price": 2.0, "name": "Peach", "availability": 15, "brand": "Test Brand"}
        # Create test GroceryItems
        GroceryItem.objects.create(**grocery_item_data_1)
        GroceryItem.objects.create(**grocery_item_data_2)
        GroceryItem.objects.create(**grocery_item_data_3)
        GroceryItem.objects.create(**grocery_item_data_4)

    def test_sort_list_view(self):
        url = reverse('sort-lists')
        data = {"items": ["Pear", "Peach"]}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        self.assertEqual(response.data[0]['store'], "Store 1")
        self.assertEqual(response.data[1]['store'], "Store 2")


class StoreSelectionTests(APITestCase):
    def setUp(self):
        self.store_a = Store.objects.create(name ="Store 1", zip = 12345, address = "123 First St.", latitude = 11.46966, longitude = -146.63588, hour_open = "06:00:00", hour_close = "10:00:00")
        self.store_b = Store.objects.create(name = "Store 2", zip =  11111, address = "123 Second St.", latitude = 21.33050, longitude = 135.06505, hour_open = "05:00:00", hour_close = "11:00:00")
        self.store_empty = Store.objects.create(name = "Store 3", zip =  22222, address = "456 Second St.", latitude = 27.33050, longitude = 125.06505, hour_open = "05:00:00", hour_close = "11:00:00")  # no items

        self.milk = Item.objects.create(name="Milk")

        GroceryItem.objects.create(
            store_id=self.store_a, name="Milk", brand="Horizon", price=3.50, availability=10, item_id = self.milk
        )
        GroceryItem.objects.create(
            store_id=self.store_b, name="Milk", brand="Great Value", price=3.50, availability=20, item_id = self.milk
        )

    def test_switch_store_shows_correct_data(self):
        url = f"/api/grocery-items/by-store/{self.store_b.id}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Now viewing prices from", response.data["Message"])
        self.assertEqual(response.data["store_selected"], self.store_b.name)
        self.assertGreater(len(response.data["data"]), 0)

    def test_show_confirmation_on_store_change(self):
        url = f"/api/grocery-items/by-store/{self.store_a.id}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["store_selected"], "Store 1")
        self.assertIn("Now viewing prices from", response.data["Message"])

        url = f"/api/grocery-items/by-store/{self.store_empty.id}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Price data for", response.data["Message"])
        self.assertIn("Previous store data remains visible", str(response.data))

    def test_invalid_store(self):
        url = "/api/grocery-items/by-store/999/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("does not exist", response.data["Message"])

    def test_default_store_view(self):
        url = "/api/grocery-items/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

class StoreHoursTests(APITestCase):
    def setUp(self):
        self.store = Store.objects.create(
            name = "Test store",
            zip=12345,
            address = "123 Main St",
            hour_open = time(6, 0),
            hour_close = time(22, 0)
        )
    
    def test_store_hours_displayed(self):
        url = "/api/stores/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        first = response.data[0]
        self.assertIn("hour_open", first)
        self.assertIn("hour_close", first)

    def test_missing_hours(self):
        Store.objects.create(
            name="No Hours Store",
            zip=99999,
            address="N/A",
            hour_open=time(0, 0),
            hour_close=time(0, 0),
        )
        url = "/api/stores/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 2)

# ------ DISTANCE/ZIP TESTS------

# Fake zip record that mimics pgeocode's return (has .latitude and .longitude)
def _fake_zip_record():
    return SimpleNamespace(latitude=35.0000, longitude=-80.0000)  

# Tests for distance-based store endpoints
class StoreDistanceAPITests(APITestCase):
    def setUp(self):
        # Stores with known distances from the fake ZIP
        self.alpha = Store.objects.create(
            name="Alpha Market",
            zip=99999, address="Alpha Rd",
            latitude=35.0000, longitude=-80.0000,
            hour_open="06:00:00", hour_close="23:00:00",
        )
        self.bravo = Store.objects.create(
            name="Bravo Foods",
            zip=99998, address="Bravo Blvd",
            latitude=35.0300, longitude=-80.0000,  # ~2.07 miles 
            hour_open="06:00:00", hour_close="23:00:00",
        )
        self.charlie = Store.objects.create(
            name="Charlie Grocer",
            zip=99997, address="Charlie Ln",
            latitude=35.0500, longitude=-80.0000,  # ~3.45 miles 
            hour_open="06:00:00", hour_close="23:00:00",
        )

# Return the single clostest store to ZIP
    @patch("api.views.pgeocode.Nominatim.query_postal_code", return_value=_fake_zip_record())
    def test_nearest_returns_single_closest_with_distance(self, _mock):
        res = self.client.get(reverse("store-nearest") + "?zip=12345")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["closest"]["name"], "Alpha Market")
        self.assertIn("distance_mi", res.data["closest"])

# Return all stores sorted by distance for a given ZIP
    @patch("api.views.pgeocode.Nominatim.query_postal_code", return_value=_fake_zip_record())
    def test_nearby_sorted_and_radius_filter(self, _mock):
        # All (sorted by distance)
        res = self.client.get(reverse("store-nearby") + "?zip=12345")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        names = [s["name"] for s in res.data["stores"]]
        self.assertEqual(names, ["Alpha Market", "Bravo Foods", "Charlie Grocer"])

        # Radius=2.0 mi: only Aplhas should remain
        res2 = self.client.get(reverse("store-nearby") + "?zip=12345&radius=2.0")
        self.assertEqual(res2.status_code, status.HTTP_200_OK)
        self.assertEqual(res2.data["count"], 1)
        self.assertEqual(res2.data["stores"][0]["name"], "Alpha Market")

# Error handling and validation tests
    def test_nearby_requires_valid_zip_length(self):
        res = self.client.get(reverse("store-nearby") + "?zip=123")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("api.views.pgeocode.Nominatim.query_postal_code",
           return_value=SimpleNamespace(latitude=None, longitude=None))
    def test_zip_not_found(self, _mock):
        res = self.client.get(reverse("store-nearest") + "?zip=99999")
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    @patch("api.views.pgeocode.Nominatim.query_postal_code", return_value=_fake_zip_record())
    def test_radius_must_be_numeric(self, _mock):
        res = self.client.get(reverse("store-nearby") + "?zip=12345&radius=abc")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("api.views.pgeocode.Nominatim.query_postal_code", return_value=_fake_zip_record())
    def test_nearby_handles_stores_without_coordinates(self, _mock):
        Store.objects.all().delete()
        Store.objects.create(
            name="NoCoords", zip=11111, address="X",
            latitude=None, longitude=None,
            hour_open="06:00:00", hour_close="23:00:00",
        )
        res = self.client.get(reverse("store-nearby") + "?zip=12345")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["count"], 0)
        self.assertIsNone(res.data["closest"])


# ------ SEARCH BY BRAND TESTS------

class SearchTests(APITestCase):
    def setUp(self):
        # Sample stores
        self.store_a = Store.objects.create(
            name="Walmart Supercenter", zip=28262, address="7735 N Tryon St",
            latitude=35.295361, longitude=-80.758278, hour_open="06:00:00", hour_close="23:00:00"
        )
        self.store_b = Store.objects.create(
            name="Food Lion", zip=28262, address="9323 N Tryon St",
            latitude=35.313821, longitude=-80.744602, hour_open="07:00:00", hour_close="23:00:00"
        )

        # Base items
        self.apple  = Item.objects.create(name="apple")
        self.banana = Item.objects.create(name="banana")

        # Grocery items with brands
        GroceryItem.objects.create(
            store_id=self.store_a, item_id=self.apple,  name="Apple",
            brand="Great Value", price=0.73, availability=49
        )
        GroceryItem.objects.create(
            store_id=self.store_a, item_id=self.banana, name="Banana",
            brand="Marketside", price=0.78, availability=55
        )
        GroceryItem.objects.create(
            store_id=self.store_b, item_id=self.apple,  name="Apple",
            brand="Nature's Promise", price=1.12, availability=15
        )

        self.url = "/api/grocery-items/search/"

    # Branch search tests
    def test_brand_search_returns_matches_case_insensitive_partial(self):
        """Searching by brand (partial + case-insensitive) returns the right rows."""
        res = self.client.get(self.url + "?q=great val")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        brands = [row.get("brand") for row in res.data]
        self.assertIn("Great Value", brands)
        self.assertNotIn("Nature's Promise", brands)

        # case-insensitive check
        res2 = self.client.get(self.url + "?q=GrEaT VaLuE")
        self.assertEqual(res2.status_code, status.HTTP_200_OK)
        brands2 = [row.get("brand") for row in res2.data]
        self.assertIn("Great Value", brands2)

    # Item name search tests
    def test_item_name_search_still_works(self):
        """Searching by item name still returns results (existing behavior preserved)."""
        res = self.client.get(self.url + "?q=apple")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        names = [row.get("name") for row in res.data]
        self.assertTrue(any(n and n.lower() == "apple" for n in names))

    # Serializer validation
    def test_search_includes_item_and_store_names_for_mapping(self):
        """Serializer exposes item_name and store_name so frontend can map brand hits -> base item."""
        res = self.client.get(self.url + "?q=value")  # hits "Great Value" Apple at Walmart
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(res.data), 1)

        row = res.data[0]
        # Verify core fields exist in response
        for key in ["id", "name", "brand", "price", "availability", "item_id", "store_id", "item_name", "store_name"]:
            self.assertIn(key, row, f"missing {key} in search row")
        # Check mapping
        self.assertEqual(row["item_name"], "apple")
        self.assertIn(row["store_name"], ["Walmart Supercenter", "Food Lion"])

    # Sorting
    def test_sorting_by_brand_ascending(self):
        """search supports ?sort=brand ascending."""
        res = self.client.get(self.url + "?q=a&sort=brand")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        brands = [r["brand"] for r in res.data if r.get("brand")]
        self.assertEqual(brands, sorted(brands, key=lambda s: s.lower()))

    #  Non matching query test
    def test_non_matching_query_returns_empty_list(self):
        """Unknown brand/item yields an empty list (no 500s)."""
        res = self.client.get(self.url + "?q=thisbranddoesnotexist")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, [])

    # No q param, returns all items (per your view)
    def test_empty_query_returns_all_items(self):
        res = self.client.get(self.url)  # no ?q=
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 3)
