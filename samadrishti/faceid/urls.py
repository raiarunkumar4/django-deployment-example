from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.routers import DefaultRouter
from faceid import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'customers', views.CustomerViewSet, basename='customer')
router.register(r'locations', views.LocationViewSet, basename='location')
router.register(r'devices', views.DeviceViewSet, basename='device')
router.register(r'persons', views.PersonViewSet, basename='person')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
