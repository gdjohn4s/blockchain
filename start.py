from pickle import TRUE
from flask import Flask
from flask_cors import CORS
from Models.blockchain import blockchain
from Controller.miningAPI import mining_api
from Controller.chainAPI import chain_api
from Controller.hostAPI import host_api
from Utils.hosts import *


app = Flask(__name__)
app.register_blueprint(mining_api)
app.register_blueprint(chain_api)
app.register_blueprint(host_api)


CORS(app)


if __name__ == "__main__":
   if connectHostToBlockchain():
      print(f"Hi {get_public_ip()}, welcome to the PippoChain!")
      otherHostChain = blockchain.getChainIfAlreadyExist()
      if len(otherHostChain) > 1:
         blockchain.chain = otherHostChain['chain']
   else:
      print(f"You are the first node")

   app.run(host="0.0.0.0", port=5000)
