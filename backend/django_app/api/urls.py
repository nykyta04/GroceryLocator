from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StoreViewSet, GroceryItemViewSet, SortListView, ItemViewSet
from api import views

router = DefaultRouter()
router.register(r'stores', StoreViewSet)
router.register(r'items', ItemViewSet)
router.register(r'grocery-items', GroceryItemViewSet)



urlpatterns = [
    path('api/', include(router.urls)),
    path('api/sort-lists/', SortListView.as_view(), name="sort-lists")
]