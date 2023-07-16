package db

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
