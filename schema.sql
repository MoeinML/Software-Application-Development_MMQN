-- Create Database
CREATE DATABASE IF NOT EXISTS TrainBookingSystem;
USE TrainBookingSystem;
-- 1. STATION Table (Independent Entity)
CREATE TABLE STATION (
    station_id INT AUTO_INCREMENT PRIMARY KEY,
    station_name VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL
);

-- 2. TRAIN Table (Independent Entity)
CREATE TABLE TRAIN (
    train_id INT AUTO_INCREMENT PRIMARY KEY,
    train_code VARCHAR(20) NOT NULL UNIQUE,
    train_type VARCHAR(50) NOT NULL
);

-- 3. PASSENGER Table (Independent Entity)
CREATE TABLE PASSENGER (
    passenger_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    phone_number VARCHAR(20) NOT NULL
);

-- 4. PASSENGER_EMAIL Table (Depends on PASSENGER)
CREATE TABLE PASSENGER_EMAIL (
    passenger_id INT NOT NULL,
    email VARCHAR(100) NOT NULL,
    PRIMARY KEY (passenger_id, email),
    FOREIGN KEY (passenger_id) REFERENCES PASSENGER(passenger_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- 5. SEAT Table (Depends on TRAIN)
CREATE TABLE SEAT (
    seat_id INT AUTO_INCREMENT PRIMARY KEY,
    seat_number VARCHAR(10) NOT NULL,
    carriage_number INT NOT NULL,
    seat_class VARCHAR(30) NOT NULL,
    train_id INT NOT NULL,
    FOREIGN KEY (train_id) REFERENCES TRAIN(train_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- 6. SCHEDULE Table (Depends on TRAIN and STATION)
CREATE TABLE SCHEDULE (
    schedule_id INT AUTO_INCREMENT PRIMARY KEY,
    departure_time TIME NOT NULL,
    travel_date DATE NOT NULL,
    arrival_time TIME NOT NULL,
    train_id INT NOT NULL,
    departure_station_id INT NOT NULL,
    arrival_station_id INT NOT NULL,
    FOREIGN KEY (train_id) REFERENCES TRAIN(train_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (departure_station_id) REFERENCES STATION(station_id),
    FOREIGN KEY (arrival_station_id) REFERENCES STATION(station_id)
);

-- 7. BOOKING Table (Depends on PASSENGER, SCHEDULE, and SEAT)
CREATE TABLE BOOKING (
    booking_id INT AUTO_INCREMENT PRIMARY KEY,
    booking_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) NOT NULL CHECK (status IN ('Confirmed', 'Pending', 'Cancelled')),
    ticket_price DECIMAL(10, 2) NOT NULL CHECK (ticket_price >= 0),
    passenger_id INT NOT NULL,
    schedule_id INT NOT NULL,
    seat_id INT NULL, -- Optional assignment (0,1 cardinality)
    FOREIGN KEY (passenger_id) REFERENCES PASSENGER(passenger_id),
    FOREIGN KEY (schedule_id) REFERENCES SCHEDULE(schedule_id),
    FOREIGN KEY (seat_id) REFERENCES SEAT(seat_id)
);
