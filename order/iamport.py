import requests

from django.conf import settings

def get_token():
    access_data = {
        'imp_key' : settings.IAMPORT_KEY,
        'imp_secret': settings.IAMPORT_SECRET
    }

    url = "https://api.iamport.kr/users/getToken"

    req = requests.post(url,data=access_data)
    access_res = req.json()

    if access_res['code'] is 0:
        return access_res['response']['access_token']
    else:
        return None

def payments_prepare(order_id,amount,*args,**kwargs):
    access_token = get_token()
    if access_token:
        access_data = {
            'merchant_uid':order_id,
            'amount':amount
        }
        url = "https://api.iamport.kr/payments/prepare"
        headers = {
            'Authorization':access_token
        }
        req = requests.post(url,data=access_data,headers=headers)
        res = req.json()

        if res['code'] is not 0:
            raise ValueError("API 통신 오류")
        else:
            raise ValueError("토큰 오류")