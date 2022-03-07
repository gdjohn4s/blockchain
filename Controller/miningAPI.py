from flask import jsonify
from Models.blockchain import blockchain
from flask import Blueprint
from Utils.hosts import *


mining_api = Blueprint('mining_api', __name__)


def send_block(block):
   hosts = GetHostsAddress()
   acceptedCounter = 0
   for host in hosts:
      print(block)
      try:
         requests.get(f"http://{host}:5000/merge_block/{block['proof']}/{block['previous_hash']}/{block['text']}/{block['signature']}")
         accepted += 1
      except Exception as ex:
         print(f"Can't send block to node {host}\n Cause: \n {ex}")

      return f"Block sended to {acceptedCounter} on {len(hosts)}"


@mining_api.route('/mine_block/<signature>/<message>', methods=['GET'])
def mine_block(signature, message):
   # get the data we need to create a block
   previous_block = blockchain.get_previous_block()
   previous_proof = previous_block['proof']
   proof = blockchain.proof_of_work(previous_proof)
   previous_hash = blockchain.hash(previous_block)
   if blockchain.is_chain_valid(blockchain.chain):
      block = blockchain.create_blockchain(
         proof, previous_hash, message, signature)
      send_block(block)
      code = 200
      response = {'message': 'Block mined!',
                  'index': block['index'],
                  'timestamp': block['timestamp'],
                  'proof': block['proof'],
                  'previous_hash': block['previous_hash']}
   else:
      code = 400
      response = {'message': 'Block not mined!'}

   return jsonify(response), code