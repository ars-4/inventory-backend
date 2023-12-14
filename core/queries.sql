CREATE DATABASE stock;
CREATE USER stock WITH PASSWORD 'stock';
GRANT ALL PRIVILEGES ON DATABASE stock TO stock;
GRANT USAGE,CREATE ON SCHEMA public TO stock;
CREATE TABLE logs(
    id SERIAL PRIMARY KEY,
    message TEXT
);