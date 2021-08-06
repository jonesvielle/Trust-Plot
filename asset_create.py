from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair
import pprint
from datetime import datetime


bdb_root_url = "https://test.ipdb.io"
bdb = BigchainDB(bdb_root_url)

# identity creation
supplier = generate_keypair()

goods = {"data": {"manufacturer": "Total Oil", "brand_no": "123456",}}

metaData = {
    "date": str(datetime.now()),
    "location": "Nigeria",
    "current_condition": "contains  5%, kerosene 2%",
}

# print(supplier.public_key)

# asset creation
prepared_creation_tx = bdb.transactions.prepare(
    operation="CREATE", signers=supplier.public_key, asset=goods, metadata=metaData
)

# fufill creation
fufill_creation_tx = bdb.transactions.fulfill(
    prepared_creation_tx, supplier.private_key
)


# send over to bgchain node
sent_creation_tx = bdb.transactions.send_commit(fufill_creation_tx)
print(sent_creation_tx)
print(supplier.public_key)

# block_height = bdb.blocks.get(txid="1c04621ee0ac0731fdb467f11f12ecd59c3df70a1b2b23ce87b9c76dd39fe359")
# print(block_height)
# block = bdb.blocks.retrieve(str(block_height))
# print(block)


# try:
# send over to bgchain node
#     sent_creation_tx = bdb.transactions.send_commit(fufill_creation_tx)
#     print(sent_creation_tx)
# except TimeoutError as err:
#     print(err)

# print(fufill_creation_tx)
# print(sent_creation_tx)
# print(prepared_creation_tx)

