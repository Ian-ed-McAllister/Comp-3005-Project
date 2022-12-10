-- The Following queries are all of the DDL queries used in the proeject
CREATE TABLE IF NOT EXISTS Users(
    username varchar(20) PRIMARY KEY,
    uid SERIAL UNIQUE,
    password varchar(20) NOT NULL,
    type char(1) NOT NULL,
    cardNum char(16),
    ccv char(3),
    expDate char(5),
    country varchar(22),
    province varchar(22),
    streetAddress varchar(30),
    city varchar(15),
    postalCode varchar(6)
);

CREATE TABLE IF NOT EXISTS orders(
    oid SERIAL PRIMARY KEY,
    cid int NOT NULL,
    shippedFrom varchar(20) NOT NULL,
    currentLocation varchar(20) NOT NULL,
    cardNum char(16) NOT NULL,
    expDate char(5) NOT NULL,
    ccv char(3) NOT NULL,
    country varchar(22) NOT NULL,
    province varchar(22) NOT NULL,
    streetAddress varchar(30) NOT NULL,
    city varchar(15) N OT NULL,
    postalCode char(6) NOT NULL,
    FOREIGN KEY (cid) REFERENCES users(uid)
);

CREATE TABLE IF NOT EXISTS publisher(
    pid SERIAL PRIMARY KEY,
    name varchar(20) UNIQUE NOT NULL,
    email varchar(40) NOT NULL,
    country varchar(22) NOT NULL,
    province varchar(22) NOT NULL,
    streetAddress varchar(20) NOT NULL,
    city varchar(20) NOT NULL,
    postalcode char(6) NOT NULL,
    bankid varchar(10) NOT NULL,
    compensation numeric (10, 2) NOT NULL
);

CREATE TABLE IF NOT EXISTS phone(
    pid int,
    num char(10),
    FOREIGN KEY (pid) REFERENCES publisher(pid),
    PRIMARY KEY (pid, num)
);

CREATE TABLE IF NOT EXISTS books(
    bid SERIAL UNIQUE,
    title varchar(100) NOT NULL,
    publisherName varchar(20) NOT NULL,
    isbn char(13) NOT NULL PRIMARY KEY,
    numPages int NOT NULL,
    price numeric (5, 2),
    percentage numeric (3, 2),
    quantity int,
    show int NOT NULL,
    FOREIGN KEY (publisherName) REFERENCES publisher(name)
);

CREATE TABLE IF NOT EXISTS authors(
    bid int,
    authName varchar(20),
    FOREIGN KEY (bid) REFERENCES books(bid),
    PRIMARY KEY (bid, authName)
);

CREATE TABLE IF NOT EXISTS genres(
    bid int,
    genre varchar(20),
    FOREIGN KEY (bid) REFERENCES books(bid),
    PRIMARY KEY (bid, genre)
);

CREATE TABLE IF NOT EXISTS contains(
    oid int,
    bid int,
    quantity int,
    FOREIGN KEY (oid) REFERENCES orders(oid),
    FOREIGN KEY (bid) REFERENCES books(bid),
    PRIMARY KEY (oid, bid)
);