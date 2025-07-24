-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 17, 2025 at 02:22 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `cabbooking`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin_users`
--

CREATE TABLE `admin_users` (
  `id` int(11) NOT NULL,
  `username` varchar(50) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin_users`
--

INSERT INTO `admin_users` (`id`, `username`, `password`) VALUES
(1, 'admin', 'admin123');

-- --------------------------------------------------------

--
-- Table structure for table `bookings`
--

CREATE TABLE `bookings` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `driver_id` int(11) DEFAULT NULL,
  `source` varchar(100) DEFAULT NULL,
  `destination` varchar(100) DEFAULT NULL,
  `booking_time` datetime DEFAULT NULL,
  `ride_datetime` datetime DEFAULT current_timestamp(),
  `ride_status` int(11) DEFAULT 2,
  `car_type` varchar(50) DEFAULT NULL,
  `price` decimal(10,2) DEFAULT NULL,
  `otp` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `bookings`
--

INSERT INTO `bookings` (`id`, `user_id`, `driver_id`, `source`, `destination`, `booking_time`, `ride_datetime`, `ride_status`, `car_type`, `price`, `otp`) VALUES
(17, 4, 10, 'hyd', 'blr', '2025-07-08 11:52:09', '2025-07-08 11:52:09', 2, 'Sedan', 6000.00, 2964),
(18, 4, 10, 'blr', 'hyd', '2025-07-08 12:12:30', '2025-07-08 12:12:30', 2, 'Hatchback', 89.00, 6374),
(19, 4, 10, 'blr', 'hyd', '2025-07-08 12:16:52', '2025-07-08 12:16:52', 2, 'Sedan', 6000.00, 9167),
(20, 4, 10, 'blr', 'hyd', '2025-07-08 12:20:07', '2025-07-08 12:20:07', 2, 'Sedan', 6000.00, 9653),
(21, 4, 10, 'blr', 'hyd', '2025-07-08 12:22:27', '2025-07-08 12:22:27', 2, 'Hatchback', 89.00, 7791),
(22, 4, 10, 'hyd', 'blr', '2025-07-08 12:22:37', '2025-07-08 12:22:37', 2, 'Sedan', 6000.00, 9464),
(23, 4, 10, 'blr', 'hyd', '2025-07-08 12:59:19', '2025-07-08 12:59:19', 2, 'Sedan', 6000.00, 2055),
(25, 4, 10, 'blr', 'hyd', '2025-07-16 11:32:56', '2025-07-16 11:32:56', 2, 'Hatchback', 89.00, 4539),
(26, 6, 11, 'blr', 'hyd', '2025-07-16 11:36:21', '2025-07-16 11:36:21', 2, 'Hatchback', 89.00, 2382),
(30, 6, 10, 'hyd', 'blr', '2025-07-17 16:51:04', '2025-07-17 16:51:04', 2, 'Hatchback', 89.00, 6783),
(31, 7, 10, 'blr', 'hyd', '2025-07-17 17:39:09', '2025-07-17 17:39:09', 0, 'Sedan', 7555.00, 8025);

-- --------------------------------------------------------

--
-- Table structure for table `drivers`
--

