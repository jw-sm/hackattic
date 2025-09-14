from requests.exceptions import HTTPError
import requests

# get the base64-encoded pack of bytes
def get_bytes(url: str):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except HTTPError as http_err:
        print(f"HTTP error occured: {http_err}")
    except Exception as err:
        print(f"Other error occured: {err}")
    else:
        data = response.json()
        return data