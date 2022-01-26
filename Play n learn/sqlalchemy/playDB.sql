PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE some_table (x int unique, y int unique);
INSERT INTO some_table VALUES(1,1);
INSERT INTO some_table VALUES(2,4);
INSERT INTO some_table VALUES(6,8);
INSERT INTO some_table VALUES(9,10);
COMMIT;
