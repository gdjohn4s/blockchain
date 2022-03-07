from flask import jsonify
from Models.blockchain import blockchain
from flask import Blueprint

chain_api = Blueprint('chain_api', __name__)

@chain_api.route('/merge_block/<proof>/<previous_hash>/<text>/<signature>', methods=['GET'])
def merge_block(proof, previous_hash, text, signature):
   previous_block = blockchain.get_previous_block()
   previous_proof = previous_block['proof']
   proof = blockchain.proof_of_work(previous_proof)
   previous_hash = blockchain.hash(previous_block)
   blockchain.create_blockchain(int(proof), previous_hash, text, signature)
   return {'message' : 'True'} , 200

@chain_api.route('/get_chain', methods=['GET'])
def get_chain():
   response = {'chain': blockchain.chain,
               'length': len(blockchain.chain)}
   return jsonify(response), 200

@chain_api.route('/edit_chain/<index>', methods=['GET'])
def edit_chain(index):
   blockchain.chain[int(index)]['signature'] = "debug"
   response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
   return jsonify(response), 200