import uuid
import logging
from flask import Flask, json, jsonify

def Items():
    return [
        {'id': '36d05424-1afb-4ed7-ac28-f37ec34e9772', 'name': 'Sony Playstation 4', 'price': 131.01}, 
        {'id': 'bb124d3b-09e0-4c8d-a141-7a37c73fd140', 'name': 'Headphones', 'price': 119.08}, 
        {'id': '6362345b-f8ab-4beb-84a5-96928c276634', 'name': 'Wireless Mouse', 'price': 134.12}, 
        {'id': 'd82fc7a4-6d72-4123-8917-ce0c20bfc979', 'name': 'Nintendo Switch', 'price': 6.4}, 
        {'id': '4bab29f3-db0c-4ea2-8f39-f43292a129c0', 'name': 'iPhone 7 Plus', 'price': 64.4}, 
        {'id': '86d788a9-2f1c-4789-ab00-24c6ca2667cb', 'name': 'Galaxy S9 Edge', 'price': 47.76}, 
        {'id': '6f6f79a7-a0d0-4c63-8b78-5ebb7d3635b7', 'name': 'Laptop', 'price': 210.37}, 
        {'id': 'e264176b-151a-45cf-b610-7cc285ea511e', 'name': 'Chair', 'price': 378.46}, 
        {'id': 'f2bbb853-d427-4a85-a661-7ce77213e543', 'name': 'Trumpet', 'price': 282.24}, 
        {'id': 'a29a4bc4-1c88-426e-8e71-cf821d60aeaa', 'name': 'Plate', 'price': 8.73}, 
        {'id': '752231a6-1af2-469d-9db6-9a0fde938cac', 'name': 'Mug', 'price': 402.51}, 
        {'id': '918798ad-ca7d-4032-8bf0-f6f8f1490ea7', 'name': 'Door', 'price': 283.64}, 
        {'id': '78704947-199c-4ce6-8a04-4ec35e92d5f7', 'name': 'Original Van Gogh', 'price': 33.92}, 
        {'id': 'abb00183-644f-4921-8fc9-d8459abae449', 'name': 'Candle', 'price': 99.06}
    ]


def Addresses():
    return [
        {'id': '592beaa6-00a4-4c46-b3e3-8d103ebd749a', 'addressLineOne': 'Bath and North East Somerset', 'addressLineTwo': 'Icantbearsedtomakeupmoredatatown', 'country': 'United Kingdom', 'streetNameAndNumber': '19 Madaline Harbors', 'postcode': 'DT2 9HZ'},
        {'id': '2b5f2a53-fd19-492f-9680-d70d8ca4233d', 'addressLineOne': 'Bath and North East Somerset', 'addressLineTwo': 'Geoffreystown', 'country': 'United Kingdom', 'streetNameAndNumber': '1 Madaline Harbors', 'postcode': 'DT2 9HZ'},
        {'id': '7fd9d4d0-3326-419b-8890-9c456c5cf5c5', 'addressLineOne': 'Bedfordshire', 'addressLineTwo': 'Junstown', 'country': 'United Kingdom', 'streetNameAndNumber': '9 Madaline Harbors', 'postcode': 'DT2 9HA'},
        {'id': '7218088f-7d69-4090-85be-5f373996fe94', 'addressLineOne': 'Bedford', 'addressLineTwo':'Wiktorstown', 'country': 'United Kingdom', 'streetNameAndNumber': '89 Madaline Harbors', 'postcode': 'DT2 9HG'},
        {'id': '737952e3-020f-4e1a-a23f-e7c41c81b41c', 'addressLineOne': 'Berkshire', 'addressLineTwo': 'Nabeelstown', 'country': 'United Kingdom', 'streetNameAndNumber': '42 Madaline Harbors', 'postcode': 'DT2 9HH'},
        {'id': '56a2372d-4ae8-4a75-94cc-ed36e62d3b00', 'addressLineOne': 'Blackburn with Darwen', 'addressLineTwo': 'Trixiestown', 'country': 'United Kingdom', 'streetNameAndNumber': '39 Madaline Harbors', 'postcode': 'DT2 9LZ'},
        {'id': '8d673180-959b-44bb-b239-d7c42e3188cb', 'addressLineOne': 'Blackpool', 'addressLineTwo': 'Evangelinestown', 'country': 'United Kingdom', 'streetNameAndNumber': '11 Madaline Harbors', 'postcode': 'DT2 9DZ'},
        {'id': '8bdfc433-45a1-454a-ab96-ef6e36cf23e5', 'addressLineOne': 'Bournemouth, Christchurch and Poole', 'addressLineTwo': 'Arunstown', 'country': 'United Kingdom', 'streetNameAndNumber': '74 Madaline Harbors', 'postcode': 'DT2 9GZ'},
        {'id': 'a325b858-fc67-4865-bceb-f3d96f98a55a', 'addressLineOne': 'Bournemouth', 'addressLineTwo': 'Serenastown', 'country': 'United Kingdom', 'streetNameAndNumber': '79 Madaline Harbors','postcode': 'DT2 5DS'},
        {'id': 'd2d11ed0-b1f1-4a19-aa56-da0f74ff8ded', 'addressLineOne': 'Brighton and Hove', 'addressLineTwo': 'Franciscostown', 'country': 'United Kingdom', 'streetNameAndNumber': '75 Madaline Harbors', 'postcode': 'DT2 9DH'},
        {'id': '0a1b64b2-f411-45e5-868e-1f30c9b5439c', 'addressLineOne': 'Bristol', 'addressLineTwo': 'Jaidonstown', 'country': 'United Kingdom', 'streetNameAndNumber': '3 Madaline Harbors', 'postcode': 'DT2 9HQ'}
    ]

