import requests
import struct
import base64
from requests.exceptions import HTTPError


# get the base64-encoded pack of bytes
def get_bytes():
    URL: str = "https://hackattic.com/challenges/help_me_unpack/problem?access_token=b5a60cc0b43768a6"
    try:
        response = requests.get(URL)
        response.raise_for_status()
    except HTTPError as http_err:
        print(f"HTTP error occured: {http_err}")
    except Exception as err:
        print(f"Other error occured: {err}")
    else:
        data = response.json()
        return data

# get the bytes from json
b = get_bytes().get("bytes", "")
# decode to base64
base64_decoded = base64.b64decode(b)

s_int, u_int, s_short, s_float, s_double = struct.unpack("<iIhxxfd", base64_decoded[:24])

network_double, = struct.unpack("!d", base64_decoded[24:32])

def post_bytes():
    URL = "https://hackattic.com/challenges/help_me_unpack/solve?access_token=b5a60cc0b43768a6"
    headers = {"Content-Type": "application/json"}
    params = {"playground": 1}

    payload = {
        "int": s_int,
        "uint": u_int,
        "short": s_short,
        "float": s_float,
        "double": s_double,
        "big_endian_double": network_double,
    }
    response = requests.post(URL, params=params, json=payload, headers=headers)
    print(response.status_code)
    return response.json()

result = post_bytes()
print(result)



