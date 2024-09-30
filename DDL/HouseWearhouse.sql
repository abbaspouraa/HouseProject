USE HouseMarket;

CREATE TABLE IF NOT EXISTS HouseMarket (
    id BIGINT AUTO_INCREMENT PRIMARY KEY ,
    price INT NOT NULL ,
    address VARCHAR(250) NOT NULL,
    bedrooms VARCHAR(10) NOT NULL ,
    bathrooms VARCHAR(10) NOT NULL ,
    sq_ft INT ,
    image VARCHAR(1000) ,
    url VARCHAR(1000) ,
    createdAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    updatedAt DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY (address),
    KEY `price` (price),
    KEY `sq_ft` (sq_ft),
    KEY `createdAt` (createdAt),
    KEY `updatedAt` (updatedAt)
)