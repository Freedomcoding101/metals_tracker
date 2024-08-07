from django.http import JsonResponse

def getRoutes(request):
    routes = [
        {'GET': '/api/gold'},
        {'GET': '/api/gold/<id>'},
        {'POST': '/api/gold'},
        {'PUT': '/api/gold/<id>'},

        {'POST': 'api/users/token'},
        {'POST': 'api/users/token/refresh'},
        
    ]

    return JsonResponse(routes, safe=False)