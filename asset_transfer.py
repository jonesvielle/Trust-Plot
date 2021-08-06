from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair
import pprint
from datetime import datetime


bdb_root_url = 'https://test.ipdb.io'
bdb = BigchainDB(bdb_root_url)

recipent = generate_keypair

assetId = "ca859ca013a9770e5045058ab46cb59829f00236af53ff7b6304349d13a404f1"
creation_tx = bdb.transactions.retrieve(assetId)
print(creation_tx['id'])
asset_id = creation_tx['id']

transfer_asset = {
    'id':asset_id
}

output_index = 0
output = creation_tx['outputs'][output_index]

transfer_input = {
    'fufillment': output['condition']['details'],
    'fufills': {
        'output_index': output_index,
        'transaction_id': creation_tx['id'],
    },
    'owners_before': output['public_keys']
}

print(recipent)

prepared_transfer_tx = bdb.transactions.prepare(
    operation='TRANSFER',
    asset=transfer_asset,
    inputs=transfer_input,
    recipients=recipent.public_key,
)
private_key = "BZEoaLnaz8JsQ7tX7hRRJJM15MfDLe7DxXb5wChSYuR8"

fufill_transfer_tx = bdb.transactions.fulfill(prepared_transfer_tx, private_key)
print("recipent public key: ", recipent.public_key)
print("asset id: ", assetId)