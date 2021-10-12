## SWAP tokens from dex
---
Swapping from balanced-dex is time consuming. Yeah you can get price data and all, but command line makes it much faster :').

```shell
python3 USDS BNUSD 1
# python3 from_token to_token amount
```

This swaps 1 USDS to BNUSD at that rate.
You can swap if there is USDS/BNUSD pool pair, which exists.
You can't swap USDS with IUSDC directly.

### Prerequisties:
 - Get your private key and place it on line number 14 of swap.py

