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
  `corrected_avg_unique_accuracy` FLOAT NOT NULL,
  `avg_unique_accuracy` FLOAT NOT NULL,
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
  `rows` INT UNSIGNED NOT NULL,
  `skip_rows` INT UNSIGNED NOT NULL,
  `vectorizer` VARCHAR(255) NULL,
  `tokenizer` VARCHAR(255) NULL,
  `parameters` VARCHAR(1023) NULL,
  `normalized_mutual_info_score` DECIMAL(10, 8) NULL,
  `adjusted_mutual_info_score` DECIMAL(10, 8) NULL,
  `completeness_score` DECIMAL(10, 8) NULL,
  `estimated_clusters` INT NULL,
  `real_clusters` INT NULL,
  `n_noise` INT NULL,
  `time_clustering` INT NULL,
  `time_preprocessing` INT NULL,
  `time_total` INT NULL,
  `processed` TINYINT UNSIGNED NOT NULL,
  `failed` TINYINT UNSIGNED NULL,
  `date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
);

CREATE TABLE `data_database`.`script_execution` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `script` VARCHAR(255) NOT NULL,
  `last_processed_date` DATETIME NOT NULL,
  `failed` TINYINT UNSIGNED NULL,
  `log_message` LONGTEXT NULL,
  `processing_time` FLOAT NULL,
  `execution_date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
);

CREATE TABLE `data_database`.`cluster` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `identifier` TEXT NOT NULL,
  `method_evaluation_id` INT UNSIGNED NULL,
  `insert_date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

  CONSTRAINT `fk_method_evaluation_id`
    FOREIGN KEY (method_evaluation_id) REFERENCES method_evaluation (id)
	ON DELETE CASCADE,

  PRIMARY KEY (`id`)
);

CREATE TABLE `data_database`.`event` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `type` INT UNSIGNED NOT NULL,
  `cluster_id` INT UNSIGNED NOT NULL,
  `additional_information` LONGTEXT NULL,
  `insert_date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
);

CREATE TABLE `data_database`.`cluster_news_article` (
  `cluster_id` INT UNSIGNED NOT NULL,
  `news_article_id` INT UNSIGNED NOT NULL,
  `insert_date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

  CONSTRAINT `fk_cluster`
    FOREIGN KEY (cluster_id) REFERENCES cluster (id)
	ON DELETE CASCADE,
  CONSTRAINT `fk_news_article`
    FOREIGN KEY (news_article_id) REFERENCES news_article (id)
	ON DELETE CASCADE,

  PRIMARY KEY ( `cluster_id`, `news_article_id`)
);

CREATE TABLE `data_database`.`cron_evaluation` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `method` VARCHAR(255) NOT NULL,
  `rows` INT UNSIGNED NOT NULL,
  `skip_rows` INT UNSIGNED NOT NULL,
  `vectorizer` VARCHAR(255) NULL,
  `tokenizer` VARCHAR(255) NULL,
  `parameters` VARCHAR(1023) NULL,
  `normalized_mutual_info_score` DECIMAL(10, 8) NULL,
  `adjusted_mutual_info_score` DECIMAL(10, 8) NULL,
  `completeness_score` DECIMAL(10, 8) NULL,
  `estimated_clusters` INT NULL,
  `real_clusters` INT NULL,
  `n_noise` INT NULL,
  `time_clustering` INT NULL,
  `time_preprocessing` INT NULL,
  `time_total` INT NULL,
  `processed` TINYINT UNSIGNED NOT NULL,
  `failed` TINYINT UNSIGNED NULL,
  `date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
);

ALTER TABLE `data_database`.`news_article`
ADD COLUMN `text_without_stopwords` LONGTEXT NULL DEFAULT NULL AFTER `newspaper_text`;

ALTER TABLE `data_database`.`news_article`
ADD COLUMN `time_without_stopwords` INT NULL DEFAULT NULL AFTER `text_without_stopwords`;

