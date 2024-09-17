CREATE DATABASE coursecollector;

CREATE USER course_admin WITH PASSWORD 'password';

GRANT ALL PRIVILEGES ON DATABASE coursecollector TO course_admin;