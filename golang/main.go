package main

import (
	"encoding/json"
	"errors"
	"fmt"
	"log"
	"math"
	"net/http"
	"os"
	"sort"
)

// The discount, if any exists for an item
type Discount struct {
	Unit  int
	Price int
}

// The item
type Item struct {
	Id    string
	Name  string
	Price int
	Disc  *Discount
	Count int
}

// The items database
type Db struct {
	Items []Item
}

// The filled out database for use with the server
// This would ideally be retrieved from a backend database
// and populated
func GetDb() Db {
	return Db{
		Items: []Item{
			{
				Id:    "001",
				Name:  "Rolex",
				Price: 100,
				Disc:  &Discount{Unit: 3, Price: 200},
				Count: 0,
			},
			{
				Id:    "002",
				Name:  "Michael Kors",
				Price: 80,
				Disc:  &Discount{Unit: 2, Price: 120},
				Count: 0,
			},
			{
				Id:    "003",
				Name:  "Swatch",
				Price: 50,
				Count: 0,
			},
			{
				Id:    "004",
				Name:  "Casio",
				Price: 30,
				Count: 0,
			},
		},
	}
}

// The incoming query of item ids
type Query struct {
	ItemId []string
}

// The response structure
type PriceResponse struct {
	price int
}

// Sort helpers
type ByItemName []string

func (a ByItemName) Len() int           { return len(a) }
func (a ByItemName) Swap(i, j int)      { a[i], a[j] = a[j], a[i] }
func (a ByItemName) Less(i, j int) bool { return a[i] < a[j] }

// Take a query with a list of items and update the working
// database and return the updated database
func getUpdatedDatabase(q Query) Db {
	var db Db = GetDb()
	sort.Sort(ByItemName(q.ItemId))

	for j := 0; j < len(db.Items); j++ {
		newLength := 0
		for idx := range q.ItemId {
			// Count all the items in the incoming query
			if q.ItemId[idx] == db.Items[j].Id {
				// Increment the count in the working database
				db.Items[j].Count++
				// Remove the processed item from the query list to
				// make the subsequent loops shorter
				q.ItemId[newLength] = q.ItemId[idx]
				newLength++
			}
		}
	}
	return db
}

// Calculate the total price to be paid
// Input Working database with updated count of items
// Returns a price
func calculatePrice(db Db) int {
	var price int = 0
	for j := 0; j < len(db.Items); j++ {
		// check if there is a discount, and update the price
		count := db.Items[j].Count
		if db.Items[j].Disc != nil {
			units := int(math.Floor(float64(count / db.Items[j].Disc.Unit)))
			remaining := count % db.Items[j].Disc.Unit
			price += (units * db.Items[j].Disc.Price) + (remaining * db.Items[j].Price)
		} else {
			// otherwise, just compute the price by a stright multiplication
			price += (count * db.Items[j].Price)
		}
	}
	return price
}

// The main handler
// Receives a http request r
// Populates a http response w
func getCheckout(w http.ResponseWriter, r *http.Request) {
	log.Println(r.Body)
	decoder := json.NewDecoder(r.Body)
	var q Query
	err := decoder.Decode(&q.ItemId)
	if err == nil {
		log.Println(q.ItemId)
		var db = getUpdatedDatabase(q)
		var price = PriceResponse{price: calculatePrice(db)}

		// Respond with the price
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(fmt.Sprintf("{\"price\": %d}", price.price))
	} else {
		// The json decoded badly... respond with an error
		w.WriteHeader(http.StatusBadRequest)
		json.NewEncoder(w).Encode(fmt.Sprintf("{\"error\": \"Requires a valid list of items\"}"))
	}
}

// Main server entry point
func main() {
	http.HandleFunc("/checkout", getCheckout)

	err := http.ListenAndServe(":8080", nil)
	if errors.Is(err, http.ErrServerClosed) {
		fmt.Printf("server closed\n")
	} else if err != nil {
		fmt.Printf("error starting server: %s\n", err)
		os.Exit(1)
	}
}
