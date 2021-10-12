import requests
import sys
from pprint import pprint
import json

def main():
    _hash = sys.argv[1]
    headers = {
        'Content-Type': 'application/json',
    }
    data = {
        "jsonrpc": "2.0",
        "method": "debug_getTrace",
        "id": 1234,
        "params": {
            "txHash": _hash
            }
        }

    response = requests.post('<ENDPOINT>', headers=headers, data=json.dumps(data))
    try:
        pprint(response.json().get('result'))
    except Exception as e:
        pprint("ERROR")

if __name__ == '__main__':
    main()
