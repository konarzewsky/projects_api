CREATE TABLE IF NOT EXISTS projects (
  id SERIAL PRIMARY KEY,
  name VARCHAR(32) NOT NULL,
  description VARCHAR,
  date_start TIMESTAMP NOT NULL,
  date_end TIMESTAMP NOT NULL,
  area JSON NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT now(),
  updated_at TIMESTAMP NOT NULL DEFAULT now()
);