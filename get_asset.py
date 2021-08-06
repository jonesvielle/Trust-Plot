from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair
import pprint
from datetime import datetime


bdb_root_url = 'https://test.ipdb.io'
bdb = BigchainDB(bdb_root_url)


block_height = bdb.blocks.get(txid="ca859ca013a9770e5045058ab46cb59829f00236af53ff7b6304349d13a404f1")
print(block_height)
block = bdb.blocks.retrieve(str(block_height))
print(block)