CREATE TABLE `drivers` (
  `id` int(11) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `vehicle_type` enum('Sedan','SUV','Hatchback') NOT NULL,
  `user_id` varchar(50) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  `vehicle_number` varchar(50) DEFAULT NULL,
  `vehicle_company` varchar(100) DEFAULT NULL,
  `vehicle_model` varchar(100) DEFAULT NULL,
  `approved` tinyint(1) DEFAULT 0,
  `available` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `drivers`
--

INSERT INTO `drivers` (`id`, `name`, `phone`, `vehicle_type`, `user_id`, `password`, `vehicle_number`, `vehicle_company`, `vehicle_model`, `approved`, `available`) VALUES
(5, 'ANISHA H KANDACHAR', '7483493042', 'SUV', 'anishaaa89a@gmail.com', 'aaaa', 'KA01MB2344', 'BMW', 'Toyota Camry 2022', 1, 0),
(10, 'fakey driver autosa', '7892011972', 'Hatchback', 'anishaaa@gmail.com', 'anishaaa@gmail.com', 'KA01MB7890', 'BMWt', 'Toyota Camry 2022', 1, 0),
(11, 'ANISHA H KANDACHAR', '8762681543', 'SUV', 'anishasri@gmail.com', 'anishasri@gmail.com', 'KA01MB1121', 'BMW', 'Toyota Camry 2025', 1, 1),
(12, 'ANISHA H KANDACHAR', '7892011973', 'Sedan', 'anishaaa1@gmail.com', 'anishaaa1@gmail.com', 'KA01MB2333', 'BMW', 'Toyota Camry 2022', 0, 1),
(17, 'om ', '8277620711', 'SUV', 'om@gmail.com', 'om@gmail.com', 'TN01MB2344', 'BMW', 'Toyota Camry 2022', 0, 0);

-- --------------------------------------------------------

--
-- Table structure for table `prices`
--

CREATE TABLE `prices` (
  `id` int(11) NOT NULL,
  `from_location` varchar(100) NOT NULL,
  `to_location` varchar(100) NOT NULL,
  `car_type` enum('Sedan','SUV','Hatchback') NOT NULL,
  `price` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `prices`
--

INSERT INTO `prices` (`id`, `from_location`, `to_location`, `car_type`, `price`) VALUES
(1, 'blr', 'hyd', 'Sedan', 7555.00),
(2, 'blr', 'hyd', 'Hatchback', 89.00),
(4, 'PES', 'Girinagar', 'SUV', 122.00),
(6, 'blr', 'hyd', 'SUV', 5544.00),
(7, 'Girinagar', 'RR', 'SUV', 1234.00);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  `user_id` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `name`, `phone`, `email`, `password`, `user_id`) VALUES
(1, 'ANISHA H aaaaa', '+9179473002996420', 'admin@cabbooking.com', '000', 'anisha'),
(4, 'fakey', '7483493052', 'admin@cabbookiang.com', 'anishaaa', 'anishaaa'),
(5, 'ANISHA H KANDACHARs', '7892011972', 'VARUN@GMAIL.COM', 'VARUN@GMAIL.COM', 'VARUN@GMAIL.COM'),
(6, 'om shivayaaa', '721827212', 'admin@cabbookinga.com', 'admin@cabbookinga.com', 'admin@cabbookinga.com'),
(7, 'veena', '7892011971', 'veena@gmail.com', 'veena@gmail.com', 'veena@gmail.com');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin_users`
--
ALTER TABLE `admin_users`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `bookings`
--
ALTER TABLE `bookings`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `driver_id` (`driver_id`);

--
-- Indexes for table `drivers`
--
ALTER TABLE `drivers`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`),
  ADD UNIQUE KEY `unique_phone` (`phone`),
  ADD UNIQUE KEY `unique_vehicle_number` (`vehicle_number`);

--
-- Indexes for table `prices`
--
ALTER TABLE `prices`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_route_car_type` (`from_location`,`to_location`,`car_type`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`),
  ADD UNIQUE KEY `unique_email` (`email`),
  ADD UNIQUE KEY `unique_phone` (`phone`),
  ADD UNIQUE KEY `unique_userid` (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin_users`
--
ALTER TABLE `admin_users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `bookings`
--
ALTER TABLE `bookings`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=32;

--
-- AUTO_INCREMENT for table `drivers`
--
ALTER TABLE `drivers`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT for table `prices`
--
ALTER TABLE `prices`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `bookings`
--
ALTER TABLE `bookings`
  ADD CONSTRAINT `bookings_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `bookings_ibfk_2` FOREIGN KEY (`driver_id`) REFERENCES `drivers` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
