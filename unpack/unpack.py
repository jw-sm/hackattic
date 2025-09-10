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


b = get_bytes().get("bytes", "")
base64_decoded = base64.b64decode(b)
print(f"{len(base64_decoded)} bytes")
unpacked = struct.unpack("<8I", base64_decoded)
print(unpacked)
signed_int, = struct.unpack("<i", base64_decoded[0:4])
unsigned_int, = struct.unpack("<I", base64_decoded[4:8])
signed_short, = struct.unpack("<h", base64_decoded[8:10])
signed_float, = struct.unpack("<f", base64_decoded[10:14])
signed_double, = struct.unpack("<d", base64_decoded[14:22])
another_double, = struct.unpack("!d", base64_decoded[22:30])

def post_bytes():
    URL = "https://hackattic.com/challenges/help_me_unpack/solve?access_token=b5a60cc0b43768a6"
    headers = {"Content-Type": "application/json"}

    payload = {
        "int": signed_int,
        "uint": unsigned_int,
        "short": signed_short,
        "float": signed_float,
        "double": signed_double,
        "big_endian_double": another_double,
    }
    response = requests.post(URL, json=payload, headers=headers)
    print(response.status_code)
    return response.text

print(post_bytes())


