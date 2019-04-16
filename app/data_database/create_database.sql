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

CREATE TABLE `data_database`.`method_evaluation` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `method` VARCHAR(255) NOT NULL,
  `sample_size` INT NOT NULL,
  `vectorizer` VARCHAR(255) NOT NULL,
  `tokenizer` VARCHAR(255) NULL,
  `parameters` VARCHAR(1023) NULL,
  `normalized_mutual_info_score` FLOAT NOT NULL,
  `adjusted_mutual_info_score` FLOAT NOT NULL,
  `completeness_score` FLOAT NOT NULL,
  `estimated_clusters` INT NOT NULL,
  `real_clusters` INT NOT NULL,
  `n_noise` INT NOT NULL,
  `processing_time` FLOAT NULL,
  `date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
);

CREATE TABLE `data_database`.`cron_evaluation` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `method` VARCHAR(255) NOT NULL,
  `rows` UNSIGNED INT NOT NULL,
  `skip_rows` UNSIGNED INT NOT NULL,
  `vectorizer` VARCHAR(255) NULL,
  `tokenizer` VARCHAR(255) NULL,
  `parameters` VARCHAR(1023) NULL,
  `normalized_mutual_info_score` DECIMAL(10, 8) NOT NULL,
  `adjusted_mutual_info_score` DECIMAL(10, 8) NOT NULL,
  `completeness_score` DECIMAL(10, 8) NOT NULL,
  `estimated_clusters` INT NOT NULL,
  `real_clusters` INT NOT NULL,
  `n_noise` INT NOT NULL,
  `time_clustering` INT NULL,
  `time_preprocessing` INT NULL,
  `time_total` INT NULL,
  `date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `processed` TINYINT UNSIGNED NOT NULL,
  `failed` TINYINT UNSIGNED NOT NULL,
  PRIMARY KEY (`id`)
);
