DROP TABLE IF EXISTS users;
CREATE TABLE users (id SERIAL PRIMARY KEY, username VARCHAR(64), password VARCHAR(256));
INSERT INTO users (username, password) VALUES ('rosa', 'password2');
INSERT INTO users (username, password) VALUES ('thomas', 'password1');
INSERT INTO users (username, password) VALUES ('admin', 'password0');
INSERT INTO users (username, password) VALUES ('megan', 'password3');
INSERT INTO users (username, password) VALUES ('tyler', 'password4');


DROP TABLE IF EXISTS Students;
CREATE TABLE Students (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(64),
    last_name VARCHAR(64),
    card_info VARCHAR(64)
);
