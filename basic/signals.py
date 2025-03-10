from django.db.models.signals import post_save 
from django.dispatch import receiver

# from django.contrib.auth.models import User 
from accounts.models import User
from .models import Doctor, Patient

# @receiver(post_save, sender=Doctor)
# def create_user_for_doctor(sender, instance, created, **kwargs):
#     if created:
#         phone = instance.phone 
#         user = User.objects.create_user(
#             name=instance.name,
#             phone=phone, 
#             password=phone,
#             is_doctor=True,
#         )
#         instance.user = user
#         instance.save()

# @receiver(post_save, sender=Patient)
# def create_user_for_paitent(sender, instance, created, **kwargs):
#     if created:
#         phone = instance.phone 
#         user= User.objects.create_user(
#             name = instance.name,
#             phone=phone, 
#             password=phone
#         )
#         instance.user=user
#         instance.save()
