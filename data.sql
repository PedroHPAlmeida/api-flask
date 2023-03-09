CREATE TABLE users (
      id int NOT NULL PRIMARY KEY AUTO_INCREMENT,
      username VARCHAR(20) NOT NULL,
      password VARCHAR(200) NOT NULL,
      name VARCHAR(60) NOT NULL,
      email VARCHAR(50) NOT NULL,
      created_on DATETIME
);