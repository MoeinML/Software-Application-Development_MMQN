-- Create Database
CREATE DATABASE IF NOT EXISTS TrainBookingSystem;
USE TrainBookingSystem;
-- 1. STATION Table (Independent Entity)
CREATE TABLE STATION (
    station_id INT AUTO_INCREMENT PRIMARY KEY,
    station_name VARCHAR(100) NOT NULL UNIQUE,
    city VARCHAR(100) NOT NULL
);

-- 2. TRAIN Table (Independent Entity)
CREATE TABLE TRAIN (
    train_id INT AUTO_INCREMENT PRIMARY KEY,
    train_code VARCHAR(20) NOT NULL UNIQUE,
    train_type VARCHAR(50) NOT NULL,
    capacity INT NOT NULL CHECK (capacity > 0)
);

-- 3. PASSENGER Table (Independent Entity)
CREATE TABLE PASSENGER (
    passenger_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    phone_number VARCHAR(20) NOT NULL UNIQUE
);

-- 4. PASSENGER_EMAIL Table (Depends on PASSENGER)
CREATE TABLE PASSENGER_EMAIL (
    passenger_id INT NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    PRIMARY KEY (passenger_id, email),
    FOREIGN KEY (passenger_id) REFERENCES PASSENGER(passenger_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- 5. SCHEDULE Table (Depends on TRAIN and STATION)
CREATE TABLE SCHEDULE (
    schedule_id INT AUTO_INCREMENT PRIMARY KEY,
    departure_time TIME NOT NULL,
    travel_date DATE NOT NULL,
    arrival_time TIME NOT NULL,
    train_id INT NOT NULL,
    departure_station_id INT NOT NULL,
    arrival_station_id INT NOT NULL,
    FOREIGN KEY (train_id) REFERENCES TRAIN(train_id)
        ON UPDATE CASCADE,
    FOREIGN KEY (departure_station_id) REFERENCES STATION(station_id),
    FOREIGN KEY (arrival_station_id) REFERENCES STATION(station_id)
);

-- 6. BOOKING Table (Depends on PASSENGER and SCHEDULE)
CREATE TABLE BOOKING (
    booking_id INT AUTO_INCREMENT PRIMARY KEY,
    booking_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    passenger_id INT NOT NULL,
    schedule_id INT NOT NULL,
    number_of_tickets INT NOT NULL CHECK (number_of_tickets > 0),
    FOREIGN KEY (passenger_id) REFERENCES PASSENGER(passenger_id)
        ON UPDATE CASCADE,
    FOREIGN KEY (schedule_id) REFERENCES SCHEDULE(schedule_id)
        ON UPDATE CASCADE
);