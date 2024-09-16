CREATE DATABASE studentcollector;

CREATE USER student_admin WITH PASSWORD 'password';

GRANT ALL PRIVILEGES ON DATABASE studentcollector TO student_admin;