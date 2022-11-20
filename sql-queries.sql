CREATE TABLE "Customer" (
	id INTEGER NOT NULL,
	name TEXT NOT NULL,
	phoneno	TEXT NOT NULL UNIQUE,
	totalbill INTEGER DEFAULT 0,
	PRIMARY KEY(id AUTOINCREMENT)
);

CREATE TABLE Reservation (
	id INTEGER,
	roomno INTEGER PRIMARY KEY AUTOINCREMENT,
	arrivaldate TEXT,
	departuredate TEXT,
	FOREIGN KEY(id) REFERENCES Customer(id)
);

CREATE TABLE Restaurant (
	id INTEGER NOT NULL,
	fooditem TEXT,
	cost INTEGER,
	PRIMARY KEY(id)
);

INSERT INTO Restaurant VALUES (1, "Veg Pizza", 10);
INSERT INTO Restaurant VALUES (2, "Chicken Pizza", 30);
INSERT INTO Restaurant VALUES (3, "Panneer Pizza", 20);
INSERT INTO Restaurant VALUES (4, "Butter Pizza", 20);
INSERT INTO Restaurant VALUES (5, "Veg Burger", 10);

CREATE TABLE Service (
	id INTEGER NOT NULL,
	servicename TEXT,
	cost INTEGER,
	PRIMARY KEY(id)
);

INSERT INTO Service VALUES (1, "Spa", 20);
INSERT INTO Service VALUES (2, "Laundry", 30);
INSERT INTO Service VALUES (3, "Rentals", 20);


