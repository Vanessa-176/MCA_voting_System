-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Aug 21, 2025 at 02:07 AM
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
-- Database: `mca_voting_system`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin_users`
--

CREATE TABLE `admin_users` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `full_name` varchar(255) NOT NULL,
  `role` enum('super_admin','admin','moderator') DEFAULT 'admin',
  `is_active` tinyint(1) DEFAULT 1,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `last_login` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin_users`
--

INSERT INTO `admin_users` (`id`, `username`, `email`, `password_hash`, `full_name`, `role`, `is_active`, `created_at`, `last_login`) VALUES
(1, 'admin', 'admin@mca.ac.mw', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'System Administrator', 'super_admin', 1, '2025-08-20 10:39:42', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `candidates`
--

CREATE TABLE `candidates` (
  `id` int(11) NOT NULL,
  `position_id` int(11) NOT NULL,
  `candidate_name` varchar(255) NOT NULL,
  `student_id` varchar(50) NOT NULL,
  `program` varchar(100) NOT NULL,
  `year_of_study` int(11) NOT NULL,
  `manifesto` text DEFAULT NULL,
  `photo_url` varchar(500) DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT 1,
  `registration_date` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `candidates`
--

INSERT INTO `candidates` (`id`, `position_id`, `candidate_name`, `student_id`, `program`, `year_of_study`, `manifesto`, `photo_url`, `is_active`, `registration_date`) VALUES
(2, 1, 'Daniel Carter', 'MCA/2024/103', 'BMIS', 4, NULL, NULL, 1, '2025-08-20 19:09:54'),
(3, 1, 'Diana Scott', 'MCA/2024/111', 'BBME', 4, NULL, NULL, 1, '2025-08-20 19:19:15'),
(4, 2, 'Kelvin Banda', 'MCA/2024/108', 'BMPR', 4, NULL, NULL, 1, '2025-08-20 19:20:28'),
(5, 2, 'Brenda Zulu', 'MCA/2024/116', 'BAAAIS', 4, NULL, NULL, 1, '2025-08-20 19:21:25'),
(6, 3, 'Victor Jere', 'MCA/2024/109', 'BMIS', 4, NULL, NULL, 1, '2025-08-20 19:22:43'),
(7, 3, 'Monica Adams', 'MCA/2024/117', 'BMPR', 4, NULL, NULL, 1, '2025-08-20 19:23:54'),
(8, 4, 'Yasmin Umar', 'MCA/2024/118', 'BMIS', 4, NULL, NULL, 1, '2025-08-20 19:24:57'),
(9, 4, 'David Chirwa', 'MCA/2024/107', 'BMIS', 4, NULL, NULL, 1, '2025-08-20 19:25:55'),
(10, 5, 'Christopher Moyo', 'MCA/2024/110', 'BMIS', 4, NULL, NULL, 1, '2025-08-20 19:26:52'),
(11, 5, 'Simon Gama', 'MCA/2024/125', 'BMIS', 3, NULL, NULL, 1, '2025-08-20 19:27:58'),
(12, 10, 'Oscar Phiri', 'MCA/2024/126', 'BMIS', 3, NULL, NULL, 1, '2025-08-20 19:28:57'),
(13, 10, 'Linda Mwanza', 'MCA/2024/129', 'BAAAIS', 4, NULL, NULL, 1, '2025-08-20 19:29:57'),
(14, 6, 'Faith Peterson', 'MCA/2024/132', 'BBME', 3, NULL, NULL, 1, '2025-08-20 19:31:03'),
(15, 6, 'Alice Brown', 'MCA/2024/131', 'BMIS', 3, NULL, NULL, 1, '2025-08-20 19:32:05'),
(16, 7, 'Chikondi Zulu', 'MCA/2024/134', 'BMPR', 4, NULL, NULL, 1, '2025-08-20 19:33:26'),
(17, 7, 'Wesley Banda', 'MCA/2024/133', 'BMPR', 4, NULL, NULL, 1, '2025-08-20 19:34:32'),
(18, 11, 'Martha Chuma', 'MCA/2024/135', 'BMIS', 3, NULL, NULL, 1, '2025-08-20 19:36:12'),
(19, 11, 'Isaac Tembo', 'MCA/2024/130', 'BMIS', 3, NULL, NULL, 1, '2025-08-20 19:37:01'),
(20, 9, 'Patrick Kumwenda', 'MCA/2024/128', 'BBME', 4, NULL, NULL, 1, '2025-08-20 19:38:20'),
(21, 9, 'Phillip Carter', 'MCA/2024/127', 'BAAAIS', 4, NULL, NULL, 1, '2025-08-20 19:39:29'),
(22, 8, 'Caroline Mwanza', 'MCA/2024/140', 'BBME', 3, NULL, NULL, 1, '2025-08-20 19:46:10'),
(23, 8, 'Jacob Kalinda', 'MCA/2024/141', 'BMPR', 4, NULL, NULL, 1, '2025-08-20 19:46:54');

-- --------------------------------------------------------

--
-- Table structure for table `election_settings`
--

CREATE TABLE `election_settings` (
  `id` int(11) NOT NULL,
  `setting_name` varchar(100) NOT NULL,
  `setting_value` varchar(500) NOT NULL,
  `description` text DEFAULT NULL,
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `election_settings`
--

INSERT INTO `election_settings` (`id`, `setting_name`, `setting_value`, `description`, `updated_at`) VALUES
(1, 'voting_enabled', 'true', 'Enable or disable voting functionality', '2025-08-20 10:39:09'),
(2, 'registration_enabled', 'true', 'Enable or disable student registration', '2025-08-20 10:39:09'),
(3, 'election_title', 'MCA Students Union Elections 2024', 'Title displayed on the voting system', '2025-08-20 10:39:09'),
(4, 'voting_start_date', '2024-03-01 08:00:00', 'When voting period begins', '2025-08-20 10:39:09'),
(5, 'voting_end_date', '2024-03-03 18:00:00', 'When voting period ends', '2025-08-20 10:39:09'),
(6, 'results_visible', 'true', 'Whether results are visible to students', '2025-08-20 10:39:09'),
(7, 'max_votes_per_position', '1', 'Maximum votes allowed per position', '2025-08-20 10:39:09');

-- --------------------------------------------------------

--
-- Table structure for table `positions`
--

CREATE TABLE `positions` (
  `id` int(11) NOT NULL,
  `position_name` varchar(100) NOT NULL,
  `position_description` text DEFAULT NULL,
  `display_order` int(11) DEFAULT 0,
  `is_active` tinyint(1) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `positions`
--

INSERT INTO `positions` (`id`, `position_name`, `position_description`, `display_order`, `is_active`) VALUES
(1, 'President', 'Student Union President - Overall leader of the student body', 1, 1),
(2, 'Vice President', 'Assistant to the President and deputy leader', 2, 1),
(3, 'General Secretary', 'Handles correspondence and documentation', 3, 1),
(4, 'Financial Controller', 'Manages student union finances and budgets', 4, 1),
(5, 'Academics Director', 'Oversees academic affairs and student academic welfare', 5, 1),
(6, 'Female Representative', 'Represents female students interests and concerns', 6, 1),
(7, 'Social Welfare', 'Handles student welfare and social activities', 7, 1),
(8, 'Religion', 'Coordinates religious activities and spiritual welfare', 8, 1),
(9, 'Sports Director', 'Manages sports activities and competitions', 9, 1),
(10, 'Cafeteria Director', 'Oversees cafeteria services and food quality', 10, 1),
(11, 'Hostel Director', 'Manages hostel affairs and accommodation issues', 11, 1);

-- --------------------------------------------------------

--
-- Table structure for table `students`
--

CREATE TABLE `students` (
  `id` int(11) NOT NULL,
  `student_id` varchar(50) NOT NULL,
  `full_name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `program` varchar(100) NOT NULL,
  `year_of_study` int(11) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `has_voted` tinyint(1) DEFAULT 0,
  `registration_date` timestamp NOT NULL DEFAULT current_timestamp(),
  `last_login` timestamp NULL DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `students`
--

INSERT INTO `students` (`id`, `student_id`, `full_name`, `email`, `program`, `year_of_study`, `password_hash`, `has_voted`, `registration_date`, `last_login`, `is_active`) VALUES
(0, 'MCA/2024/107', 'David Chirwa', 'ch4765@mca.ac.mw', 'BAAAIS', 4, 'chirwa1234', 0, '2025-08-20 11:15:09', NULL, 1),
(1, 'MCA/2024/100', 'Melody Phiri', 'ph0234@mca.ac.mw', 'BBME', 3, 'melody1243', 0, '2025-08-20 10:40:04', NULL, 1),
(2, 'MCA/2024/101', 'Brian Williams', 'wi9832@maca.ac.mw', 'BBME', 2, 'Brian1234', 0, '2025-08-20 10:59:54', NULL, 1),
(4, 'MCA/2024/102', 'Amina Hassan', 'ha1254@mca.ac.mw', 'BMIS', 1, 'amina1234', 0, '2025-08-20 11:03:50', NULL, 0),
(5, 'MCA/2024/103', 'Daniel Carter', 'ca2346@maca.ac.mw', 'BMIS', 4, 'Carter1234', 0, '2025-08-20 11:06:03', NULL, 1),
(6, 'MCA/2024/104', 'Olivia Brown', 'br5870@mca.ac.mw', 'BAAAIS', 3, 'brown1234', 0, '2025-08-20 11:08:06', NULL, 1),
(7, 'MCA/2024/105', 'Emily Clarke', 'cl9453@mca.ac.mw', 'BMPR', 2, 'clarke1234', 0, '2025-08-20 11:10:10', NULL, 1),
(8, 'MCA/2024/106', 'Hannah Jere', 'jr2548@mca.ac.mw', 'BMIS', 2, 'jere1234', 0, '2025-08-20 11:11:32', NULL, 1),
(9, 'MCA/2024/136', 'Chloe Peterson', 'pr5683@mca.ac.mw', 'BBME', 3, 'peterson1234', 0, '2025-08-20 11:12:53', NULL, 1),
(12, 'MCA/2024/108', 'Kelvin Banda', 'ba3785@mca.ac.mw', 'BMPR', 4, 'Banda1234', 0, '2025-08-20 11:22:52', NULL, 1),
(13, 'MCA/2024/109', 'Victor Jere', 'jr7603@mca.ac.mw', 'BMIS', 4, 'jere1234', 0, '2025-08-20 11:24:19', NULL, 1),
(14, 'MCA/2024/110', 'Christopher Moyo', 'my3498@mca.ac.mw', 'BMIS', 4, 'moyo1234', 0, '2025-08-20 11:25:50', NULL, 1),
(15, 'MCA/2024/111', 'Diana Scott', 'sc2309@mca.ac.mw', 'BBME', 4, 'scott1234', 0, '2025-08-20 11:27:07', NULL, 1),
(16, 'MCA/2024/112', 'Anthony Mbewe', 'mb5693@maca.ac.mw', 'BBME', 4, 'mbewe1234', 0, '2025-08-20 11:29:20', NULL, 1),
(17, 'MCA/2024/115', 'Fatima Mohammed', 'mh4876@mca.ac.mw', 'BAAAIS', 4, 'mohammed1234', 0, '2025-08-20 11:31:42', NULL, 1),
(18, 'MCA/2024/116', 'Brenda Zulu', 'zu4763@mca.ac.mw', 'BAAAIS', 4, 'zulu1234', 0, '2025-08-20 11:32:57', NULL, 1),
(19, 'MCA/2024/117', 'Monica Adams', 'ad6513@mca.ac.mw', 'BMPR', 4, 'adams1234', 0, '2025-08-20 11:33:55', NULL, 1),
(20, 'MCA/2024/118', 'Yasmin Umar', 'um3892@mca.ac.mw', 'BMIS', 4, 'umar1234', 0, '2025-08-20 11:36:00', NULL, 1),
(21, 'MCA/2024/119', 'Robert Khumalo', 'kh6123@mca.ac.mw', 'BMIS', 1, 'khumalo1234', 0, '2025-08-20 11:39:28', NULL, 1),
(22, 'MCA/2024/120', 'Justin Kaunda', 'ku9384@mca.ac.mw', 'BMIS', 1, 'kaunda1234', 0, '2025-08-20 11:41:22', NULL, 1),
(23, 'MCA/2024/121', 'Juliet Manda', 'ma4139@mca.ac.mw', 'BBME', 2, 'manda1234', 0, '2025-08-20 11:43:40', NULL, 1),
(24, 'MCA/2024/122', 'Patricia Young', 'yg6589@mca.ac.mw', 'BMIS', 2, 'young1234', 0, '2025-08-20 11:45:06', NULL, 1),
(25, 'MCA/2024/123', 'Andrew Kalua', 'kl6705@mca.ac.mw', 'BBME', 3, 'kalua1234', 0, '2025-08-20 11:47:03', NULL, 1),
(26, 'MCA/2024/124', 'Ruth Miller', 'ml7836@mca.ac.mw', 'BMPR', 3, 'miller1234', 0, '2025-08-20 11:48:24', NULL, 1),
(27, 'MCA/2024/125', 'Simon Gama', 'ga3674@mca.ac.mw', 'BMIS', 3, 'gama1234', 0, '2025-08-20 18:53:07', NULL, 1),
(28, 'MCA/2024/126', 'Oscar Phiri', 'pr3971@mca.ac.mw', 'BMIS', 3, 'phiri1234', 0, '2025-08-20 18:54:21', NULL, 1),
(29, 'MCA/2024/127', 'Phillip Carter', 'ca6549@mca.ac.mw', 'BAAAIS', 4, 'carter1234', 0, '2025-08-20 18:55:41', NULL, 1),
(30, 'MCA/2024/128', 'Patrick Kumwenda', 'ku2780@mca.ac.mw', 'BBME', 4, 'kumwenda1234', 0, '2025-08-20 18:57:00', NULL, 1),
(31, 'MCA/2024/129', 'Linda Mwanza', 'mw1698@mca.ac.mw', 'BAAAIS', 4, 'mwanza1234', 0, '2025-08-20 18:58:14', NULL, 1),
(32, 'MCA/2024/130', 'Isaac Tembo', 'tb1159@mca.ac.mw', 'BMIS', 3, 'tembo1234', 0, '2025-08-20 18:59:35', NULL, 1),
(33, 'MCA/2024/131', 'Alice Brown', 'br3587@mca.ac.mw', 'BMIS', 3, 'brown1234', 0, '2025-08-20 19:00:47', NULL, 1),
(34, 'MCA/2024/132', 'Faith Peterson', 'pr4368@mca.ac.mw', 'BBME', 3, 'peterson1234', 0, '2025-08-20 19:02:06', NULL, 1),
(35, 'MCA/2024/133', 'Wesley Banda', 'ba5398@mca.ac.mw', 'BMPR', 4, 'banda1234', 0, '2025-08-20 19:03:53', NULL, 1),
(36, 'MCA/2024/134', 'Chikondi Zulu', 'zu6987@mca.ac.mw', 'BMPR', 4, 'zulu1234', 0, '2025-08-20 19:04:57', NULL, 1),
(37, 'MCA/2024/135', 'Martha Chuma', 'ch7098@mca.ac.mw', 'BMIS', 3, 'chuma1234', 0, '2025-08-20 19:06:32', NULL, 1),
(39, 'MCA/2024/140', 'Caroline Mwanza', 'mw7809@mca.ac.mw', 'BBME', 3, 'mwanza1234', 0, '2025-08-20 19:43:54', NULL, 1),
(40, 'MCA/2024/141', 'Jacob Kalinda', 'ka6701@mca.ac.mw', 'BMPR', 4, 'kalinda1234', 0, '2025-08-20 19:45:08', NULL, 1);

-- --------------------------------------------------------

--
-- Table structure for table `votes`
--

CREATE TABLE `votes` (
  `id` int(11) NOT NULL,
  `student_id` varchar(50) NOT NULL,
  `position_id` int(11) NOT NULL,
  `candidate_id` int(11) NOT NULL,
  `vote_timestamp` timestamp NOT NULL DEFAULT current_timestamp(),
  `ip_address` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin_users`
--
ALTER TABLE `admin_users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `candidates`
--
ALTER TABLE `candidates`
  ADD PRIMARY KEY (`id`),
  ADD KEY `position_id` (`position_id`),
  ADD KEY `student_id` (`student_id`);

--
-- Indexes for table `election_settings`
--
ALTER TABLE `election_settings`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `setting_name` (`setting_name`);

--
-- Indexes for table `positions`
--
ALTER TABLE `positions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `position_name` (`position_name`);

--
-- Indexes for table `students`
--
ALTER TABLE `students`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `student_id` (`student_id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `votes`
--
ALTER TABLE `votes`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_vote` (`student_id`,`position_id`),
  ADD KEY `position_id` (`position_id`),
  ADD KEY `candidate_id` (`candidate_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin_users`
--
ALTER TABLE `admin_users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `candidates`
--
ALTER TABLE `candidates`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT for table `election_settings`
--
ALTER TABLE `election_settings`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `positions`
--
ALTER TABLE `positions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `students`
--
ALTER TABLE `students`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=41;

--
-- AUTO_INCREMENT for table `votes`
--
ALTER TABLE `votes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `candidates`
--
ALTER TABLE `candidates`
  ADD CONSTRAINT `candidates_ibfk_1` FOREIGN KEY (`position_id`) REFERENCES `positions` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `candidates_ibfk_2` FOREIGN KEY (`student_id`) REFERENCES `students` (`student_id`) ON DELETE CASCADE;

--
-- Constraints for table `votes`
--
ALTER TABLE `votes`
  ADD CONSTRAINT `votes_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`student_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `votes_ibfk_2` FOREIGN KEY (`position_id`) REFERENCES `positions` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `votes_ibfk_3` FOREIGN KEY (`candidate_id`) REFERENCES `candidates` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
