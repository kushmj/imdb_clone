from rest_framework import permissions

class ReviewUserOrReadOnly(permissions.BasePermission):
   # permission allowed for reviewusers 
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
             return True
        else:
            return obj.review_user == request.user
       
        
class IsAdminOrReadonly(permissions.IsAdminUser):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            print("Admin user", request.user.is_staff)
            return bool(request.user and request.user.is_staff)

class UserprofileOwnerOrReadonly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        print("user", obj.user_name, request.user)
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.user_name == request.user