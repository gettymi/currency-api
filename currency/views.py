
from django.conf import settings
from django.http import JsonResponse
import requests

# Create your views here.

def convert(request):
    amount = request.GET.get('amount')
    from_parameter = request.GET.get('from')
    to_parameter = request.GET.get('to')
        
    OXR_APP_ID = settings.OXR_APP_ID 
    OXR_APP_URL = settings.OXR_APP_URL

    url = f"{OXR_APP_URL}/latest.json"

    params = {"app_id":OXR_APP_ID}
    resp = requests.get(url,params).json()

    rates = resp.get('rates',{})

    if from_parameter not in rates or to_parameter not in rates:
        return JsonResponse({'error': 'Unsupported currency'}, status=400)

    try:
        amount = float(amount)
    except ValueError:
        return JsonResponse({'error': 'Amount must be a number'}, status=400)

    usd_convert = amount / rates[from_parameter]
    converted = usd_convert * rates[to_parameter]

    return JsonResponse({
        'from':from_parameter,
        'to':to_parameter,
        'amount':amount,
        'converted':round(converted,2),
        'rate':round(rates[to_parameter] / rates[from_parameter],6)
    })