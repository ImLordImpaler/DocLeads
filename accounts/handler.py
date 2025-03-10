import random
from .models import UserOTP, User
from django.contrib.auth import login, authenticate
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed

class AuthHandler:
    def __init__(self, request):
        self.request = request
        self.post_data = request.data

    def login(self):
        phone = self.post_data['phone']
        password = self.post_data['password']
        user = authenticate(self.request, phone=phone, password=password)
        if user is None:
            raise AuthenticationFailed('Invalid credentials.')
        token, created = Token.objects.get_or_create(user=user)

        return 200, {"token":"Bearer {}".format(token.key)}
    
    def logout(self):
        
        token = self.request.headers.get('Authorization', None).split(' ')[-1]
        token = Token.objects.get(key=token)
        token.delete() 
        return 201, {"response":"Logged Out Success"}
    
    def register(self):
        phone = self.post_data['phone']
        password = self.post_data['password']
        password1 = self.post_data['password1']

        REQUIRED_FIELDS = ['phone', 'password', 'password1']

        kwargs = self.fill_user_data(REQUIRED_FIELDS)

        user = User.objects.create_user(
            phone=phone, 
            password = password,
            # password1 = password1,
            **kwargs
        )
        token, created = Token.objects.get_or_create(user=user)
        return 200, {'token':"Bearer {}".format(token.key)}

    def fill_user_data(self, required_field, **kwargs):
        for i in self.post_data:
            if i not in required_field:
                kwargs[i] = self.post_data[i]
        return kwargs

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
        phone = self.post_data['phone']
        otp = self.post_data['otp']
        try:
            obj = UserOTP.objects.get(phone=phone, otp=otp)
        except UserOTP.DoesNotExist:
            return 400, {'error':"Wrong OTP entered"}
        
        return 200, {'message':"OTP Succesfull"}