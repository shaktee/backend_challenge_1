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

type PriceResponse struct {
	price int
}

type Discount struct {
	Unit  int
	Price int
}

type Item struct {
	Key   string
	Name  string
	Price int
	Disc  *Discount
}

type Db struct {
	Items []Item
}

func GetDb() Db {
	return Db{
		Items: []Item{
			{
				Key:   "001",
				Name:  "Rolex",
				Price: 100,
				Disc:  &Discount{Unit: 3, Price: 200},
			},
			{
				Key:   "002",
				Name:  "Michael Kors",
				Price: 80,
				Disc:  &Discount{Unit: 2, Price: 120},
			},
			{
				Key:   "003",
				Name:  "Swatch",
				Price: 50,
			},
			{
				Key:   "004",
				Name:  "Casio",
				Price: 30,
			},
		},
	}
}

type Query struct {
	Item []string
}

type ByItem []string

func (a ByItem) Len() int           { return len(a) }
func (a ByItem) Swap(i, j int)      { a[i], a[j] = a[j], a[i] }
func (a ByItem) Less(i, j int) bool { return a[i] < a[j] }

func calculatePrice(q Query) int {
	var d Db = GetDb()
	var price int = 0
	sort.Sort(ByItem(q.Item))

	for j := 0; j < len(d.Items); j++ {
		var count int = 0
		newLength := 0
		for idx := range q.Item {
			// Count all the items in the incoming query
			if q.Item[idx] == d.Items[j].Key {
				count++
				q.Item[newLength] = q.Item[idx]
				newLength++
			}
		}
		// check if there is a discount, and update the price
		if d.Items[j].Disc != nil {
			units := int(math.Floor(float64(count / d.Items[j].Disc.Unit)))
			remaining := count % d.Items[j].Disc.Unit
			price += (units * d.Items[j].Disc.Price) + (remaining * d.Items[j].Price)
		} else {
			price += (count * d.Items[j].Price)
		}
	}
	return price
}

func getCheckout(w http.ResponseWriter, r *http.Request) {
	log.Println(r.Body)
	decoder := json.NewDecoder(r.Body)
	var t Query
	err := decoder.Decode(&t.Item)
	if err != nil {
		panic(err)
	}
	log.Println(t.Item)
	var price = PriceResponse{price: calculatePrice(t)}

	// io.WriteString(w, fmt.Sprintf("Price is %d!\n", price))
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(fmt.Sprintf("{\"price\": %d}", price.price))
}

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
