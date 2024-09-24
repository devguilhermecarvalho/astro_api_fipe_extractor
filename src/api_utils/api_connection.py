# src/api_utils/api_connection.py

import requests
from functools import wraps

class BaseConnector:
    def __init__(self, url):
        self.url = url

    @classmethod
    def request_post(cls):
        def decorator(func):
            @wraps(func)
            def wrapper(self, data=None, *args, **kwargs):
                try:
                    data_to_send = data if data else {}
                    response = requests.post(self.url, data=data_to_send)
                    response.raise_for_status()
                    
                    if response.status_code == 200:
                        print(f"\nRequisição bem-sucedida.")
                        return func(self, response.json(), *args, **kwargs)
                    
                    elif response.status_code == 426:
                        pass

                    elif response.status_code == 500:
                        pass
                    
                    else:
                        print(f"Falha na requisição. Status Code: {response.status_code}")
                        return None
                except requests.exceptions.RequestException as e:
                    print(f"Erro na requisição: {e}")
                    return None

            return wrapper
        return decorator
