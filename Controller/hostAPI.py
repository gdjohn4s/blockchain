from flask import jsonify
from flask import Blueprint

host_api = Blueprint('host_api', __name__)

@host_api.route('/mergeNewHost/<newAdress>', methods=['GET'])
def mergeNewHost(newAdress):
   with open("ip-chain.txt", 'r+') as ipFile:
      if newAdress in ipFile.read():
            return jsonify({'reponse': 'true'}), 200
      try:
            ipFile.write(f"\n{newAdress}")
            return jsonify({'reponse': 'true'}), 200
      except:
            return jsonify({'reponse': 'false'}), 500