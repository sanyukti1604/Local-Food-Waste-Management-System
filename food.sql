
use food_management;
CREATE DATABASE food_management;
CREATE TABLE food_listing_data (
    food_id INT,
    provider_id INT,
    food_item VARCHAR(255),
    quantity INT,
    expiry_date DATE,
    description TEXT
);

SET GLOBAL local_infile = 1;


LOAD DATA LOCAL INFILE "C:\Users\shrut\Downloads\providers_data (1).csv"
INTO TABLE food_listing_data
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

SHOW VARIABLES LIKE 'local_infile';
 
 
CREATE TABLE providers (
    provider_id INT,
    name VARCHAR(255),
    Type VARCHAR(255),
    Address VARCHAR(255),
    City VARCHAR(255),
    contact VARCHAR(50)
    
);

LOAD DATA LOCAL INFILE 'C:\\Users\\shrut\\Downloads\\providers_data (1).csv'
INTO TABLE providers
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

