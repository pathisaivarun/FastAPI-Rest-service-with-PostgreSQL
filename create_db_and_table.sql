--creating database with default values
CREATE DATABASE ecommerce_activity;

--creating table
CREATE TABLE IF NOT EXISTS ecommerce_activity_table (
    source_id serial PRIMARY KEY,
    source VARCHAR ( 200 ) NOT NULL,  
    source_type VARCHAR ( 10 ) NOT NULL,
    source_tag VARCHAR ( 10 ) NOT NULL,
    last_update_date TIMESTAMP NOT NULL,
    from_date TIMESTAMP NOT NULL,
    to_date TIMESTAMP NOT NULL,
    frequency VARCHAR ( 5 ) NOT NULL
);


---Inserting record
INSERT INTO ecommerce_activity_table (source, source_type, source_tag, last_update_date, from_date, to_date, frequency) values('flipkart', 'online', 'fk', '2023-01-01 00:00:30', '2023-01-01 00:00:15', '2023-01-01 00:00:30', '15M');