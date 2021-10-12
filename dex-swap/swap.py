from iconsdk.exception import JSONRPCException
import json
from iconsdk.icon_service import IconService
from iconsdk.providers.http_provider import HTTPProvider
from iconsdk.builder.transaction_builder import CallTransactionBuilder
from iconsdk.builder.call_builder import CallBuilder
from iconsdk.signed_transaction import SignedTransaction
from iconsdk.wallet.wallet import KeyWallet
from checkscore.repeater import retry
import sys

icon_service = IconService(HTTPProvider("https://ctz.solidwallet.io", 3))
NID = 1

wallet = KeyWallet.load(bytes.fromhex(''))

@retry(JSONRPCException, tries=10, delay=1, back_off=1)
def get_tx_result(_tx_hash):
    tx_result = icon_service.get_transaction_result(_tx_hash)
    return tx_result

addr = {
    "DEX" : "cxa0af3165c08318e988cb30993b3048335b94af6c",
    "BNUSD" : "cx88fd7df7ddff82f7cc735c871dc519838cb235bb",
    "METX" : "cx369a5f4ce4f4648dfc96ba0c8229be0693b4eca2",
    "IUSDC" : "cxae3034235540b924dfcc1b45836c293dcc82bfb7",
    "USDS" : "cxbb2871f468a3008f80b08fdde5b8b951583acf06",
    "SICX" : "cx2609b924e33ef00b648a409245c7ea394c467824",
    "OMM": "cx1a29259a59f463a67bb2ef84398b30ca56b5830a"
}

def send_tx(_from, _to, method, params):
    transaction = CallTransactionBuilder()\
        .from_(_from.get_address())\
        .to(_to)\
        .step_limit(3_000_000)\
        .nid(NID)\
        .nonce(100)\
        .method(method)\
        .params(params)\
        .build()

    signed_transaction = SignedTransaction(transaction, _from)
    tx_hash = icon_service.send_transaction(signed_transaction)
    print(get_tx_result(tx_hash))
    return tx_hash

def get_balance_of(token_name):
    address = addr[token_name]
    call = CallBuilder(
        to=address,
        method='balanceOf',
        params={'_owner': f'{wallet.get_address()}'}
    ).build()
    try:
        result = icon_service.call(call)
        return result
    except:
        print('Get Balance Of Error')
        return '1'

def current_icx_price():
    result = requests.post(
        url= 'https://ctz.solidwallet.io/api/v3',
        data=json.dumps({"jsonrpc":"2.0","id":1630737303776,"method":"icx_call","params":{"to":"cxe647e0af68a4661566f5e9861ad4ac854de808a2","dataType":"call","data":{"method":"get_reference_data","params":{"_base":"ICX","_quote":"USD"}}}})
    )
    return int(result.json()['result']['rate'], 16)/10**18

def swap(fromToken, toToken, fromTokenAmount):
    if fromToken == 'sICX':
        fromTokenAmount = int(fromTokenAmount / (get_current_icx_price()) * 10 **  18)
    elif fromToken == 'IUSDC':
        fromTokenAmount = int(fromTokenAmount * 10 ** 6)
    elif fromToken == "USDS":
        fromTokenAmount = int(fromTokenAmount * 10 ** 18)

    actual_data = {
        'method': '_swap',
        'params': {
            'toToken': addr[toToken],
        }
    }
    encoded_data = bytes(json.dumps(actual_data), 'utf-8')
    tx_result = send_tx(wallet, addr[fromToken], method='transfer', params={
        "_to": addr["DEX"],
        "_value": fromTokenAmount,
        "_data": encoded_data
    })
    print(f'Swapping {fromTokenAmount} {fromToken} to {get_balance_of(toToken)} {toToken}')
    return tx_result

if __name__ == "__main__":
    if len(sys.argv) < 4:
        exit()
      
    fromToken = sys.argv[1]
    toToken = sys.argv[2]
    fromTokenAmount = float(sys.argv[3])

    swap(fromToken, toToken, fromTokenAmount)