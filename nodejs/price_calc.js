const db = require('./db.js')

module.exports = {
    /// Count the items in the query and create a dictionary with the item as key and count as value
    /// Input: query = sorted list of items from the POST
    /// Returns: a dictionary of items and counts
    count_items: (query) => {
        let results = {}
        for (let i = 0; i < query.length; ++i) {
            if (query[i] in results) {
                ++results[query[i]]
            } else {
                results[query[i]] = 1
            }
        }
        return results
    },

    /// Calculate the prices if the items based on the database values after applying discounts, if any
    /// Inputs: A dictionary of items and counts
    /// Returns: a calculated price
    calculated_price: (items) => {
        let price = 0
        for (var item in items) {
            if (item in db) {
                let quantity = items[item]
                let discount = db[item].discount
                if (discount !== undefined) {
                    price += Math.floor(quantity / discount.unit) * discount.price
                    price += (quantity % discount.unit) * db[item].price
                } else {
                    price += quantity * db[item].price
                }
            }
        }
        return price
    }
}
