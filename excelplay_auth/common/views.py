
from django.shortcuts import render
from django.http import JsonResponse,HttpResponse

from django.views.decorators.csrf import csrf_exempt

from .models import *

from urllib import request as rq
import json

def get_all_users(request):
    ''' Get all users '''
    
    if request.method == "GET":
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)

@csrf_exempt
def sign_in(request):
	if 'access_token' in request.POST:
		access_token = request.POST['access_token']
	else:
		return JsonResponse({ 'success' : False })

	try:
		headers = { 'Authorization' : 'Bearer %s'%access_token }
		req = rq.Request('https://excelplay2k18.auth0.com/userinfo',headers=headers)
		data = json.loads( rq.urlopen(req).read().decode("utf-8") )
	except:
		return JsonResponse({ 'success' : False })


	created = False
	if not User.objects.filter(user_id=data['sub']).exists():
		obj = User.objects.create(user_id = data['sub'],
			username = data['name'],
			profile_picture = data['picture'],
			email = data['email']
			)
	else:
		obj = User.objects.get(user_id = data['sub'])

	if created:
		user_count_channel_push({'count': User.objects.all().count() })

	request.session['user'] = obj.user_id

	return JsonResponse({ 'success' : True })

def sign_out(request):
	request.session.flush()
	return JsonResponse({ 'success' : True })