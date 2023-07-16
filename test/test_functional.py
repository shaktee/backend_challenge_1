#!/usr/bin/env python3
import argparse
import http.client
import json
import threading
import os
import subprocess
import sys
import time
import urllib.parse
import random
import collections

VERBOSE = False

DB = {
    "001": {
        "name": "Rolex",
        "price": 100,
        "discount": {"unit": 3, "price": 200}
    },
    "002": {
        "name": "Michael Kors",
        "price": 80,
        "discount": {"unit": 2, "price": 120}
    },
    "003": {
        "name": "Swatch",
        "price": 50
    },
    "004": {
        "name": "Casio",
        "price": 30
    }
}

def random_tests(numtests):
    '''Run random tests'''
    def get_items():
        '''get items for a random test'''
        numitems = random.randrange(100)
        items = []
        keys = list(DB.keys())
        for i in range(numitems):
            item = random.choice(keys)
            items.append(item)
        if VERBOSE:
            print(f'   Items: {items}')
        return items
    
    def get_expected_output(items):
        '''Get expected output from the server'''
        counts = collections.Counter(items)
        price = 0
        if VERBOSE:
            print(f'   Count of Items: {counts}')
        for item in sorted(counts):
            if item in DB:
                if 'discount' in DB[item]:
                    discount_quantity = counts[item] // DB[item]['discount']['unit']
                    remaining = counts[item] % DB[item]['discount']['unit']
                    disc_price = discount_quantity * DB[item]['discount']['price']
                    price += disc_price
                    rem_price = remaining * DB[item]['price']
                    price += rem_price
                    if VERBOSE:
                        print(f'''   Discounted price of     {item}: {discount_quantity:3d} x {DB[item]['discount']['price']:4d} = {disc_price:5d}''')
                        print(f'''   Non-discounted price of {item}: {remaining:3d} x {DB[item]['price']:4d} = {rem_price:5d}''')
                else:
                    item_price = counts[item] * DB[item]['price']
                    price += item_price
                    if VERBOSE:
                        print(f'''   Non-discounted price of {item}: {counts[item]:3d} x {DB[item]['price']:4d} = {item_price:5d}''')

        return {'price': price}

    success = 0
    fails = 0
    for i in range(numtests):
        items = get_items()
        expected = get_expected_output(items)
        resp = get_result(items)
        ret = check_result(i, expected, resp)
        if ret:
            success += 1
        else:
            fails += 1
    print(f'PASS {success}/{numtests}; FAIL {fails}/{numtests}')

def directed_tests():
    '''Directed test list'''
    tests = [
        {'data': [], 'resp': '{"price": 0}'},
        {'data': ['001'], 'resp': '{"price": 100}'},
        {'data': ['001', '001'], 'resp': '{"price": 200}'},
        {'data': ['001', '001', '001'], 'resp': '{"price": 200}'},
        {'data': ['001', '001', '001', '001'], 'resp': '{"price": 300}'},
        {'data': ['002'], 'resp': '{"price": 80}'},
        {'data': ['002', '002'], 'resp': '{"price": 120}'},
        {'data': ['002', '002', '002'], 'resp': '{"price": 200}'},
        {'data': ['002', '002', '002', '002'], 'resp': '{"price": 240}'},
        {'data': ['003'], 'resp': '{"price": 50}'},
        {'data': ['003', '003'], 'resp': '{"price": 100}'},
        {'data': ['003', '003', '003'], 'resp': '{"price": 150}'},
        {'data': ['003', '003', '003', '003'], 'resp': '{"price": 200}'},
        {'data': ['004'], 'resp': '{"price": 30}'},
        {'data': ['004', '004'], 'resp': '{"price": 60}'},
        {'data': ['004', '004', '004'], 'resp': '{"price": 90}'},
        {'data': ['004', '004', '004', '004'], 'resp': '{"price": 120}'},
    ]

    t = 0
    success = 0
    fails = 0
    for test in tests:
        resp = get_result(test['data'])
        expected = json.loads(test['resp'])
        if VERBOSE:
            print(f'Test: {t} Expecting {expected}')
        ret = check_result(t, expected, resp)
        t += 1
        if ret:
            success += 1
        else:
            fails += 1
    print(f'PASS {success}/{t}; FAIL {fails}/{t}')

def check_result(t, expected, resp):
    '''Check the actual result vs expected'''
    success = False
    if resp[0] == 200:
        if type(resp[2]) == bytes:
            output = json.loads(resp[2].decode('utf-8'))
        else:
            output = json.loads(resp[2])
        # Some servers return a byte stream and that decodes to a string
        # which needs further decode to a json object
        if type(output) == str:
            output = json.loads(output)
        if VERBOSE:
            print(f'Test: {t} Received {output}')

        if output['price'] == expected['price']:
            print(f'{t}: HTTP/{resp[1]} PASS')
            success = True
        else:
            print(f'{t}: HTTP/{resp[1]} FAIL.')
            print(f'''   Expected {expected}''')
            print(f'   Received {output}')
    else:
        print(f'{t}: HTTP/{resp[1]} FAIL')
    return success

def get_result(data):
    '''send data and receive response'''
    conn = http.client.HTTPConnection("localhost", 8080)
    params = json.dumps(data)
    headers = {"Content-type": "application/json", "Accept": "application/json"}
    conn.request("POST","/checkout", params, headers)
    response = conn.getresponse()
    return (response.status, response.reason, response.read())

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog=sys.argv[0],
                    description='Test backend servers',
                    epilog='''Let's go!''')
    parser.add_argument('-v', '--verbose', action='store_true', help="Be verbose")

    tests = parser.add_argument_group('tests')
    tests.add_argument('--directed', action='store_true', help="Run directed tests", default=False)
    tests.add_argument('--random', type=int, action='store', help="Number of tests to run", default=10)

    args = parser.parse_args(sys.argv[1:])
    VERBOSE = args.verbose
    print(args)

    # Run the tests
    if args.directed:
        directed_tests()
    else:
        random_tests(args.random)