CREATE TABLE purchases (
    purchase_id     INT PRIMARY KEY AUTO_INCREMENT,
    amount          DECIMAL(10, 2) NOT NULL,
    category        VARCHAR(255) NOT NULL,
    date_purchased  DATE NOT NULL, 
    comment         VARCHAR(255)
);


