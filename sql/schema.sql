-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema friends_db
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema friends_db
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `friends_db` DEFAULT CHARACTER SET utf8 ;
USE `friends_db` ;

-- -----------------------------------------------------
-- Table `friends_db`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `friends_db`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NULL,
  `alias` VARCHAR(45) NULL,
  `email` VARCHAR(255) NULL,
  `pw_hash` VARCHAR(255) NULL,
  `birthday` VARCHAR(255) NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `friends_db`.`friends`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `friends_db`.`friends` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  `user_id` INT NOT NULL,
  `friends_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_friends_users_idx` (`user_id` ASC),
  INDEX `fk_friends_friends1_idx` (`friends_id` ASC),
  CONSTRAINT `fk_friends_users`
    FOREIGN KEY (`user_id`)
    REFERENCES `friends_db`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_friends_friends1`
    FOREIGN KEY (`friends_id`)
    REFERENCES `friends_db`.`friends` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
