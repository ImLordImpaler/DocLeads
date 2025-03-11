from rest_framework.viewsets import ViewSet
from rest_framework.response import Response 
from .handler import AuthHandler

class AuthViewSet(ViewSet):
    '''
    First Implementation of Login and Register. To serve auth tokens on succesfull request. 
    Auth can be done with two type of users. 
        1) Doctors
        2) Paitent 
    Prefer to use like an OTP service. 
    '''
    def login(self,request):
        obj = AuthHandler(request)
        status,response = obj.login()
        return Response(data=response, status=status)
    
    def logout(self, request):
        obj = AuthHandler(request)
        status,response = obj.logout()
        return Response(data=response, status=status)

    def register(self, request):
        obj = AuthHandler(request)
        status,response = obj.register()
        return Response(data=response, status=status)
    
    def send_otp(self, request):
        obj = AuthHandler(request)
        status,response=obj.send_otp() 
        return Response(data=response, status=status)
    
    def check_otp(self, request):
        obj = AuthHandler(request)
        status,response=obj.check_otp() 
        return Response(data=response, status=status)