def Users():
    return [
        {'id': '4c8e3056-b6f8-4fe3-b1f7-090930056d38', 'name': 'Roscoe Pike', 'email': 'RoscoePike@hotmail.com'},
        {'id': '95c3dd8b-00d3-4eec-a471-42d6506b04b9', 'name': 'Geoffrey Noel', 'email': 'GeoffreyNoel@hotmail.com'},
        {'id': 'be708ef2-9432-45d1-ab36-86e7fd743414', 'name': 'Jun Christian', 'email': 'JunChristian@hotmail.com'},
        {'id': '284be557-8157-42fb-bfa6-54ed6dfa2efc', 'name': 'Wiktor Corona', 'email': 'WiktorCorona@hotmail.com'},
        {'id': '67e28298-f2d4-4966-b985-bbbd0d9e5d43', 'name': 'Nabeel Fellows', 'email': 'NabeelFellows@hotmail.com'},
        {'id': '9ed3c699-d9f4-4a15-ac43-bf18bca27f0b', 'name': 'Trixie Black', 'email': 'TrixieBlack@hotmail.com'},
        {'id': '658558cc-b905-4af2-9994-a2ea84575dc8', 'name': 'Evangeline Willis', 'email': 'EvangelineWillis@hotmail.com'},
        {'id': 'c5899028-2448-4c7c-b404-0e372e4a832c', 'name': 'Arun Stubbs', 'email': 'ArunStubbs@hotmail.com'},
        {'id': '834f1a58-8180-4e0c-90b5-4ca2b4723043', 'name': 'Serena Carlson', 'email': 'SerenaCarlson@hotmail.com'},
        {'id': 'dec16e70-8f75-47e6-9aeb-9fc6de1f1041', 'name': 'Francisco Shannon', 'email': 'FranciscoShannon@hotmail.com'},
        {'id': '0e862ec6-030d-438f-bbf7-3f050bfa27b8', 'name': 'Jaidon Plant', 'email': 'JaidonPlant@hotmail.com'}
    ]

def generateOrders():
    orders = []
    numItems = 1
    itemIndex = 0
    items = Items()
    users = Users()
    addresses = Addresses()
    for i in range(len(users)):
        selectedItems = []
        for i in range(numItems):
            selectedItems.append(items[itemIndex])
            itemIndex += 1
        orders.append({
            "id" : uuid.uuid4(),
            "user" : users[i],
            "address" : addresses[i],
            "items" : selectedItems
        })
        
        numItems += 1
        if numItems == 4:
            numItems = 1
        if itemIndex > len(items) - 2:
            itemIndex = 0
    return orders

def runWebay(host, port, logLevel=logging.INFO, debug=False):
    app = Flask(__name__)
    app.logger.setLevel(logLevel)
    
    @app.route('/orders')
    def orderRoute():
        orders = generateOrders()
        return jsonify(orders)

    @app.route('/listings')
    def itemRoute():
        return jsonify(Items())
    
    app.debug = False
    app.run(host=host, port=port)   

if __name__ == '__main__':
    runWebay("127.0.0.1", 5000, debug=True)