BEGIN TRANSACTION;
CREATE TABLE KPL 
(
kid INTEGER NOT NULL,                 -- key id
pid INTEGER NOT NULL,                 -- person id
PRIMARY KEY (kid,pid),
FOREIGN KEY(kid) REFERENCES KEY(kid),
FOREIGN KEY(pid) REFERENCEs person(pid)
);
INSERT INTO "KPL" VALUES(1,1);
INSERT INTO "KPL" VALUES(2,2);
CREATE TABLE basket
(
bid INTEGER PRIMARY KEY NOT NULL,     -- basket ID
total DECIMAL(5,2),                   -- never directly accessed by user, should be safe
date datetime,                        -- in YYYY-MM-DD HH-MM-SS format
pid NOT NULL,                         -- person id
FOREIGN KEY(pid) REFERENCES person(pid)
);
INSERT INTO "basket" VALUES(1,15.62,'2016-11-01 13:37:33',2);
CREATE TABLE categories
(
cid INTEGER PRIMARY KEY NOT NULL,     -- category id
name varchar
);
INSERT INTO "categories" VALUES(0,'Drinks');
INSERT INTO "categories" VALUES(1,'Food');
INSERT INTO "categories" VALUES(2,'Snacks');
CREATE TABLE items
(
iid INTEGER PRIMARY KEY NOT NULL,     -- item id
item_name varchar,
stock INTEGER,                        --make db constraint that always above > -1?
current_price DECIMAL(5,2),           --is most likely just overkill for a snack system,
pic_url text,
cid INTEGER,                           --category ID
FOREIGN KEY(cid) REFERENCES categories(cid)
);
INSERT INTO "items" VALUES(1,'Bueno',10,0.54,'bueno.png',2);
INSERT INTO "items" VALUES(2,'Bastogne',10,0.54,'snacks/bastogne.png',2);
INSERT INTO "items" VALUES(3,'Chips',10,0.54,'snacks/chips.png',2);
INSERT INTO "items" VALUES(4,'Gevulde Koek',10,0.54,'snacks/Gevulde-koek.png',2);
INSERT INTO "items" VALUES(5,'Kinder',10,0.54,'snacks/kinder.png',2);
INSERT INTO "items" VALUES(6,'Liga',10,0.54,'snacks/liga.png',2);
INSERT INTO "items" VALUES(7,'M&M''s',10,0.54,'snacks/m&m.png',2);
INSERT INTO "items" VALUES(8,'Maltesers',10,0.54,'snacks/maltesers.png',2);
INSERT INTO "items" VALUES(9,'Mars',10,0.54,'snacks/mars.png',2);
INSERT INTO "items" VALUES(10,'Milky Way',10,0.54,'snacks/milky-way.png',2);
INSERT INTO "items" VALUES(11,'Oreo',10,0.54,'snacks/oreo.png',2);
INSERT INTO "items" VALUES(12,'Snickers',10,0.54,'snacks/snickers.png',2);
INSERT INTO "items" VALUES(13,'Sultana',10,0.54,'snacks/sultana.png',2);
INSERT INTO "items" VALUES(14,'Timeout',10,0.54,'snacks/timeout.png',2);
INSERT INTO "items" VALUES(15,'Timeout Granen',10,0.54,'snacks/timeout_granen.png',2);
INSERT INTO "items" VALUES(16,'Tuc',10,0.54,'snacks/tuc.png',2);
INSERT INTO "items" VALUES(17,'Twix',10,0.54,'snacks/twix.png',2);
INSERT INTO "items" VALUES(18,'Bagel',104,0.66,'bagel.png',1);
INSERT INTO "items" VALUES(19,'Appeltje',0,0.26,'food/appeltje.png',1);
INSERT INTO "items" VALUES(20,'Banaan',2,0.66,'food/banaan.png',1);
INSERT INTO "items" VALUES(21,'Frikandelbroodje',4,0.66,'food/frikandelbroodje.png',1);
INSERT INTO "items" VALUES(22,'Groene appel',4,0.66,'food/groene_appel.png',1);
INSERT INTO "items" VALUES(23,'Muffin',4,0.66,'food/muffin.png',1);
INSERT INTO "items" VALUES(24,'Muffin Chocolate',4,0.66,'food/muffin_chocolate.png',1);
INSERT INTO "items" VALUES(25,'Saucijzen',4,0.66,'food/saucijzen.png',1);
INSERT INTO "items" VALUES(26,'Snelle Jelle',-17,0.66,'food/snelle_jelle.png',1);
INSERT INTO "items" VALUES(27,'Fristi',10,1.01,'fristi.png',0);
INSERT INTO "items" VALUES(28,'Coca Cola',25,0.99,'drinks/coca-cola.png',0);
INSERT INTO "items" VALUES(29,'Dr Pepper',25,0.99,'drinks/dr-pepper.png',0);
INSERT INTO "items" VALUES(30,'Fanta',25,0.99,'drinks/fanta.png',0);
INSERT INTO "items" VALUES(31,'Fanta Casis',25,0.99,'drinks/fanta-casis.png',0);
INSERT INTO "items" VALUES(32,'Redbull',25,0.99,'drinks/redbull.png',0);
INSERT INTO "items" VALUES(33,'Sprite',25,0.99,'drinks/sprite.png',0);
CREATE TABLE key
(
kid INTEGER NOT NULL PRIMARY KEY,     -- key id
keyhash BLOB                          -- sha3_512 hash rfid tag uid; BLOB = Binary Large OBject, maybe TEXT also acceptable?
);
INSERT INTO "key" VALUES(1,0);
INSERT INTO "key" VALUES(2,1);
CREATE TABLE keys
(
kid BLOB NOT NULL PRIMARY KEY,  -- hash rfid tag uid; BLOB = Binary Large OBject, maybe TEXT also acceptable?
keyname VARCHAR,
pid INTEGER,
CHECK(keyname <> ''),
FOREIGN KEY (pid) REFERENCES persons(pid) ON UPDATE CASCADE
);
INSERT INTO "keys" VALUES('0','tag',1);
INSERT INTO "keys" VALUES('7025d4507c74741955afb94b73397eaefff4b4caea8b486169c7be8635917','Studenten kaart',2);
CREATE TABLE orderitems
(
oid INTEGER NOT NULL,                 -- basket ID
iid INTEGER NOT NULL,                 -- Item ID
quantity INTEGER,                     -- amount of times this item
price DECIMAL(5,2),                   -- Price as found in system on time of Buying, singular price
PRIMARY KEY (oid,iid),
FOREIGN KEY(oid) REFERENCES orders(oid),
FOREIGN KEY (iid) REFERENCES items(iid)
);
INSERT INTO "orderitems" VALUES(1,20,2,0.66);
INSERT INTO "orderitems" VALUES(1,19,4,0.26);
INSERT INTO "orderitems" VALUES(1,26,20,0.66);
INSERT INTO "orderitems" VALUES(2,27,5,1.01);
INSERT INTO "orderitems" VALUES(2,26,1,0.66);
CREATE TABLE orders
(
oid INTEGER PRIMARY KEY NOT NULL,     -- basket ID
total DECIMAL(5,2),                   -- never directly accessed by user, should be safe
date datetime,                        -- in YYYY-MM-DD HH-MM-SS format
pid NOT NULL,                         -- person id
FOREIGN KEY(pid) REFERENCES persons(pid)
);
INSERT INTO "orders" VALUES(1,15.56,'2016-11-04 18:53:49',2);
INSERT INTO "orders" VALUES(2,5.71,'2016-11-04 18:53:50',2);
CREATE TABLE person                     
(
pid INTEGER NOT NULL PRIMARY KEY,     -- person id
name VARCHAR,
sid INTEGER UNIQUE,                   -- student id
balance DECIMAL (5,2) DEFAULT 0,      -- SHOULD ONLY BE NUMBERS, DO NOT USE THE 'FEATURE' of strings, check this in python/js input!
usertype TINYINT                      -- 0: user, 1: admin

);
INSERT INTO "person" VALUES(1,'Admin',1000000,7.66,1);
INSERT INTO "person" VALUES(2,'User 1',1000001,13.91,0);
CREATE TABLE persons                     
(
pid INTEGER NOT NULL PRIMARY KEY,     -- person id
name VARCHAR,
sid INTEGER UNIQUE,                   -- student id
balance DECIMAL (5,2) DEFAULT 0,      -- SHOULD ONLY BE NUMBERS, DO NOT USE THE 'FEATURE' of strings, check this in python/js input!
usertype TINYINT,                     -- 0: user, 1: admin
password VARCHAR
);
INSERT INTO "persons" VALUES(1,'Admin','s1000000',0,1,X'2432622431322469377A4B334F486835705852706B3976416459355375674D49596F787659616E626B7836646C4F3442546C38497732446758596A61');
INSERT INTO "persons" VALUES(2,'Pieter-Tjerk','x1000001',21.27,0,X'24326224313224636C3571744A6C3074644C4673644E374D596944462E767A6F5051686C766A543959374E326A554E7934717546734D6A722E716961');
CREATE TABLE transactions
(
bid INTEGER NOT NULL,                 -- basket ID
iid INTEGER NOT NULL,                 -- Item ID
quantity INTEGER,                     -- amount of times this item
price DECIMAL(5,2),                   -- Price as found in system on time of Buying
PRIMARY KEY (bid,iid),
FOREIGN KEY(bid) REFERENCES basket(bid),
FOREIGN KEY (iid) REFERENCES items(iid)
);
COMMIT;
