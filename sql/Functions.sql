-- The Following are all of the Fuctions queries used in the project
 --Function gets called after a update to contain is called this will reduce the number of book avalible for sale by that many

CREATE OR REPLACE FUNCTION reduce_quantity() RETURNS TRIGGER LANGUAGE plpgsql AS $$
    BEGIN
        UPDATE books
        SET quantity = quantity - NEW.quantity        --NEW.quantity refers to the quantity column of the new row that was added in the contains relation
        WHERE books.bid = NEW.bid; -- will only do this when it matches the book id as that would correspond to the correct book
        RETURN NEW;
    END;
    $$ -- function gets called after a book row is updated will add compensation to the books publisher equal to its cut of the profits

CREATE OR REPLACE FUNCTION compensation_add() RETURNS TRIGGER LANGUAGE plpgsql AS $$
                    BEGIN
                        IF NEW.quantity < OLD.quantity then -- needed to make sure that you only do this when the number of books is being rediced as that means the book would be getting sold
                        UPDATE publisher
                        SET compensation = compensation + ((OLD.price * (OLD.quantity - NEW.quantity))*OLD.percentage) -- add the current compensation to the publishers cut of the new books sold
                        WHERE publisher.name = NEW.publishername; -- only do this when the books publisher is the same as this row
                        END IF;
                        RETURN NEW;
                    END;
                    $$ -- function gets called after a update to the books table, it will check to see if new books need to ordered if so you would be able to send out an email using the publishers email.

CREATE OR REPLACE FUNCTION reorder_check() RETURNS TRIGGER LANGUAGE plpgsql AS $$
                    BEGIN
                        IF NEW.quantity < 10 then -- checks to see if the quantity is lower than the threshold
                        UPDATE books
                        SET quantity = quantity  + (SELECT sum(quantity) FROM contains WHERE bid = NEW.bid) -- gets the quantity of books that have been sold in the last month to then add on to the current number of books
                        WHERE books.bid = NEW.bid;
                        END IF;
                        RETURN NEW;
                    END;
                    $$