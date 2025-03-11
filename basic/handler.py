import random
from django.db.models.query import QuerySet
from basic.models import Doctor, Patient, DoctorAvailability, Appointment, Speciality
from datetime import datetime, timedelta
from django.conf import settings
from .utils import parse_response, create_user_for_instance

class DoctorHandler:
    def __init__(self , request):
        self.request = request 
        self.post_data = request.data 
        self.get_data = request.query_params.dict() 

        self.return_fields = [
            'id', 'name', 'dob', 'years_of_experience', 'speciality__name', 'doc_image', 'consulation_fee', 'user__phone','user__email'
        ]

    def get_doctor(self, pk):
        doctor = Doctor.objects.get(id =pk)
        return self.parse_doctor_response(doctor)

    def get_doctors(self):
        kwargs = self.filter_doctors()
        doctors = Doctor.objects.filter(**kwargs)\
            .values(*self.return_fields)
        
        return self.parse_doctor_response(doctors)

    def create_doctor(self, **kwargs):
        try:
            return "Use Registration API instead for Create Doctor"

            kwargs,password = self.get_doctor_creation_details()
            doctor = Doctor.objects.create(**kwargs)

            create_user_for_instance(doctor, 
                                     type='doctor',
                                     password=password)
            
            return self.parse_doctor_response(doctor)
        except KeyError as E:
            raise Exception(str(E)) 

    def get_doctor_creation_details(self, **kwargs):
        try:
            kwargs['name'] = self.post_data['name']
            try:
                kwargs['speciality'] = Speciality.objects.get(name=self.post_data['speciality'])
            except Speciality.DoesNotExist as E:
                raise Exception("No Speciality found")
            
            # kwargs['phone'] = self.post_data['phone']

            password = self.post_data['password']
            password1 = self.post_data['password1']

            if password != password1:
                raise Exception("Passwords don't match")
            
            return kwargs,password
        except Exception as E:
            raise Exception(str(E))

    def update_doctor(self, pk):
        try:
            doc = Doctor.objects.filter(id = pk)
            if not doc:
                raise Exception("Doctor Object Doesn't Exist: {}".format(pk))
            doc.update(**self.post_data)

            return self.parse_doctor_response(doc[0]) 
        except Exception as E:
            raise Exception(str(E))

    def delete_doctor(self):
        pass 

    def parse_doctor_response(self, doctor_obj):
        if isinstance(doctor_obj, QuerySet): # Will get list incase of mutiple object responses
            response_list = []
            print(doctor_obj)
            for doctor in doctor_obj:
                response_obj = {}
                for field in self.return_fields:
                    response_obj[field] = doctor.get(field)

                # Append all availbility here:
                response_obj = self.add_availibilty_times(doctor, response_obj)
                response_list.append(response_obj)
            return response_list 
        else:
            response = {}
            for field in self.return_fields:
                
                if field in ['speciality__name']:
                    response[field] = doctor_obj.speciality.name
                    continue
                response[field] = getattr(doctor_obj, field, None)
            # Append Availability here: 
            response = self.add_availibilty_times(doctor_obj, response)
            return response
    
    def add_availibilty_times(self, doctor_obj , response_obj):
        try:
            if isinstance(doctor_obj, dict):
                doctor_id = doctor_obj.get('id')
            else:
                doctor_id = doctor_obj.id

            # Fetch all availibility for the doctor and append it to the response_obj
            availabilities = DoctorAvailability.objects.filter(doctor_id=doctor_id)\
                                .values('day_of_week', 'start_time', 'end_time')
            response_obj['availability'] = []
            for timing in availabilities:
                response_obj['availability'].append({
                    'day_of_week': timing['day_of_week'],
                    'start_time': timing['start_time'], 
                    'end_time':timing['end_time']
                })
            return response_obj
        except Exception:
            import traceback
            traceback.print_exc()


    def filter_doctors(self, **kwargs):
        # Write conditions here to filter doctors
        for i in self.get_data:
            kwargs[i] = self.get_data[i]
        return kwargs
    
class PatientHandler:
    def __init__(self, request):
        self.request = request
        self.post_data = request.data
        self.get_data = request.query_params.dict() 
        self.return_fields = ['name','age','user__phone','user__email']

    def create_patient(self):
        try:
            return "Use Registration API instead for Create Doctor", 200
            kwargs,password = self.fill_patient_data()
            obj = Patient.objects.create(**kwargs)

            create_user_for_instance(obj, type='paitent', password=password)
            return self.parse_doctor_response(obj), 201
        except Exception as E:
            return str(E), 400
        
    def fill_patient_data(self, **kwargs):
        try:
            kwargs['name'] = self.post_data['name']
            kwargs['phone'] = self.post_data['phone']
            kwargs['email'] = self.post_data['email']

            password = self.post_data['password']
            password1 = self.post_data['password1']

            if password !=password1:
                raise Exception("Passwords don't match")
            return kwargs,password
        except KeyError as E:
            raise Exception("Field missing: {}".format(str(E)))

    def get_patients(self):
        kwargs = self.filter_doctors()
        doctors = Patient.objects.filter(**kwargs)\
            .values(*self.return_fields)
        return self.parse_doctor_response(doctors)
    
    def view_patient(self, pk):
        patient_obj = Patient.objects.get(id = pk)
        return parse_response(patient_obj, self.return_fields)
    
    def filter_doctors(self):
        return {}
    
    def parse_doctor_response(self, patient):
        if isinstance(patient, QuerySet): # Will get list incase of mutiple object responses
            response_list = []
            for doctor in patient:
                response_obj = {}
                for field in self.return_fields:
                    response_obj[field] = doctor.get(field)

                response_list.append(response_obj)
            return response_list 
        else:
            response = {}
            for field in self.return_fields:
                response[field] = getattr(patient, field, None)
            return response

