from django.shortcuts import render
from django.http import JsonResponse

from .models import User
from .serializers import UserSerializer

def get_all_users(request):
    ''' Get all users '''
    
    if request.method == "GET":
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)

