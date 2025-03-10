from django.contrib import admin
from basic.models import * 


admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Appointment)
admin.site.register(DoctorAvailability)
admin.site.register(Speciality)