
CREATE DATABASE IF NOT EXISTS eagleEyeDB;
USE eagleEyeDB;

CREATE TABLE IF NOT EXISTS agents (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codeName VARCHAR(255),
    realName VARCHAR(255),
    location VARCHAR(255),
    status VARCHAR(50),
    missionsCompleted INT
);
