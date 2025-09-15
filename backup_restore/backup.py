import base64
import requests
import re
import gzip
from helpers import get_bytes


def decompress(pg_dump: bytes) -> str:
    try:
        decompressed = gzip.decompress(decoded_data)
        dump_str = decompressed.decode("utf-8")
        print(type(dump_str))
        return dump_str
    except Exception as e:
        print(f"no gzip: {e}")


if __name__ == "__main__":
    url: str = "https://hackattic.com/challenges/backup_restore/problem?access_token=b5a60cc0b43768a6"
    data = get_bytes(url).get("dump", {})
    decoded_data = base64.b64decode(data, validate=True)
    decompressed_dump = decompress(decoded_data)
    # TODO: re.S/DOTALL flag, re.search, the rest of regex
    match = re.search(
        r"COPY public\.criminal_records.*?FROM stdin;\n(.*?)\n\\\.\n",
        decompressed_dump,
        re.S,
    )

    alive: list[str] = []
    if match:
        copy_data = match.group(1).strip().splitlines()
        headers = [
            "id",
            "name",
            "felony",
            "ssn",
            "home_address",
            "entry",
            "city",
            "status",
        ]

        ssn_index = headers.index("ssn")
        status_index = headers.index("status")

        for line in copy_data:
            values = line.split("\t")  # COPY uses tab-delimited
            if values[status_index] == "alive":
                alive.append(values[ssn_index])

    data = {"alive_ssns": alive}

    URL = "https://hackattic.com/challenges/backup_restore/solve?access_token=b5a60cc0b43768a6"
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(URL, json=data, headers=headers)
        print(response.status_code)
        print(response.text)
    except Exception as e:
        print(f"Error: {e}")
