DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS buildings;
DROP TABLE IF EXISTS schools;
DROP TABLE IF EXISTS classrooms;
DROP TABLE IF EXISTS course_slots;
DROP TABLE IF EXISTS domains;
DROP TABLE IF EXISTS classroom_availability;

CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email VARCHAR(50) UNIQUE NOT NULL,
  password VARCHAR(25) NOT NULL,
  school_id INTEGER,
  school_name VARCHAR(100) NOT NULL,
  FOREIGN KEY (school_id) references schools (id)
);

CREATE TABLE buildings (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name VARCHAR(50) NOT NULL,
  slug VARCHAR(5) NOT NULL,
  school_id INTEGER,
  school_name VARCHAR(100) NOT NULL,
  FOREIGN KEY (school_id) references schools (id)
);

CREATE TABLE schools (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name VARCHAR(50) NOT NULL,
  tz_offset VARCHAR(3) NOT NULL
);

CREATE TABLE classrooms (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  room_number VARCHAR(5) NOT NULL,
  capacity INTEGER NULL,
  building_id INTEGER,
  school_id INTEGER,
  building_name VARCHAR(50) NOT NULL,
  school_name VARCHAR(50) NOT NULL,
  FOREIGN KEY (school_id) references schools (id),
  FOREIGN KEY (building_id) references buildings (id)
);

CREATE TABLE classroom_availability (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  classroom_id INTEGER,
  classroom_number VARCHAR(10) NOT NULL,
  building_id INTEGER,
  school_id INTEGER,
  building_name VARCHAR(50) NOT NULL,
  school_name VARCHAR(50) NOT NULL,
  start_time DATETIME NOT NULL,
  end_time DATETIME NOT NULL,
  weekday VARCHAR(10) NOT NULL,

  FOREIGN KEY (school_id) references schools (id),
  FOREIGN KEY (classroom_id) references classrooms (id),
  FOREIGN KEY (building_id) references buildings (id)
);

CREATE TABLE course_slots (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  start_time DATETIME NOT NULL,
  end_time DATETIME NOT NULL,
  weekday VARCHAR(10) NOT NULL,
  school_id INTEGER,
  building_id INTEGER,
  classroom_id INTEGER,
  classroom_number VARCHAR(10) NOT NULL,
  building_name VARCHAR(50) NOT NULL,
  school_name VARCHAR(50) NOT NULL,

  FOREIGN KEY (school_id) references schools (id),
  FOREIGN KEY (building_id) references buildings (id),
  FOREIGN KEY (classroom_id) references classrooms (id)
);

CREATE TABLE domains (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  site VARCHAR(50) UNIQUE NOT NULL
);