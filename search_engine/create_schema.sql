CREATE DATABASE IF NOT EXISTS SearchEngine;

USE SearchEngine;

CREATE TABLE IF NOT EXISTS users (
  u_id INT AUTO_INCREMENT,
  u_name VARCHAR (255),
  PRIMARY KEY (u_id)
);

CREATE TABLE IF NOT EXISTS rel_scores (
  u_id INT,
  p_id VARCHAR (50),
  qry VARCHAR (255),
  click_score INT DEFAULT 0,
  rel_score INT DEFAULT 1,
  PRIMARY KEY (u_id, p_id, qry),
  CONSTRAINT fk_uid FOREIGN KEY (u_id) REFERENCES users (u_id)
);