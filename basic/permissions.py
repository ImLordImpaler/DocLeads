from rest_framework import permissions 
from rest_framework.exceptions import PermissionDenied

class IsDoctorOrSelf(permissions.BasePermission):
    def has_permission(self, request, view):
        '''
        
        '''
        raise PermissionDenied("Kya bai?")
    

class IsPatientOrSelf(permissions.BasePermission):

    def has_permission(self, request, view):
        return True
    

class IsSameDocOrNot(permissions.BasePermission):

    def has_permission(self, request, view):
        return True 

    def has_object_permission(self, request, view, obj):
        import pdb
        pdb.set_trace() 

        return True
