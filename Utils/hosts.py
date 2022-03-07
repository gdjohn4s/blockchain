import requests
from config import PUBLIC_IP_API


def get_public_ip():
    print("Getting public IP")
    result = requests.get(PUBLIC_IP_API).json()
    return result['ip']


def GetHostsAddress():
    result = []
    with open("ip-chain.txt", 'r') as ipFile:
        lines = ipFile.readlines()
        for line in lines:
            result.append(line.replace('\n',''))
    return result


def connectHostToBlockchain():
    currentIpAddress = get_public_ip()
    hosts = GetHostsAddress()
    acceptedCounter = 0
    for host in hosts:
        try:
            response = requests.get(f'http://{host}:5000/mergeNewHost/{currentIpAddress}').json()
            if(response['reponse'] == 'true'):
               acceptedCounter += 1
        except:
            acceptedCounter += 0

    if len(hosts) / 2 <= acceptedCounter:
        return True
        
    return False
