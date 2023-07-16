from abc import ABC, abstractmethod
import collections
import http.client
import json
import random

class Database:
    """The database"""
    def __init__(self):
        self.itemsdict = {}
        pass

    @property
    def items(self):
        return self.itemsdict.keys()
    
    @items.setter
    def items(self, item):
        if item in self.itemsdict:
            raise Exception(f'Item {item.key} already exists in database!')
        self.itemsdict[item.key] = item

    def get_item(self, key):
        if key in self.itemsdict:
            return self.itemsdict[key]
        return None

class Item:
    """The item"""
    def __init__(self, key, name, price, discount=None, verbose=False):
        self.key = key
        self.name = name
        self.price = price
        self.discount = discount
        self.verbose = verbose

    def calculate_price(self, count):
        price = 0
        if self.discount:
            discount_quantity = count // self.discount['unit']
            remaining = count % self.discount['unit']
            disc_price = discount_quantity * self.discount['price']
            price += disc_price
            rem_price = remaining * self.price
            price += rem_price
            if self.verbose:
                print(f'''   Discounted price of     {self.name:12s}: {discount_quantity:3d} x {self.discount['price']:4d} = {disc_price:5d}''')
                print(f'''   Non-discounted price of {self.name:12s}: {remaining:3d} x {self.price:4d} = {rem_price:5d}''')
        else:
            item_price = count * self.price
            price += item_price
            if self.verbose:
                print(f'''   Non-discounted price of {self.name:12s}: {count:3d} x {self.price:4d} = {item_price:5d}''')
        return price

class TestCase(ABC):
    """The test case"""
    __testcase = 0
    __pass = 0
    __fail = 0
    def __init__(self, database, verbose=False, itemlist=[]):
        self.testcase = TestCase.__testcase
        TestCase.__testcase += 1
        self.itemlist = itemlist
        self.db = database
        self.verbose = verbose
    
    def get_items(self):
        return self.itemlist

    def calculate_price(self):
        counts = collections.Counter(self.itemlist)
        price = 0
        for key in counts:
            item = self.db.get_item(key)
            if item:
                price += item.calculate_price(counts[key])
        return price

    def check_result(self, expected, resp):
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
            if self.verbose:
                print(f'Test: {self.testcase} Received {output}')

            if output['price'] == expected['price']:
                print(f'{self.testcase}: HTTP/{resp[1]} PASS')
                success = True
            else:
                print(f'{self.testcase}: HTTP/{resp[1]} FAIL.')
                print(f'''   Expected {expected}''')
                print(f'   Received {output}')
        else:
            print(f'{self.testcase}: HTTP/{resp[1]} FAIL')
        return success
    
    def get_result(self):
        '''send data and receive response'''
        conn = http.client.HTTPConnection("localhost", 8080)
        params = json.dumps(self.itemlist)
        headers = {"Content-type": "application/json", "Accept": "application/json"}
        conn.request("POST","/checkout", params, headers)
        response = conn.getresponse()
        return (response.status, response.reason, response.read())

    def test(self):
        '''Run the test case'''
        res = self.get_result()
        expected = {'price': self.calculate_price()}
        ret = self.check_result(expected, res)
        if ret:
            TestCase.__pass += 1
        else:
            TestCase.__fail += 1

    @classmethod
    def results(cls):
        print(f'PASS {TestCase.__pass}/{TestCase.__testcase}, FAIL {TestCase.__fail}/{TestCase.__testcase}')

class RandomTestCase(TestCase):
    '''The Random test case'''
    def __init__(self, database, verbose=False, itemlist=[]):
        numitems = random.randrange(20)
        itemlist = []
        for i in range(numitems):
            item = random.choice(list(database.items))
            itemlist.append(item)
        if verbose:
            print(f'   Items: {itemlist}')
        super().__init__(database, verbose, itemlist)


class DirectedTestCase(TestCase):
    '''The directed test case'''