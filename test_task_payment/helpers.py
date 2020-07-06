import requests
from validators import url as url_validator
from hashlib import sha256
from collections import OrderedDict


class Piastrix():

    def __init__(self, shop_id, secret_key, base_url):
        self.base_url = base_url
        self.secret_key = secret_key
        self.shop_id = shop_id

    def _post(self, endpoint, body):
        url = self._form_url(endpoint)
        response = requests.post(url, json=body).json()
        if response['result'] is False:
            raise PiastrixApiException(response['message'],
                                       response['error_code'])

        return response['data']

    def _sign(self, data, required_fields):
        sorted_data = [str(data[key]) for key in sorted(required_fields)]
        signed_data = ':'.join(sorted_data) + self.secret_key
        data['sign'] = sha256(signed_data.encode('utf-8')).hexdigest()

    def _form_url(self, endpoint):
        # Typical case for url forming.
        typical_case = self.base_url + endpoint

        if self.base_url.endswith('/'):
            formed_url = typical_case if not endpoint.startswith('/') else self.base_url[:-1] + endpoint
        else:
            formed_url = typical_case if endpoint.startswith('/') else self.base_url + '/' + endpoint

        if url_validator(formed_url):
            return formed_url
        else:
            raise ValueError(f'Url "{formed_url}" is not valid!')

    def bill(self, shop_amount, shop_currency, payer_currency,
             shop_order_id, description=None):

        required_fields = [
            'shop_amount',
            'shop_currency',
            'shop_id',
            'shop_order_id',
            'payer_currency'
        ]

        body = {
            "shop_amount": shop_amount,
            "shop_currency": shop_currency,
            "payer_currency": payer_currency,
            "shop_order_id": shop_order_id,
            "shop_id": self.shop_id
        }

        if description:
            body['description'] = description

        self._sign(body, required_fields)
        return self.get_data('bill/create', body)

    def invoice(self, amount, currency, shop_order_id,
                payway='payeer_rub', description=None):

        required_fields = [
            'amount',
            'currency',
            'payway',
            'shop_id',
            'shop_order_id'
        ]

        body = {
            "amount": amount,
            "currency": currency,
            "shop_order_id": shop_order_id,
            "payway": payway,
            "shop_id": self.shop_id
        }

        if description:
            body['description'] = description

        self._sign(body, required_fields)
        return self.get_data('invoice/create', body)

    def pay(self, amount, currency, description, shop_order_id, lang='ru'):

        if lang not in ('ru', 'en'):
            raise ValueError(f'{lang} is not valid language')

        required_fields = [
            'amount',
            'currency',
            'shop_id',
            'shop_order_id'
        ]

        form_data = {
            "amount": amount,
            "currency": currency,
            "description": description,
            "shop_order_id": shop_order_id,
            "shop_id": self.shop_id
        }

        self._sign(form_data, required_fields)
        return form_data, f"https://pay.piastrix.com/{lang}/pay"


class PiastrixApiException(Exception):

    def __init__(self, message, error_code):
        super().__init__(message)
        self.error_code = error_code

