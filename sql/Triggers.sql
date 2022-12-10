-- The Following are all of the Fuctions triggers used in the project
-- trigger called after a new line has been inserted will call the reduce quantity function

CREATE OR REPLACE TRIGGER contains_trigger AFTER
INSERT ON contains
FOR EACH ROW EXECUTE PROCEDURE reduce_quantity();

--trigger that gets called after a update on the books table will call the compensation_add() fucnton

CREATE OR REPLACE TRIGGER compensation_trigger AFTER
UPDATE ON books
FOR EACH ROW EXECUTE PROCEDURE compensation_add();

-- trigger that gets called after an upadte on the books table, will call teh reorder check function

CREATE OR REPLACE TRIGGER reorder_trigger AFTER
UPDATE ON books
FOR EACH ROW EXECUTE PROCEDURE reorder_check();