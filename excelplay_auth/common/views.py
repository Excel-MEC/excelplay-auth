from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse

from .models import User
from .serializers import UserSerializer
from .decorators import is_logged_in, set_cookies

from django.views.decorators.csrf import csrf_exempt

import json
import requests
import jwt


def get_all_users(request):
    """ Get all users """

    if request.method == "GET":
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)


@csrf_exempt
def sign_in(request):
    if request.method == "POST":
        key = json.loads(request.body.decode("utf-8")).get("access_token", False)
        if not key:
            return JsonResponse({"Malformed Token": True}, status=401)
        # key = key.split(" ")
        # if len(key) != 2:
        #     return Response("Malformed Token", status.HTTP_401_UNAUTHORIZED)
        # key = key[1]
        try:
            userinfo = jwt.decode(key, settings.JWT_SECRET_KEY, algorithms="HS512")

            if not User.objects.filter(id=userinfo["user_id"]).exists():
                obj = User.objects.create(
                    id=userinfo["user_id"],
                    name=userinfo["name"],
                    profile_picture=userinfo["picture"],
                    email=userinfo["email"],
                )

            else:
                obj = User.objects.get(id=userinfo["user_id"])

            request.session["user"] = obj.id
            request.session["logged_in"] = True
            request.session.save()

            return JsonResponse({"Success": True})
        except Exception as e:
            return JsonResponse({"Malformed Token": True}, status=401)

    # if request.method == "POST":

    #     data = request.POST

    #     if 'access_token' in data:
    #         access_token = data['access_token']
    #     else:
    #         return JsonResponse({'Error': 'User not authorized'},
    #                             status=401)

    #     try:

    #         headers = {'Authorization': 'Bearer % s' % access_token}
    #         r = requests.get('http://excelplay-2019.auth0.com/userinfo',
    #                          headers=headers)

    #         userinfo = r.json()
    #         userinfo['sub'] = userinfo['sub'].split('|')[1]

    #         if not User.objects.filter(id=userinfo['sub']).exists():
    #             obj = User.objects.create(id=userinfo['sub'],
    #                                       name=userinfo['name'],
    #                                       profile_picture=userinfo['picture'],
    #                                       email=userinfo['email'])

    #         else:
    #             obj = User.objects.get(id=userinfo['sub'])

    #         request.session['user'] = obj.id
    #         request.session['logged_in'] = True
    #         request.session.save()

    #         return JsonResponse({'Success': True})

    #     except Exception as e:
    #         print('Unable to fetch userinfo', e)
    #         return JsonResponse({'Error': 'Authorization failed'},
    #                             status=500)

    # else:
    #     return JsonResponse({'Error': 'Method not allowed'}, status=405)


@set_cookies
def set_token(request):
    if request.method == "GET":
        return JsonResponse({"Success": True})
    else:
        return JsonResponse({"Error": "Invalid Request"}, status=405)


@is_logged_in
def sign_out(request):
    if request.method == "GET":
        request.session.flush()
        return JsonResponse({"Success": True})
    else:
        return JsonResponse({"Error": "Invalid Request"}, status=405)


@is_logged_in
def get_user_detail(request):
    if request.method == "GET":
        try:
            user = request.session.get("user", False)
            if user:
                user = User.objects.get(id=user)
                data = {
                    "id": user.id,
                    "name": user.name,
                    "profile_picture": user.profile_picture,
                    "email": user.email,
                }

                return JsonResponse({"data": data})

        except Exception as e:
            print(e, request.session["user"])
            return JsonResponse(
                {"Error": "Something unexpected happened while fetching userinfo"},
                status=500,
            )

    else:
        return JsonResponse({"Error": "Invalid request"}, status=405)


# Used by other microservices to get details of a certain user ID. Does not require authentication.
def get_user_detail_noauth(request):
    if request.method == "POST":
        userid = json.loads(request.body.decode("utf-8")).get("user_id", False)
        if not userid:
            return JsonResponse({"Error": "Invalid request"}, status=405)
        else:
            try:
                details = User.objects.get(id=userid)
                return JsonResponse(
                    {
                        "userid": details.id,
                        "name": details.name,
                        "email": details.email,
                        "picture": details.profile_picture,
                    },
                    status=200,
                )
            except Exception as e:
                print(e)
                return JsonResponse({"userid": -1})
    else:
        return JsonResponse({"Error": "Invalid request"}, status=405)
