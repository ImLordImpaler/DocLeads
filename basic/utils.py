from django.db.models.query import QuerySet
from accounts.models import User 

def parse_response(obj, return_fields):
    if isinstance(obj, QuerySet): # Will get list incase of mutiple object responses
        response_list = []
        for doctor in obj:
            response_obj = {}
            for field in return_fields:
                response_obj[field] = doctor.get(field)

            response_list.append(response_obj)
        return response_list 
    else:
        response = {}
        for field in return_fields:
            response[field] = getattr(obj, field, None)
        return response
    

def create_user_for_instance(instance,type,password, **kwargs):
    if type == 'doctor':
        kwargs['is_doctor'] = True
    elif type == 'paitent':
        kwargs['is_paitent'] = True 

    user = User.objects.create_user(
        name = instance.name, 
        phone=instance.phone, 
        password=password,
        **kwargs
    )
    instance.user = user 
    instance.save() 