#!/usr/bin/env python3
import argparse
import sys
from testcase import Database, Item, RandomTestCase, DirectedTestCase, TestCase

def items_database(verbose):
    '''Populate and return the items database'''
    db = Database()
    db.items = Item('001', 'Rolex', 100, discount = {'unit': 3, 'price': 200}, verbose = verbose)
    db.items = Item('002', 'Michael Kors', 80, discount = {'unit': 2, 'price': 120}, verbose = verbose)
    db.items = Item('003', 'Swatch', 50, verbose = verbose)
    db.items = Item('004', 'Casio', 30, verbose = verbose)
    return db

def directed_tests(db, verbose):
    '''Create directed tests and run them'''
    return [
        DirectedTestCase(db, verbose=verbose, itemlist=[]),
        DirectedTestCase(db, verbose=verbose, itemlist=[]),
        DirectedTestCase(db, verbose=verbose, itemlist=['001']),
        DirectedTestCase(db, verbose=verbose, itemlist=['001', '001']),
        DirectedTestCase(db, verbose=verbose, itemlist=['001', '001', '001']),
        DirectedTestCase(db, verbose=verbose, itemlist=['001', '001', '001', '001']),
        DirectedTestCase(db, verbose=verbose, itemlist=['002']),
        DirectedTestCase(db, verbose=verbose, itemlist=['002', '002']),
        DirectedTestCase(db, verbose=verbose, itemlist=['002', '002', '002']),
        DirectedTestCase(db, verbose=verbose, itemlist=['002', '002', '002', '002']),
        DirectedTestCase(db, verbose=verbose, itemlist=['003']),
        DirectedTestCase(db, verbose=verbose, itemlist=['003', '003']),
        DirectedTestCase(db, verbose=verbose, itemlist=['003', '003', '003']),
        DirectedTestCase(db, verbose=verbose, itemlist=['003', '003', '003', '003']),
        DirectedTestCase(db, verbose=verbose, itemlist=['004']),
        DirectedTestCase(db, verbose=verbose, itemlist=['004', '004']),
        DirectedTestCase(db, verbose=verbose, itemlist=['004', '004', '004']),
        DirectedTestCase(db, verbose=verbose, itemlist=['004', '004', '004', '004']),
    ]

def random_tests(numtests, db, verbose=False):
    tests = []
    for i in range(numtests):
        tests.append(RandomTestCase(db, verbose))
    return tests

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
    print(args)

    database = items_database(args.verbose)
    # Run the tests
    if args.directed:
        tests = directed_tests(database, args.verbose)
    else:
        tests = random_tests(args.random, database, args.verbose)

    for test in tests:
        test.test()
    TestCase.results()