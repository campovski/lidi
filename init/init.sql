-- Create database with UTF8 encoding.
CREATE DATABASE lidi_db ENCODING 'UTF8';

-- Create admin for database and grant permissions. Remember to change
-- password later!
CREATE ROLE admin_lidi;
ALTER ROLE admin_lidi WITH PASSWORD 'testpwd1';
GRANT ALL PRIVILEGES ON DATABASE lidi_db TO admin_lidi;
ALTER ROLE admin_lidi WITH LOGIN;
