from django.http import JsonResponse


from common.models import User
from common.decorators import is_logged_in

from redis_leaderboard.wrapper import RedisLeaderboard

rdb = RedisLeaderboard('redis', 6379, 0)


@is_logged_in
def get_all_rank(request):

    if request.method == "GET":
        try:
            user_id = request.session['user']

            try:
                user = User.objects.get(id=user_id)
                print(user)

                try:
                    kryptos = rdb.get_rank('kryptos', user_id)
                    dalalbull = rdb.get_rank('dalalbull', user_id)
                    echo = rdb.get_rank('echo', user_id)
                    circuimstance = rdb.get_rank('circuimstance', user_id)

                    return JsonResponse({'user_id': user_id,
                                         'name': user.name,
                                         'pic': user.profile_picture,
                                         'email': user.email,
                                         'kryptos': kryptos,
                                         'circuimstance': circuimstance,
                                         'dalalbull': dalalbull,
                                         'echo': echo
                                         })

                except Exception as e:
                    print(e)
                    return JsonResponse({'Error': 'Unable to fetch leaderboard'}, status=500)

            except Exception as e:
                print(e)
                return JsonResponse({'Error': 'Internal server error'}, status=500)

        except:
            return JsonResponse({'Error': 'User not logged in'}, status=403)
    else:
        return JsonResponse({'Error': 'Method not allowed'}, status=405)


@is_logged_in
def kryptos_ranklist(request):

    if request.method == "GET":
        try:
            user_id = request.session['user']

            try:
                ranklist = []

                users = rdb.get_all('kryptos')
                rank = 1

                for user_id, score in users:
                    player = {}
                    user = User.objects.get(id=user_id)

                    player['id'] = user.id
                    player['name'] = user.name
                    player['pic'] = user.profile_picture
                    player['rank'] = rank
                    player['level'] = round(score)

                    rank += 1
                    ranklist.append(player)

                return JsonResponse({'ranklist': ranklist})

            except:
                return JsonResponse({'Error': 'Internal Server Error'}, status=500)

        except:
            return JsonResponse({'Error': 'User not logged in'}, status=403)

    else:
        return JsonResponse({'Error': 'Method not allowed'}, status=405)


@is_logged_in
def circuimstance_ranklist(request):

    if request.method == "GET":
        try:
            user_id = request.session['user']

            try:
                ranklist = []

                users = rdb.get_all('circuimstance')
                rank = 1

                for user_id, score in users:
                    player = {}
                    user = User.objects.get(id=user_id)

                    player['id'] = user.id
                    player['name'] = user.name
                    player['pic'] = user.profile_picture
                    player['rank'] = rank
                    player['level'] = round(score)

                    rank += 1
                    ranklist.append(player)

                return JsonResponse({'ranklist': ranklist})

            except:
                return JsonResponse({'Error': 'Internal Server Error'}, status=500)

        except:
            return JsonResponse({'Error': 'User not logged in'}, status=403)

    else:
        return JsonResponse({'Error': 'Method not allowed'}, status=405)


@is_logged_in
def dalalbull_ranklist(request):

    if request.method == "GET":
        try:
            user_id = request.session['user']

            try:
                ranklist = []

                users = rdb.get_all('dalalbull')
                rank = 1

                for user_id, score in users:
                    player = {}
                    user = User.objects.get(id=user_id)

                    player['id'] = user.id
                    player['name'] = user.name
                    player['pic'] = user.profile_picture
                    player['rank'] = rank
                    player['level'] = round(score)

                    rank += 1
                    ranklist.append(player)

                return JsonResponse({'ranklist': ranklist})

            except Exception as e:
                print(e)
                return JsonResponse({'Error': 'Internal Server Error'}, status=500)

        except:
            return JsonResponse({'Error': 'User not logged in'}, status=403)

    else:
        return JsonResponse({'Error': 'Method not allowed'}, status=405)


def test_ldb(request):
    rdb.add('aa', 'one', 1)
    s = rdb.get_rank('aa', 'one')
    print(s)
    return JsonResponse({'Success': True})
