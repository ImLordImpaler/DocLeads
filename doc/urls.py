from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('basic.urls')),
    path('accounts/', include('accounts.urls'))
    # path('', include('frontend.urls'))
]
