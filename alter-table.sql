-- Adminer 4.8.1 MySQL 8.0.33 dump

SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

SET NAMES utf8mb4;

DROP TABLE IF EXISTS `berita`;
CREATE TABLE `berita` (
  `prediksi` varchar(75) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `id` int NOT NULL AUTO_INCREMENT,
  `judul` varchar(255) NOT NULL,
  `kategori` varchar(75) NOT NULL,
  `hasil` varchar(10) NOT NULL,
  `isi` text NOT NULL,
  `data` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- 2024-05-15 16:09:02


ALTER TABLE `berita`
ADD `user_id` int NOT NULL DEFAULT '1',
ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

ALTER TABLE `uploaders`
ADD `user_id` int NULL,
ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);