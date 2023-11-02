import meraki
import json
import requests
from env import API_KEY, ORG_ID, SG_HQ, TE_BEARER, TE_EMAIL, HQ_MR_SN

# BASE_URL = "https://api.meraki.com/api/v1/"
BASE_URL = "https://api.thousandeyes.com/v6/"
HEADER = {"Authorization": "Bearer " + TE_BEARER}

# clients = {}


def getNetworkClients(dashboard):
    
    response = dashboard.networks.getNetworkClients(SG_HQ, total_pages=all)
    # print(json.dumps(response, indent=2))
    
    my_clients = []
    
    for client in response:
        my_clients.append({"id" : client["id"], "mac" : client["mac"], "description" : client["description"], "ip" : client["ip"], "user" : client["user"]})
    
    return my_clients


def getNetworkClientsApplicationUsage(dashboard, clients, t0, t1):

    response = dashboard.networks.getNetworkClientsApplicationUsage(
        SG_HQ, clients, t0=t0, t1=t1
    )
    return response


def getNetworkClientTrafficHistory(dashboard, clients, t0, t1):

    response = dashboard.networks.getNetworkClientTrafficHistory(
        SG_HQ, clients, total_pages='all', t0=t0, t1=t1
    )
    return response


def getTEtests():

    response = requests.get(BASE_URL+"tests.json", headers=HEADER)
    print(response.status_code)
    print(json.dumps(response.json(), indent=2))


def getNetworkWirelessSignalQualityHistory(dashboard):
    
    response = dashboard.wireless.getNetworkWirelessSignalQualityHistory(networkId=SG_HQ, deviceSerial=HQ_MR_SN)
    print(json.dumps(response, indent=2))


if __name__ == "__main__":
    print("Hello... \n Welcome to Metheia \n I will help you understand your network health")
    print("First let's check your Meraki API connectivity...")

    dashboard = meraki.DashboardAPI(API_KEY)
    # print(dashboard)
    
    response = dashboard.organizations.getOrganization(ORG_ID)
    print("API Established with {} : {}".format(response["name"], response["id"]))

    # print("Let's check ThousandEyes API connectivity...")
    # response = requests.get(BASE_URL+"status", headers=HEADER)
    # print(response.status_code)

    # getTEtests()

    # getNetworkWirelessSignalQualityHistory(dashboard)

    my_clients = getNetworkClients(dashboard)
    print(my_clients)

    for client in my_clients:
        if client["description"] == "Uross-iPhone":
            print (client["id"])

    clients = "k8508ec"
    t0 = "2023-10-07T07:00:00.0000"
    t1 = "2023-10-08T19:00:00.0000"

    print(json.dumps(getNetworkClientsApplicationUsage(dashboard=dashboard, clients=clients, t0=t0, t1=t1), indent=2))
    
    traffic = getNetworkClientTrafficHistory(dashboard=dashboard, clients=clients, t0=t0, t1=t1)
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(traffic, f, ensure_ascii=False, indent=4)