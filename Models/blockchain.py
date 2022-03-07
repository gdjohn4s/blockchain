import json
import hashlib
import datetime
from Utils.hosts import  GetHostsAddress
import requests

class Blockchain:
    def __init__(self):
       self.chain = []
       self.create_blockchain(proof=1, previous_hash='0',
                              text='Hello World', signature='Pippo')

    def create_blockchain(self, proof, previous_hash, text, signature, timestamp = None):
        if timestamp is not None:
            timestamp = str(datetime.datetime.now())
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'proof': proof,
            'previous_hash': previous_hash,
            'text': text,
            'signature': signature
            }

        self.chain.append(block)
        return block

    def get_previous_block(self):
       last_block = self.chain[-1]
       return last_block

    def proof_of_work(self, previous_proof):
       # miners proof submitted
       new_proof = 1
       # status of proof of work
       check_proof = False
       while check_proof is False:
           # problem and algorithm based off the previous proof and new proof
           hash_operation = hashlib.sha256(
               str(new_proof ** 2 - previous_proof ** 2).encode()).hexdigest()
           # check miners solution to problem, by using miners proof in cryptographic encryption
           # if miners proof results in 4 leading zero's in the hash operation, then:
           if hash_operation[:2] == '00':
               check_proof = True
           else:
               # if miners solution is wrong, give mine another chance until correct
               new_proof += 1
       return new_proof

   # generate a hash of an entire block
    def hash(self, block):
       encoded_block = json.dumps(block, sort_keys=True).encode()
       return hashlib.sha256(encoded_block).hexdigest()

   # check if the blockchain is valid
    def is_chain_valid(self, chain):
       # get the first block in the chain and it serves as the previous block
       previous_block = chain[0]
       # an index of the blocks in the chain for iteration
       block_index = 1
       while block_index < len(chain):
           # get the current block
           block = chain[block_index]
           # check if the current block link to previous block has is the same as the hash of the previous block
           if block["previous_hash"] != self.hash(previous_block):
               return False

           # get the previous proof from the previous block
           previous_proof = previous_block['proof']

           # get the current proof from the current block
           current_proof = block['proof']

           # run the proof data through the algorithm
           hash_operation = hashlib.sha256(
               str(current_proof ** 2 - previous_proof ** 2).encode()).hexdigest()
           # check if hash operation is invalid
           if hash_operation[:2] != '00':
               return False
           # set the previous block to the current block after running validation on current block
           previous_block = block
           block_index += 1
       return True

    def get_ipList(filename: str):
        ip_list = list()
        with open(filename, 'r') as ipfile:
            lines = ipfile.readlines()
            for line in lines:
                ip_list.append(line)
            ipfile.close()
            return ip_list

    def getChainIfAlreadyExist(self):
        for host in GetHostsAddress():
            try:
                response = requests.get(f'http://{host}:5000/get_chain').json()
                if len(response['chain']) > 1:
                    return response
            except:
                print("Host not reachable")
        return []

blockchain = Blockchain()