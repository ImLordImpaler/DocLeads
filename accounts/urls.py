from django.urls import path 
from .views import * 


urlpatterns = [

    path('login', AuthViewSet.as_view({'post':'login'})),
    path('logout', AuthViewSet.as_view({'post':'logout'})),

    path('register', AuthViewSet.as_view({'post':'register'})),
    path('send_otp', AuthViewSet.as_view({'post':'send_otp'})),
    path('check_otp', AuthViewSet.as_view({'post':'check_otp'}))
]
