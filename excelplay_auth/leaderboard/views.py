from django.http import JsonResponse

from rest_framework.decorators import api_view

from common.models import User
from common.decorators import is_logged_in

from redis_leaderboard.wrapper import RedisLeaderboard

rdb = RedisLeaderboard()


@is_logged_in
@api_view(['GET'])
def get_all_rank(request):
    
    try:
        user_id = request.session['user']
        
        try:
            user = User.objects.get(id=user_id)
            
            try:
                kryptos = rdb.get_rank('kryptos', user_id)
                dalalbull = rdb.get_rank('dalalbull', user_id)
                echo = rdb.get_rank('echo', user_id)
            
                return JsonResponse({'user_id': user_id,
                                     'name': user.name,
                                     'pic': user.profile_picture,
                                     'email': user.email,
                                     'kryptos': kryptos,
                                     'dalalbull': dalalbull,
                                     'echo': echo
                                     })
            
            except:
                return JsonResponse({'Error': 'Unable to fetch leaderboard'}, status=500)

        except:
            return JsonResponse({'Error': 'Internal server error'}, status=500)
    
    except:
        return JsonResponse({'Error': 'User not logged in'}, status=403)


@is_logged_in
@api_view(['GET'])
def kryptos_ranklist(request):
    
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
                
            
        except:
            return JsonResponse({'Error': 'Unable to fetch ranklist'}, status=500)
    
    except:
        return JsonResponse({'Error': 'User not logged in'}, status=403)


