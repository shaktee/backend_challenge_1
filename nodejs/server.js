const express = require('express')
const bodyParser = require('body-parser')
const app = express()
const port = 8080
const priceCalc = require('./price_calc.js')

app.use(bodyParser.json())

// Return an error when / is called with a GET or a POST
const errfunc = (req, res) => {
    res.statusMessage = "Sorry, this is a checkout server. POST to /checkout";
    res.status(501).end()
}

app.get('/', errfunc)
app.post('/', errfunc)

/// Main endpoint
app.post('/checkout', (req, res) => {
    'use strict';
    let query = req.body;
    let result = {"price": 0}
    /// Make sure the JSON 
    if (Array.isArray(query)) {
        query.sort() /// Purely an optimization
        let items = priceCalc.count_items(query)
        result.price = priceCalc.calculated_price(items)
        res.json(result)
    } else {
        res.status(500).json(`{Error: "Invalid input. Requires a list of valid items"}`)
    }
})

app.listen(port, () => {
    console.log(`Checkout app listening on port ${port}`)
})