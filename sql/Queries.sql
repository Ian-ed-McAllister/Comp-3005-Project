-- The Following are all of the Fuctions triggers used in the project
 --DBinit.py all of the following are insert queries, only giving one of the values inserted for each table

INSERT INTO users (username,password,type,cardNum,ccv,expDate,country,province,streetAddress,city,postalCode)
Values ('bookowner',
        'admin',
        'A',
        '1234567891234567',
        '123',
        '12/24',
        'CA',
        'Ontario',
        '1 west str.',
        'OTTAWA',
        'A1B1C1');


INSERT INTO orders (cid,shippedFrom,currentLocation,cardNum,expDate,ccv,country,province,streetAddress,city,postalCode)
Values ('1',
        'StartHouse',
        'in transit',
        '1234567890123456',
        '07/12',
        '123',
        'CA',
        'Ontario',
        '123 Street',
        'Ottawa',
        'A1B2C3');


INSERT INTO publisher (name,email,country,province,streetAddress,city,postalcode,bankid,compensation)
Values ('Fantastic Books',
        'FB@email.com',
        'CA',
        'Ontario',
        '3 Book Street',
        'Ottawa',
        'S3B4D5',
        '1234567890',
        '0');


INSERT INTO phone (pid,num)
VALUES (1,
        '6131112222');


INSERT INTO books (title,publisherName,isbn,numPages,price,percentage, quantity,show)
Values ('Book about books',
        'Best Books',
        '1111111111111',
        '112',
        '12.99',
        '0.3',
        '15',
        '1');


INSERT INTO authors (bid,authname)
Values ('1',
        'Phil');


INSERT INTO genres (bid,genre)
Values ('1',
        'Science');


INSERT INTO contains (oid,
                      bid,
                      quantity)
Values ('1',
        '1',
        '1');

--middlware.py will not show any of duplicate queries, anything with a values option the data passed in are just place holder the queries may not run as the data may not exsist
 --gets all the books

SELECT *
FROM books;

--gets all genres

SELECT *
FROM genres; --gets all authors


SELECT *
FROM authors;

--used to get the most recent order placed

SELECT *
FROM orders
ORDER BY oid DESC
LIMIT 1;

--checks to see if a user exists with the given useranme and password

SELECT *
FROM users
WHERE username = 'user'
    AND password = 'pass';

--select all orders where the customer who placed them is the same as cid

SELECT *
FROM orders
WHERE cid = 1;

--update a user that has the corresponding uid value, and change its shipping and billing info

UPDATE users
SET cardnum = 1234123412341234,
    ccv =123,
    expdate = '05/16',
    country = 'Canada',
    province = 'Ontario',
    streetaddress = '13 street',
    city = 'Ottawa',
    postalcode = 'a1b2c3'
WHERE uid = 1;

--updates the books show value when the id is correct

UPDATE books
SET show = 0
WHERE bid = 1;

-- calls a agragate function that sums the compensation column of the publisher relation

SELECT sum(compensation) AS costs
FROM publisher;

-- a queries that has a sums the values of a subquery, teh subquery finds when a book was purchased using the contain tables then multiplying the quantity in the contains table
-- by the price in teh books table

SELECT sum(total_cost)
FROM
    (SELECT b.quantity*a.price AS total_cost
     FROM books a,
          contains b
     WHERE a.bid = b.bid) AS my_table;

