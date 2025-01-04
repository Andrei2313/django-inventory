from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponseRedirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('inventory/', include('inventory.urls')),  # Include the inventory app URLs
    path('', lambda request: HttpResponseRedirect('/inventory/')),  # Redirect root to inventory
    path('accounts/', include('django.contrib.auth.urls')),  # Authentication URLs
]
