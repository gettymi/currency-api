
from django.conf import settings
from django.http import JsonResponse
import requests
from django.core.cache import cache

import logging



logger = logging.getLogger(__name__)

OXR_APP_ID = settings.OXR_APP_ID 
OXR_BASE_URL = settings.OXR_BASE_URL


def convert(request):
    logger.info(f"/convert called with params: {request.GET.dict()}")
    amount = request.GET.get('amount')
    from_parameter = request.GET.get('from')
    to_parameter = request.GET.get('to')
    
    if not amount or not from_parameter or not to_parameter:
        logger.error("Missing required parameters for convert endpoint.")
        return JsonResponse(
            {"success":False, "error": "Missing required parameters"},
            status = 400
        )
    
    try:
        amount = float(amount)
        if amount <=0 :
            raise ValueError
    except ValueError:
        logger.error(f"Invalid amount received: {amount}")
        return JsonResponse(
            {"success":False, "error":"Missing required parameters"},
            status = 400
        )
    
    valid_codes = get_valid_currency_codes()

    if from_parameter not in valid_codes or to_parameter not in valid_codes:
        logger.error(f"Unsupported currency code: from={from_parameter}, to={to_parameter}")
        return JsonResponse(
            {"success":False,"error":"Unsupported currency code"},
            status = 400
        )


    url = f"{OXR_BASE_URL}/latest.json"

    params = {"app_id":OXR_APP_ID}

    try:
        resp = requests.get(url, params)
        resp.raise_for_status()
        data = resp.json()
    except requests.RequestException as e:
        logger.error(f"Failed to fetch rates from OXR: {e}")
        return JsonResponse({'success': False, 'error': 'API is unreachable'}, status=502)
    except ValueError as e:
        logger.error(f"Invalid JSON from OXR: {e}")
        return JsonResponse({'success': False, 'error': 'API did not return valid JSON'}, status=502)

    rates = data.get('rates', {})
    if from_parameter not in rates or to_parameter not in rates:
        logger.error(f"Currency rate not found: from={from_parameter}, to={to_parameter}")
        return JsonResponse({'success': False, 'error': 'Unsupported currency'}, status=400)

    


    usd_convert = amount / rates[from_parameter]
    converted = usd_convert * rates[to_parameter]

    logger.info(f"Converted {amount} {from_parameter} to {to_parameter}: {converted}")
    return JsonResponse({
        'from':from_parameter,
        'to':to_parameter,
        'amount':amount,
        'converted':round(converted,2),
        'rate':round(rates[to_parameter] / rates[from_parameter],6)
    })

def currencies(request):
    logger.info("/currencies called")
    url = f"{OXR_BASE_URL}/currencies.json"
    params = {
        "app_id": OXR_APP_ID
    }

    try:
        r = requests.get(url, params)
        r.raise_for_status() 
        data = r.json()
        logger.info("Fetched currencies successfully.")
    except requests.RequestException as e:
        logger.error(f"API is unreachable: {e}")
        return JsonResponse({'success':False,'error': 'API is unreachable'}, status=502)
    except ValueError as e:
        logger.error(f"API did not return valid JSON: {e}")
        return JsonResponse({'success':False,'error': 'API did not return valid JSON'}, status=502)

    return JsonResponse(data)


def latest(request):
    logger.info("/latest called")
    symbols = request.GET.get('symbols')

    url = f"{OXR_BASE_URL}/latest.json"
    params = {
        "app_id":OXR_APP_ID,
    }

    cache_key = f"latest_{symbols if symbols else 'all'}"
    data = cache.get(cache_key)

    if data:
        logger.info("Used cached data")
        return JsonResponse(data)
        

    if symbols:
        params["symbols"] = symbols


    try:
        r = requests.get(url, params)
        r.raise_for_status() 
        data = r.json()
        logger.info("Fetched latest successfully.")
    except requests.RequestException as e:
        logger.error(f"API is unreachable: {e}")
        return JsonResponse({'success':False,'error': 'API is unreachable'}, status=502)
    except ValueError as e:
        logger.error(f"API did not return valid JSON: {e}")
        return JsonResponse({'success':False,'error': 'API did not return valid JSON'}, status=502)

    cache.set(cache_key,data,timeout=60)

    return JsonResponse(
        data 
    )


def get_valid_currency_codes():
    logger.info("Fetching valid currency codes (from cache or API)")
    codes = cache.get("currency_codes")

    if codes:
        return codes
    
    url = F"{OXR_BASE_URL}/currencies.json"
    params = {
        "app_id":OXR_APP_ID
    }

    try:
        r = requests.get(url,params)
        r.raise_for_status()
        data = r.json()
        codes = set(data.keys())
        cache.set('currency_codes',codes,timeout=24*60*60)
        return codes
    except requests.RequestException:
        return set()



    