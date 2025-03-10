from django.urls import path 
from .views import * 


urlpatterns = [
    path('doctors', DoctorViewSet.as_view({'get':'get_doctors', 'post':'create_doctor'})),
    path('doctors/<int:pk>', DoctorViewSet.as_view({'get': 'view_doctor', 'put': 'update_doctor', 'delete': 'delete_doctor'})),  # For retrieving, updating, and deleting a specific doctor
    path('paitent', PaitentViewSet.as_view({'get':'get_paitents', 'post':'create_paitent'})),
    path('paitent/<int:pk>', PaitentViewSet.as_view({'get':'view_paitent', 'put':'update_paitent'})),
    path('speciality', MiscViewSet.as_view({'get':'get_speciality', 'post':'create_speciality'})),

    

    path("booking_slots", AppointmentSet.as_view({'get':'get_booking_slots'})),
    path('create_appointment', AppointmentSet.as_view({'post':'make_appointment'})),
]

