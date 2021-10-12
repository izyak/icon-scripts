## Goloop
---
Goloop doesn't directly show revert message and the cause of txn fail.

Not as convenient as icon 1.0, but we can get detailed info about the tx by querying txn hash on an api.

Since it is not convenient to modify the command everytime, here is a script. :')

---
Here are 2 files, goloop.sh and goloop.py
First, configure the endpoint to your local goloop or sejong testnet or mainnet.

Set an alias for any of these files in `.bashrc` or `.zshrc`.

```shell
alias goloop="~/directory/goloop.sh"
# OR
alias goloop="python3 ~/directory/goloop.py"
```

If you use goloop.sh, you need to make it executable with the following command.
```shell
chmod +x ./golooop.sh
```

Then, to get detailed info about any transaction, enter the following command in the terminal.
```shell
goloop txn-hash
# goloop 0xa3333b7fb6c56945274215ce5d361409271200fd28a4a5c1d1378eb7ab284492
```
