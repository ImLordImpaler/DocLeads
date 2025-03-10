from rest_framework.viewsets import ViewSet
from rest_framework.response import Response 
from .handler import DoctorHandler, PatientHandler, AppointmentHandler, AvailbilityHandler, MiscHandler
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from .permissions import IsDoctorOrSelf, IsPatientOrSelf, IsSameDocOrNot

class DoctorViewSet(ViewSet):
    
    def get_doctors(self, request):
        doc_obj = DoctorHandler(request)
        response = doc_obj.get_doctors()
        return Response(data=response, status=200)
        
    def create_doctor(self , request):
        doc_obj = DoctorHandler(request)
        response = doc_obj.create_doctor()
        return Response(data=response, status=201)

    def update_doctor(self, request, pk):
        doc_obj = DoctorHandler(request)
        response = doc_obj.update_doctor(pk)
        return Response(data=response , status=202)
    
    def view_doctor(self , request, pk):
        doc_obj = DoctorHandler(request)
        response = doc_obj.get_doctor(pk)
        return Response(data=response , status=200) 

    def delete_doctor(self, request,pk):
        pass 
    
    def get_doc_availability(self, request, pk):
        doc_objs = AvailbilityHandler(request)
        response = doc_objs.get_doc_availability(pk)
        return Response(data=response, status=200)

class AppointmentSet(ViewSet):
    # permission_classes = [IsPatientOrSelf]
    def make_appointment(self , request):
        appointment_obj = AppointmentHandler(request)
        response = appointment_obj.book_appointment()
        return Response(data=response , status=201)
    
    def get_booking_slots(self , request):
        appointment_obj = AppointmentHandler(request)
        response = appointment_obj.get_booking_slots()
        return Response(data = response , status = 200)
    
class PaitentViewSet(ViewSet):

    def get_paitents(self, request):
        paitent_obj = PatientHandler(request)
        response = paitent_obj.get_patients()
        return Response(data=response, status=200) 

    def view_paitent(self,request,pk):
        paitent_obj = PatientHandler(request) 
        response = paitent_obj.view_patient(pk)
        return Response(data=response, status = 200)

    def create_paitent(self, request):
        patient_obj = PatientHandler(request)
        response,status = patient_obj.create_patient()
        return Response(data=response, status=status)

    def update_paitent(self, pk):
        pass 


class MiscViewSet(ViewSet):
    def get_speciality(self , request):
        misc_obj = MiscHandler(request)
        status,response = misc_obj.get_specialities()
        return Response(data=response , status=status)
    
    def create_speciality(self, request):
        misc_obj = MiscHandler(request)
        status,response = misc_obj.create_speciality()
        return Response(data=response , status=status)
        

