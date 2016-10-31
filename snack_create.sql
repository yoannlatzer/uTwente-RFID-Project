--------------------------------------------------------------------------------;
DROP TABLE IF EXISTS key;
CREATE TABLE key
(
kid INTEGER NOT NULL PRIMARY KEY, -- key id
keyhash BLOB   --? sha3_512 hash rfid tag uid
); 

--------------------------------------------------------------------------------;
DROP TABLE IF EXISTS person;     
CREATE TABLE person                     
(
pid INTEGER NOT NULL PRIMARY KEY, -- person id
name VARCHAR,
sid INTEGER UNIQUE, -- student id
usertype TINYINT -- 0: user, 1: admin
);
--------------------------------------------------------------------------------;
DROP TABLE IF EXISTS KPL;

CREATE TABLE KPL 
(
kid INTEGER NOT NULL, -- key id
pid INTEGER NOT NULL, -- person id
PRIMARY KEY (kid,pid),
FOREIGN KEY(kid) REFERENCES KEY(kid),
FOREIGN KEY(pid) REFERENCEs person(pid)
);
--------------------------------------------------------------------------------

DROP TABLE IF EXISTS items;

CREATE TABLE items
(
iid INTEGER PRIMARY KEY NOT NULL, -- item id
item_name varchar,
stock INTEGER,  --make db constraint that always above > -1?,
cprice DECIMAL(5,2), --is most likely just overkill for a snack system,
pic varchar   -- currently of no use due to non-GUI enviroment
CHECK(PIC <> '')
);
INSERT INTO items VALUES(1,'Bueno',20,0.41,Null);

--------------------------------------------------------------------------------
DROP TABLE IF EXISTS basket;

CREATE TABLE basket
(
bid INTEGER PRIMARY KEY NOT NULL,
total DECIMAL(5,2),
date datetime,
pid NOT NULL,
FOREIGN KEY(pid) REFERENCES person(pid)
);
INSERT INTO basket VALUES (1,15.62,CURRENT_TIMESTAMP,2);
--------------------------------------------------------------------------------
DROP TABLE IF EXISTS transactions;

Create TABLE transactions
(
bid INTEGER NOT NULL,
iid INTEGER NOT NULL,
quantity INTEGER,
price DECIMAL(5,2),
PRIMARY KEY (bid,iid),
FOREIGN KEY(bid) REFERENCES basket(bid),
FOREIGN KEY (iid) REFERENCES items(iid)
)