#!/bin/bash

curl --location --request POST 'API ENDPOINT' \
--header 'Content-Type: application/json' \
--data-raw '{
    "jsonrpc": "2.0",
    "method": "debug_getTrace",
    "id": 1234,
    "params": {
        "txHash":'\""$1"\"'
    }
}'
