
CREATE DATABASE IF NOT EXISTS eagleEyeDB;
USE eagleEyeDB;

CREATE TABLE IF NOT EXISTS agents (
    _id INT AUTO_INCREMENT PRIMARY KEY,
    code_name VARCHAR(255) NOT NULL UNIQUE,
    real_name VARCHAR(255),
    location VARCHAR(255),
    status VARCHAR(50),
    missions_completed INT DEFAULT 0
);
