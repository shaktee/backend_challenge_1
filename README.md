# Backend challenge
This is an implementation of the backend challenge in multiple languages

## Backend languages used
1. Javascript (node.js) [README](nodejs/README.md)
2. Go [README](golang/README.md)

Each subdirectory has a README with instructions on how to start and use the server

## Test languages
1. Python [README](test/README.md)

## Running tests
To understand how to invoke the test, execute
```
./test/test.py --help
```
To directly run tests against each implementation, you may start the server (as stated in the README in the server directory) and then

1. Run random number of tests as shown below
```
./test/test.py --random <number of random tests>
```
2. Run directed tests as shown below
```
./test/test.py --directed
```
