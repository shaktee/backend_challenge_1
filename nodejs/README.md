# Backend Coding Challenge
This is the node js implementation of the coding challenge.

## Setup
1. Install `npm` using your package manager
2. Optionally install `nodemon` (helps in restarting the server automatically)
3. Install the packages required for this server by executing
   `npm install`

## Starting the server
4. Start using `npm start` or `nodemon server.js`
```
% nodemon server.js
[nodemon] 3.0.1
[nodemon] to restart at any time, enter `rs`
[nodemon] watching path(s): *.*
[nodemon] watching extensions: js,mjs,cjs,json
[nodemon] starting `node server.js`
Checkout app listening on port 8080
```

## Running the test
### Using CURL
### Success cases
```
curl  -X POST http://localhost:8080/checkout   -H 'Content-Type: application/json'   -d '[]'
{"price":0}%                          

 curl  -X POST http://localhost:8080/checkout   -H 'Content-Type: application/json'   -d '["002","002","001","001","001","003"]'
{"price":370}%                                                                                                                      
rajeshvaidheeswarran@Rajeshs-MBP nodejs % curl  -X POST http://localhost:8080/checkout   -H 'Content-Type: application/json'   -d '["002","002","001","001","001","003","001"]'
{"price":470}%                                                                                                                      
rajeshvaidheeswarran@Rajeshs-MBP nodejs % curl  -X POST http://localhost:8080/checkout   -H 'Content-Type: application/json'   -d '["002","002","001","001","001","003","001","001"]'
{"price":570}%                                                                                                                      
rajeshvaidheeswarran@Rajeshs-MBP nodejs % curl  -X POST http://localhost:8080/checkout   -H 'Content-Type: application/json'   -d '["002","002","001","001","001","003","001","001","001"]'
{"price":570}%                                   
```
### Error cases
```
% curl  -X POST http://localhost:8080/checkout   -H 'Content-Type: application/json'   -d '{}'
"{Error: \"Invalid input. Requires a list of valid items\"}"
%
```