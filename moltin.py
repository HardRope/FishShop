import requests
import time

class Moltin():
    def __init__(self, moltin_client_id, moltin_client_secret):
        self.id = moltin_client_id
        self.secret = moltin_client_secret
        self.token = ''
        self.expires_at = 0
        self.__update_token()

    def __update_token(self):
        url = 'https://api.moltin.com/oauth/access_token'
        data = {
            'client_id': self.id,
            'client_secret': self.secret,
            'grant_type': 'client_credentials',
        }
        response = requests.post(url, data=data)
        response.raise_for_status()
        token_attributes = response.json()
        self.token = token_attributes.get('access_token')
        self.expires_at = token_attributes.get('expires')

    def __check_token_alive(self):
        current_timestamp = int(time.time())
        if current_timestamp >= self.expires_at:
            return False

    def get_products(self):
        if not self.__check_token_alive():
            self.__update_token()
        url = 'https://api.moltin.com/catalog/products'
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json().get('data')

    def add_product_to_cart(self, cart_id, product):
        if not self.__check_token_alive():
            self.__update_token()
        url = f'https://api.moltin.com/v2/carts/{cart_id}/items'
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json',
        }
        product_collection = {
            'data': {
                'type': 'custom_item',
                'name': product.get('attributes').get('name'),
                'sku': product.get('attributes').get('sku'),
                'description': product.get('attributes').get('description'),
                'quantity': 1,
                'price': {
                    'amount': product.get('attributes').get('price').get('USD').get('amount'),
                },
            },
        }
        response = requests.post(url, headers=headers, json=product_collection)
        response.raise_for_status()
        return True

    def get_cart(self, cart_id):
        if not self.__check_token_alive():
            self.__update_token()
        url = f'https://api.moltin.com/v2/carts/{cart_id}'
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.get(url, headers=headers, )
        response.raise_for_status()
        moltin_cart_id = response.json().get('data').get('id')
        return moltin_cart_id

    def get_cart_items(self, cart_id):
        if not self.__check_token_alive():
            self.__update_token()
        url = f'https://api.moltin.com/v2/carts/{cart_id}/items'
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json().get('data')

    def delete_item(self, cart_id, item_id):
        if not self.__check_token_alive():
            self.__update_token()
        url = f'https://api.moltin.com/v2/carts/{cart_id}/items/{item_id}'
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.delete(url, headers=headers)
        response.raise_for_status()
        return True