ALTER TABLE `data_database`.`news_article`
ADD COLUMN `text_keyterms` LONGTEXT NULL DEFAULT NULL AFTER `time_without_stopwords`;

ALTER TABLE `data_database`.`news_article`
ADD COLUMN `time_keyterms` INT NULL DEFAULT NULL AFTER `text_keyterms`;

ALTER TABLE `data_database`.`news_article`
ADD COLUMN `text_entities` LONGTEXT NULL DEFAULT NULL AFTER `time_keyterms`;

ALTER TABLE `data_database`.`news_article`
ADD COLUMN `time_entities` INT NULL DEFAULT NULL AFTER `text_entities`;

ALTER TABLE `data_database`.`news_article`
ADD COLUMN `text_keyterms_and_entities` LONGTEXT NULL DEFAULT NULL AFTER `time_entities`;

ALTER TABLE `data_database`.`news_article`
ADD COLUMN `time_keyterms_and_entities` INT NULL DEFAULT NULL AFTER `text_keyterms_and_entities`;

ALTER TABLE `data_database`.`news_article`
ADD COLUMN `text_stemmed` LONGTEXT NULL DEFAULT NULL AFTER `time_keyterms_and_entities`;

ALTER TABLE `data_database`.`news_article`
ADD COLUMN `time_stemmed` INT NULL DEFAULT NULL AFTER `text_stemmed`;

ALTER TABLE `data_database`.`news_article`
ADD COLUMN `text_lemmatized` LONGTEXT NULL DEFAULT NULL AFTER `time_stemmed`;

ALTER TABLE `data_database`.`news_article`
ADD COLUMN `time_lemmatized` INT NULL DEFAULT NULL AFTER `text_lemmatized`;

ALTER TABLE `data_database`.`news_article`
ADD COLUMN `preprocessed` TINYINT UNSIGNED NOT NULL DEFAULT 0 AFTER `title_keywords_intersection`;

ALTER TABLE `data_database`.`news_article`
ADD COLUMN `preprocessing_failed` TINYINT UNSIGNED NOT NULL DEFAULT 0 AFTER `preprocessed`;

ALTER TABLE `data_database`.`news_article`
ADD COLUMN `newspaper_publish_date` DATETIME NULL DEFAULT NULL AFTER `newspaper_processed`;

ALTER TABLE `data_database`.`news_article`
ADD COLUMN `text_stemmed_without_stopwords` LONGTEXT NULL DEFAULT NULL AFTER `time_stemmed`;

ALTER TABLE `data_database`.`news_article`
ADD COLUMN `time_stemmed_without_stopwords` INT NULL DEFAULT NULL AFTER `text_stemmed_without_stopwords`;

ALTER TABLE `data_database`.`news_article`
ADD COLUMN `text_lemmatized_without_stopwords` LONGTEXT NULL DEFAULT NULL AFTER `time_lemmatized`;

ALTER TABLE `data_database`.`news_article`
ADD COLUMN `time_lemmatized_without_stopwords` INT NULL DEFAULT NULL AFTER `text_lemmatized_without_stopwords`;

ALTER TABLE `data_database`.`news_article`
ADD COLUMN `text_stemmed_without_stopwords_aggr` LONGTEXT NULL DEFAULT NULL AFTER `time_stemmed_without_stopwords`;

ALTER TABLE `data_database`.`news_article`
ADD COLUMN `time_stemmed_without_stopwords_aggr` INT NULL DEFAULT NULL AFTER `text_stemmed_without_stopwords_aggr`;

ALTER TABLE `data_database`.`news_article`
ADD COLUMN `text_lemmatized_without_stopwords_aggr` LONGTEXT NULL DEFAULT NULL AFTER `time_lemmatized_without_stopwords`;

ALTER TABLE `data_database`.`news_article`
ADD COLUMN `time_lemmatized_without_stopwords_aggr` INT NULL DEFAULT NULL AFTER `text_lemmatized_without_stopwords_aggr`;
