# blockstack_recover

This is a utility to recover private keys from wallets created by the legacy and now-abandoned blockstack-client Python module. This tool is inspired by the success story of [someone who recovered 1BTC](https://bitcointalk.org/index.php?topic=5306458.0) using a basic version of this tool. I ported it to Python 3 and made it easy to run with minimum dependencies. This utility works on Windows, MacOS and Linux.

Discussion thread on Bitcointalk: https://bitcointalk.org/index.php?topic=5317833.0
## Installation

Install using pip:

```
pip install blockstack_recover
```

Or clone this Github repo and then run:

```
apt-get install build-essential libffi-dev libssl-dev python-dev
python setup.py install
```

If installation fails because of dependency issues, try creating a virtualenv first and installing blockstack_recover in that:

```
python -m venv blockstack_env
# On Unix
source blockstack_env/bin/activate
# On Windows
blockstack_env\Scripts\activate.bat
# on all platforms
pip install blockstack_recover
```

## Running

### Decrypting encrypted wallet.json

Blockstack creates the the wallet.json file inside $HOME/.blockstack for Linux and C:/Users/username/.blockstack for Windows. It creates the .blockstack folder in your home folder in all cases.

This file is encrypted and can be decrypted using the `decrypt` subcomand if you know the password.

Example invocation using `blockstack-recover decrypt /home/ubuntu/.blockstack/wallet.json /tmp/decrypted-wallet.json`

```
Blockstack Legacy wallet private key extractor by NotATether
----
Opening wallet file /tmp/encwallet.json...
Enter wallet password:
Dumping decryted wallet to /tmp/wallet.json

-----
master_private_key: e33d56f41cf64bc53cda0c5d963bf673a4bdd7db01c3c6d86937b8c2f99286b201
wallet_password: qwertyuiop
```

### Extracting private keys

Once you have the decrypted wallet.json, or perhaps you have the copy that Blockstack asked you to backup when you created the wallet, use the `extract` subcommand to dump its wallet information including private keys to the terminal.

Example incovation using `blockstack_recover extract /tmp/decrypted-wallet.json`:

```
Blockstack Legacy wallet private key extractor by NotATether
-----

Opening wallet file ../wallet.json...
Deriving master private key...

Dumping wallet info: Make sure to import payment_WIF

-----
master_private_key: e33d56f41cf64bc53cda0c5d963bf673a4bdd7db01c3c6d86937b8c2f99286b201
wallet_password: qwertyuiop
-----

-----
owner_addresses: ['1HSsAuiZkBZr7UtCHpGpun6KNEZVN7VeYw']
owner_addresses: 1HSsAuiZkBZr7UtCHpGpun6KNEZVN7VeYw
owner_key_hex: eea604061aa6d40be8c975758335869c55369692725f326d03400d984068354601
WIF owner: L5DcUHwCoLSmAVXL1pa2ycaVqCN3g4LUYWJvxaBCKyULJn4HXUZk
-----
payment_addresses: ['1NGyJBY8peLGMiGQRWsd1J96iJ8XppBh2B']
payment_addresses: 1NGyJBY8peLGMiGQRWsd1J96iJ8XppBh2B
payment_key_hex b13c3ba20318abf2b9f6aa017964c809e9d3215396cef1648c2f94f92264926701
WIF payment: L3AEUTCqJsqWv2YowCwRrJFYw5tsUaVunokSaQQZpDKVCtG7i1tM
-----
payment_addresses: ['19FFB3N65WZ4o95Je3pYLiW51a1qC1Ajo9']
payment_addresses: 19FFB3N65WZ4o95Je3pYLiW51a1qC1Ajo9
payment_key_hex 162c8298b7104d4d50b782f5ffd689c80d6e2e53f949703e6e137e2d7bf3a96101
WIF payment: KwxpAVS4wc7qUM7fPzZosih2Hp55JRvZuSwT9oZ9SKBaC4gu2u9k
-----

FROM MASTER
Address: 1CiuZ4G32KqgiCAePLpMBUPtZ6im8iLVNa
Priv HEX: e33d56f41cf64bc53cda0c5d963bf673a4bdd7db01c3c6d86937b8c2f99286b201
WIF Master: L4qSBYSbfeHM1nCL1esc6kANbkmdKhXGdSSLcHev42Kt94GxiBrr
```

Your money will be located in the `WIF payment` private key, so import or sweep that into another wallet.
