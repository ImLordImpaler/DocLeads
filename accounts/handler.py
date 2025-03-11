import random
import hashlib
from .models import UserOTP, User
from basic.models import Doctor, Patient, Speciality
from django.contrib.auth import login, authenticate
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from django.db import transaction
from datetime import datetime
class AuthHandler:
    def __init__(self, request):
        self.request = request
        self.post_data = request.data
        self.get_data = request.query_params.dict()

    def login(self):
        phone = self.post_data['phone']

        if self.post_data['type'] == "doctor":
            password = self.post_data['password']
            user = authenticate(self.request, phone=phone, password=password)
            if user is None:
                raise AuthenticationFailed('Invalid credentials.')
            

        elif self.post_data['type'] == 'paitent':
            '''
            Paitent Login: 
                -> This is from OTP success
                -> check if phone is registed : return user, token 
                   else:
                        -> New User. Please Register First
                    
            '''
            try:
                user = User.objects.get(phone=phone)
            except User.DoesNotExist as E:
                return 200, {'error':"User Not registed. Please Register First"}
            
            if not user.is_paitent:
                raise AuthenticationFailed("User registerd as Doctor. Cannot login as Paitent")
        else:
            raise Exception("Wrong Type selected: choices are [doctor, paitent]")
            
        token, created = Token.objects.get_or_create(user=user)

        response = {
            'user_id': user.id, 
            'username':user.name,
            'phone':user.phone, 
            'email':user.email, 
            'key': "Bearer {}".format(token.key)
        }
        return 200, response


    def logout(self):
        
        token = self.request.headers.get('Authorization', None).split(' ')[-1]
        token = Token.objects.get(key=token)
        token.delete() 
        return 201, {"response":"Logged Out Success"}
    
    def register(self):
        phone = self.post_data['phone']
        name = self.post_data['name']
        type = self.post_data['type']
        with transaction.atomic():
            if type == 'doctor':
                
                    password = self.post_data['password']
                    password1 = self.post_data['password1']
                    speciality_id = self.post_data['speciality_id']
                    if password != password1: raise Exception("Passwords don't match")
                    
                    kwargs = self.fill_user_data()

                    user = User.objects.create_user(
                        phone=phone, 
                        name=name,
                        password = password,
                        # password1 = password1,
                        is_doctor=True,
                        **kwargs
                    )
                    speciality = Speciality.objects.get(id = speciality_id)
                    doc_data = self.fill_doctor_data()
                    Doctor.objects.create(
                        user=user, 
                        name=name, 
                        speciality = speciality,
                        **doc_data
                    )

            elif type == 'paitent':
                '''
                Create a user 
                '''
                password = self.generate_hash_for_password()
                user = User.objects.create_user(
                    phone = phone, 
                    name=name, 
                    password = password,
                    is_paitent = True
                )

                Patient.objects.create(
                    user=user, 
                    name=name,
                    **self.fill_user_data()
                )

            token, created = Token.objects.get_or_create(user=user)
            
            response = {
                'user_id': user.id, 
                'username':user.name,
                'phone':user.phone, 
                'email':user.email, 
                'key': "Bearer {}".format(token.key)
            }
        
        return 200, response

    def fill_doctor_data(self, **kwargs):
        for key in self.post_data:
            if key == 'dob':
                kwargs['dob'] = self.post_data[key]
            elif key == 'years_of_experience':
                kwargs['years_of_experience'] = self.post_data[key]
            
            elif key == 'consultation_fee':
                kwargs['consultation_fee'] = self.post_data[key]

        return kwargs
    
    def fill_user_data(self, **kwargs):
        for key in self.post_data: 
            if key == 'email':
                kwargs['email'] = self.post_data[key] 
        return kwargs

    def generate_hash_for_password(self):
        now = datetime.now().isoformat()
        return hashlib.sha256(now.encode()).hexdigest()

    def send_otp(self):
        '''
        params: 
            Phone
        return 
            Otp 
        '''
        phone = self.post_data['phone']
        try:
            obj = UserOTP.objects.get(phone=phone)
        except UserOTP.DoesNotExist:
            random_num = random.randint(100000, 999999)
            obj = UserOTP.objects.create(phone=phone, otp=random_num)
        
        return 200, {'otp': obj.otp, 'phone':str(obj.phone)}
    
    def check_otp(self):
        '''
        params: 
            Phone
            Otp 
        return 
            Bool (True, False)
        '''
        phone = self.get_data['phone']
        otp = self.get_data['otp']
        try:
            obj = UserOTP.objects.get(phone=phone, otp=otp)
        except UserOTP.DoesNotExist:
            return 400, {'error':"Wrong OTP entered"}
        
        # # If OTP is success, Call login api after this:

        return 200, {'message':"OTP Succesfull"}
    

    def create_or_return_user(self):
        '''
        User Logs in using OTP method:
        if user exists:
            return user, token 
        else:
            create Paitent 
            return 
        '''
        pass 

    def register_paitent(self):
        return 200, "Working"