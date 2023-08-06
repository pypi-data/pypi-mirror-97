import requests, json, logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(threadName)-11s %(levelname)-10s %(message)s")

class MpmsController:
    """Controller da API MPMS"""

    @classmethod
    def send_product(self, url, token, accountId, itemId, product):
        """Enviar o Produto
        - Parametros:
        ---"""

        headers = dict()
        headers['Content-Type'] = 'application/json'
        headers['Authorization'] = f'Bearer {token}'

        r = requests.put(f'{url}/v1-napp/accounts/{accountId}/items/{itemId}/seller-integrator', headers=headers, data=json.dumps(product))

        if r.status_code == 200 or r.status_code == 201:
            logging.info(f'         Product sent... [{r.status_code}]')
        else:
            logging.error(f'         Failed to send Product [{r.status_code}]')

    @classmethod
    def send_intentory(self, url, token, accountId, stockId, itemId, inventory):
        """Enviar estoque
        - Parametros:
        ---"""

        headers = dict()
        headers['Content-Type'] = 'application/json'
        headers['Authorization'] = f'Bearer {token}'

        r = requests.put(f'{url}/v1-napp/accounts/{accountId}/stocks/{stockId}/items/{itemId}', headers=headers, data=json.dumps(inventory))

        if r.status_code == 200 or r.status_code == 201:
            logging.info(f'         Inventory sent... [{r.status_code}]')
        else:
            logging.error(f'         Failed to create Inventory [{r.status_code}] - {r.content.decode("utf-8")}')

    @classmethod
    def send_price(self, url, token, accountId, pricingTableId, itemId, price):
        """Enviar estoque
        - Parametros:
        ---"""

        headers = dict()
        headers['Content-Type'] = 'application/json'
        headers['Authorization'] = f'Bearer {token}'

        r = requests.put(f'{url}/v1-napp/accounts/{accountId}/pricing-tables/{pricingTableId}/items/{itemId}', headers=headers, data=json.dumps(price))

        if r.status_code == 200 or r.status_code == 201:
            logging.info(f'         Price sent... [{r.status_code}]')
        else:
            logging.error(f'         Failed to create Price [{r.status_code}]')