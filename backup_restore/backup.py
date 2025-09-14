import base64
import gzip
from helpers import get_bytes

def decompress(pg_dump: bytes) -> str:
    try:
        decompressed = gzip.decompress(decoded_data)
        dump_str = decompressed.decode('utf-8')
        print(type(dump_str))
        return dump_str
    except Exception as e:
        print(f"no gzip: {e}")

if __name__ == "__main__":
    url: str = "https://hackattic.com/challenges/backup_restore/problem?access_token=b5a60cc0b43768a6"
    data = get_bytes(url).get("dump", {})
    decoded_data = base64.b64decode(data, validate=True)
    decompressed_dump = decompress(decoded_data)
    #TODO: re.S/DOTALL flag, re.search, the rest of regex
    match = re.search(
        r"COPY public.criminal_records"
    )
