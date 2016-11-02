--------------------------------------------------------------------------------  
DROP TABLE IF EXISTS persons;     
CREATE TABLE persons                     
(
pid INTEGER NOT NULL PRIMARY KEY,     -- person id
name VARCHAR,
sid INTEGER UNIQUE,                   -- student id
balance DECIMAL (5,2) DEFAULT 0,      -- SHOULD ONLY BE NUMBERS, DO NOT USE THE 'FEATURE' of strings, check this in python/js input!
usertype TINYINT                      -- 0: user, 1: admin
);
--------------------------------------------------------------------------------
DROP TABLE IF EXISTS keys;
CREATE TABLE keys
(
kid BLOB NOT NULL PRIMARY KEY,  -- hash rfid tag uid; BLOB = Binary Large OBject, maybe TEXT also acceptable?
keyname VARCHAR,
pid INTEGER,
CHECK(keyname <> ''),
FOREIGN KEY (pid) REFERENCES persons(pid) ON UPDATE CASCADE
); 


--------------------------------------------------------------------------------
--DROP TABLE IF EXISTS KPL;

--CREATE TABLE KPL 
--(
--kid INTEGER NOT NULL,                 -- key id
--pid INTEGER NOT NULL,                 -- person id
--PRIMARY KEY (kid,pid),
--FOREIGN KEY(kid) REFERENCES KEY(kid),
--FOREIGN KEY(pid) REFERENCEs person(pid)
--);
--------------------------------------------------------------------------------
DROP TABLE IF EXISTS categories;

CREATE TABLE categories
(
cid INTEGER PRIMARY KEY NOT NULL,     -- category id
name varchar
);
INSERT INTO categories VALUES(0, 'Drinks');
INSERT INTO categories VALUES(1, 'Food');
--------------------------------------------------------------------------------
DROP TABLE IF EXISTS items;

CREATE TABLE items
(
iid INTEGER PRIMARY KEY NOT NULL,     -- item id
item_name varchar,
stock INTEGER,                        --make db constraint that always above > -1?
current_price DECIMAL(5,2),           --is most likely just overkill for a snack system,
pic_url text,
cid INTEGER,                           --category ID
CHECK(pic_url <> ''),
FOREIGN KEY(cid) REFERENCES categories(cid)
);
INSERT INTO items VALUES(1,'Bueno',20,0.41,'xx', 1);
INSERT INTO items VALUES(2,'Bagel',25,2.41,'bagel.jpg', 1);
INSERT INTO items VALUES(3,'Fristi',10,1.41,'xx', 0);
--------------------------------------------------------------------------------
DROP TABLE IF EXISTS orders;

CREATE TABLE orders
(
oid INTEGER PRIMARY KEY NOT NULL,     -- basket ID
total DECIMAL(5,2),                   -- never directly accessed by user, should be safe
date datetime,                        -- in YYYY-MM-DD HH-MM-SS format
pid NOT NULL,                         -- person id
FOREIGN KEY(pid) REFERENCES persons(pid)
);
INSERT INTO orders VALUES (1,15.62,CURRENT_TIMESTAMP,2);
--------------------------------------------------------------------------------
DROP TABLE IF EXISTS orderitems;

Create TABLE orderitems
(
oid INTEGER NOT NULL,                 -- basket ID
iid INTEGER NOT NULL,                 -- Item ID
quantity INTEGER,                     -- amount of times this item
price DECIMAL(5,2),                   -- Price as found in system on time of Buying, singular price
PRIMARY KEY (oid,iid),
FOREIGN KEY(oid) REFERENCES orders(oid),
FOREIGN KEY (iid) REFERENCES items(iid)
)