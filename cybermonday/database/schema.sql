-- Create database
CREATE DATABASE cybermonday;
\c cybermonday;

-- Create table products
CREATE TABLE products(
    id     BIGSERIAL PRIMARY KEY NOT NULL,
    name   VARCHAR(200) NOT NULL,
    desc   VARCHAR(200) NOT NULL,
    price  BIGINT NOT NULL
);
