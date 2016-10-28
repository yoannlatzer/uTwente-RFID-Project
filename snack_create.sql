--------------------------------------------------------------------------------;
DROP TABLE IF EXISTS key;
CREATE TABLE key
(
kid INTEGER NOT NULL PRIMARY KEY, 
keyhash BLOB   --?
); 
INSERT INTO key VALUES(3,'xyz');

--------------------------------------------------------------------------------;
DROP TABLE IF EXISTS person;     
CREATE TABLE person                     
(
PID INTEGER NOT NULL PRIMARY KEY,
name VARCHAR,
sid INTEGER,
usertype TINYINT
);
INSERT INTO person VALUES(2,'Henk',1234567,1);
--------------------------------------------------------------------------------;  
DROP TABLE IF EXISTS KPL;

CREATE TABLE KPL 
(
kid INTEGER NOT NULL,
pid INTEGER NOT NULL,
PRIMARY KEY (kid,pid),
FOREIGN KEY(kid) REFERENCES KEY(kid),
FOREIGN KEY(pid) REFERENCEs person(pid)
) ;
INSERT INTO KPL VALUES(3,2);
--------------------------------------------------------------------------------

DROP TABLE IF EXISTS items;

CREATE TABLE items
(
iid INTEGER PRIMARY KEY NOT NULL,
item_name varchar,
stock INTEGER,  --make db constraint that always above > -1?,
cprice DECIMAL(5,2), --is most likely just overkill for a snack system,
PIC varchar   -- currently of no use due to non-GUI enviroment
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
DROP TABLE IF EXISTS transacties;

Create TABLE transacties
(
bid INTEGER NOT NULL,
iid INTEGER NOT NULL,
quantity INTEGER,
price DECIMAL(5,2),
FOREIGN KEY(bid) REFERENCES basket(bid),
FOREIGN KEY (iid) REFERENCES items(iid)
)