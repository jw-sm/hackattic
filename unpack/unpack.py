import struct
import base64
import requests
from helpers import get_bytes


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


if __name__ == "__main__":
    url: str = "https://hackattic.com/challenges/help_me_unpack/problem?access_token=b5a60cc0b43768a6"
    # get the bytes from json
    b = get_bytes(url).get("bytes", "")
    # decode to base64
    base64_decoded = base64.b64decode(b)

    # note that everything is in the context of 32-bit platform, and an int is 4-bytes.
    # "xx" was used as format string to skip 2 bytes to be used as padding
    # since the next type is going to be 8-bytes.
    # 4 + 4 + 2 = 10,
    s_int, u_int, s_short, s_float, s_double = struct.unpack(
        "<iIhxxfd", base64_decoded[:24]
    )

    (network_double,) = struct.unpack("!d", base64_decoded[24:32])
    result = post_bytes()
    print(result)
