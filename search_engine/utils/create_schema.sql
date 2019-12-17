CREATE DATABASE IF NOT EXISTS SearchEngine;

USE SearchEngine;

CREATE TABLE IF NOT EXISTS users (
  u_id INT AUTO_INCREMENT,
  u_name VARCHAR (255),
  PRIMARY KEY (u_id)
);

CREATE TABLE IF NOT EXISTS user_clicks (
  u_id INT,
  p_id VARCHAR (50),
  qry VARCHAR (255),
  duration decimal,
  CONSTRAINT fk_uid FOREIGN KEY (u_id) REFERENCES users (u_id)
);

CREATE TABLE IF NOT EXISTS ref_sels (
  u_id INT,
  p_id VARCHAR (50),
  qry VARCHAR (255),
  relevant BOOLEAN,
  PRIMARY KEY (u_id, p_id, qry),
  CONSTRAINT fk_uid_rel FOREIGN KEY (u_id) REFERENCES users (u_id)
);