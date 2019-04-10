CREATE DATABASE `data_database` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE `data_database`.`news_article` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(255) NULL,
  `url` VARCHAR(1023) NULL,
  `publisher` VARCHAR(255) NULL,
  `category` VARCHAR(255) NULL,
  `story` VARCHAR(255) NULL,
  `hostname` VARCHAR(255) NULL,
  `date` DATETIME NULL,
  `newspaper_processed` TINYINT UNSIGNED NOT NULL,
  `newspaper_meta_language` VARCHAR(16) NULL,
  `newspaper_keywords` LONGTEXT NULL,
  `newspaper_text` LONGTEXT NULL,
  `title_keywords_intersection` TINYINT UNSIGNED NULL,
  PRIMARY KEY (`id`)
);

ALTER TABLE `data_database`.`news_article`
ADD INDEX `idx_title` (`title` ASC),
ADD INDEX `idx_date` (`date` ASC);
