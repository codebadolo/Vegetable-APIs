from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
   path('admin/', admin.site.urls),
   #path('grappelli/', include('grappelli.urls')),  # Grappelli URLS
   path('api/', include('vendors.urls')),  # This links the vendor app URLs under the 'api/' path
   path('orders/', include('orders.urls')), 
    # Add other app URLs here, e.g.:

    # path('api/', include('product.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
