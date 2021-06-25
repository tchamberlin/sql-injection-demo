DROP TABLE IF EXISTS users;
CREATE TABLE users (id SERIAL PRIMARY KEY, username VARCHAR(64), password VARCHAR(256));
INSERT INTO users (username, password) VALUES ('thomas', 'password1');
INSERT INTO users (username, password) VALUES ('bill', 'password2');


DROP TABLE IF EXISTS Students;
CREATE TABLE Students (id SERIAL PRIMARY KEY, first_name VARCHAR(64), last_name VARCHAR(64));
INSERT INTO Students (first_name, last_name) VALUES ('fred', 'frederson');
INSERT INTO Students (first_name, last_name) VALUES ('bob', 'boberson');
