/* definition for SQL - sadly inserting millions of records into SQLite is slow so need to use my/postgreqsl */
CREATE TABLE Magnets (
	   tpb_id INT PRIMARY KEY,
	   name TEXT,
	   size INT,
	   seeders INT,
	   leechers INT,
	   urn TEXT
);
