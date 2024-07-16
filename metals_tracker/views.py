from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def reloadPrices(request):
    if request.method == 'POST':
        # Your logic here
        return JsonResponse({'message': 'Prices reloaded successfully'})
    return JsonResponse({'error': 'Invalid request'}, status=400)