class AvailbilityHandler:
    def __init__(self, request):
        self.request = request
        self.post_data = request.data 
        self.get_data = request.query_params.dict() 
        self.return_fields = ['doctor', 'day_of_week', 'start_time','end_time']

    def get_doc_availability(self, pk):
        availbility_obj = DoctorAvailability.objects.filter(doctor_id = pk).values(*self.return_fields)
        return availbility_obj

class AppointmentHandler:
    def __init__(self, request):
        self.request = request
        self.post_data = request.data 
        self.get_data = request.query_params.dict() 
        self.doctor = None
        self.patient = None
        self.return_fields = ['patient', 'doctor', 'appointment_time', 'patient__name','doctor__name']
        
    def get_booking_slots(self, **kwargs):
        doctor = Doctor.objects.get(id = self.get_data['doctor_id'])
        
        if self.get_data.get('start_time'):
            kwargs['start_time'] = self.get_data['start_time']

        if self.get_data.get('end_time'):
            kwargs['end_time'] = self.get_data['end_time']
        else:
            kwargs['end_time'] = datetime.strftime(datetime.strptime(self.get_data['start_time'], "%Y-%m-%d %H:%M:%S"), "%Y-%m-%d 23:59:59")

        slots = self.get_available_slots_for_doctor(doctor, **kwargs)
        return slots
    
    def get_doc_availability(self, doc):
        return DoctorAvailability.objects.filter(doctor=doc).values(*self.return_fields)
        
    def get_available_slots_for_doctor(self,doctor, slot_duration=30, **kwargs): 
        '''
        Params: 
            start_datetime, 
            end_datetime 
            doctor_id 
        Flow: 
            Start from start_datetime. 
                
            till end_datetime 
        '''
        start_date = datetime.strptime(kwargs['start_time'], "%Y-%m-%d %H:%M:%S")
        end_date = datetime.strptime(kwargs['end_time'], '%Y-%m-%d %H:%M:%S')
        from django.db.models import Q
        availabilities = DoctorAvailability.objects.filter(doctor=doctor)
        # import pdb
        # pdb.set_trace()
        all_slots = []
        current_date = start_date
        while current_date <= end_date:
            current_time = current_date.strftime("%H:%M")

            daily_availabilities = availabilities.filter(
                                        Q(day_of_week=current_date.strftime('%A')) & 
                                        (
                                            # If the current time is between start_time and end_time
                                            Q(start_time__lte=current_time, end_time__gte=current_time) |
                                            
                                            # If the current time is before the start_time, and we want to include the future slots
                                            Q(start_time__gte=current_time)
                                        )
                                    )
            
            if not daily_availabilities:
                current_date = current_date + timedelta(days=1)
                current_date = current_date.replace(hour=0, minute=0, second=0, microsecond=0)
                continue

            for i in daily_availabilities:
                
                x = current_date #Maybe Refactor this code. Later...
                y = current_date.replace(hour=int(str(i.start_time)[:2]), minute= int(str(i.start_time)[3:5]))
                if x > y:
                    slot_start = x 
                else:
                    slot_start = y
                slot_end = current_date.replace(hour=int(str(i.end_time)[:2]), minute=int(str(i.end_time)[3:5]))

                while (slot_start < slot_end):
                    end_time = slot_end if slot_start + timedelta(minutes=slot_duration) > slot_end else slot_start + timedelta(minutes=slot_duration)
                    
                    if not self.check_slot_availability(

                    ): # Do this after Appointment
                        continue
                    
                    all_slots.append({
                            "start_time": datetime.strftime(slot_start, "%H:%M:%S"),
                            "end_time": datetime.strftime(end_time, "%H:%M:%S"),
                            "date": datetime.strftime(slot_start, "%d/%m/%Y"),
                            "doctor":doctor.id,
                            "unique_slug": ''.join(char for char in str(slot_start) +" "+ str(doctor.id) if char.isdigit())
                    })
                    slot_start += timedelta(minutes=slot_duration)
            current_date += timedelta(days=1)
            current_date.replace(hour=0, minute=0 , second=0)
            
        return all_slots

    def book_appointment(self):
        patient_phone = self.post_data['patient_phone']
        doctor_id = self.post_data['doctor_id']

        appointment_start_time = self.post_data['appointment_start_time']
        appointment_end_time = self.post_data['appointment_end_time']

        patient = self.get_patient(patient_phone)

        app = Appointment.objects.create(
            patient = patient, 
            doctor_id = doctor_id,
            appointment_start_time = datetime.strptime(appointment_start_time, "%d/%m/%Y %H:%M:%S"),
            appointment_end_time=datetime.strptime(appointment_end_time, "%d/%m/%Y %H:%M:%S")
        )
        return {
            'data':'Appointment Made {}'.format(app.id)
        }
    
    def get_patient(self, phone):
        patient = Patient.objects.get(phone = phone)
        self.patient = patient
        return patient
    
    def check_slot_availability(self):
        '''
        Depends on: 
            doctor.

        1) No existing Appointments should be there. 
        2) Doctor should be available. 
        '''
        return True 
    

class MiscHandler:
    def __init__(self, request):
        self.request = request 
        self.get_data = request.query_params.dict() 
        self.post_data = request.data
        self.return_fields = ['id','name']

    def get_specialities(self):
        return 200 , Speciality.objects.filter(**self.get_data).values(*self.return_fields)
    
    def create_speciality(self):
        return 201, parse_response(Speciality.objects.create(**self.post_data), self.return_fields)
    

