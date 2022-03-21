-- import to SQLite by running: sqlite3.exe db.sqlite3 -init sqlite.sql

-- PRAGMA journal_mode = MEMORY;
-- PRAGMA synchronous = OFF;
-- PRAGMA foreign_keys = OFF;
-- PRAGMA ignore_check_constraINTEGERs = OFF;
-- PRAGMA auto_vacuum = NONE;
-- PRAGMA secure_delete = OFF;
BEGIN TRANSACTION;

-- Drop all tables
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Users_files;
DROP TABLE IF EXISTS Modules;
DROP TABLE IF EXISTS Users_modules;
DROP TABLE IF EXISTS Feedback_post;
DROP TABLE IF EXISTS Feedback_type;


CREATE TABLE Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name STRING NOT NULL,
    username STRING NOT NULL UNIQUE,
    email STRING UNIQUE,
    password STRING NOT NULL,
    created_at DATE NOT NULL
);
CREATE TABLE Users_files (
    id INTEGER PRIMARY KEY AUTOINCREMENT ,
    filename STRING NOT NULL UNIQUE,
    file_type STRING NOT NULL,
    created_at DATE NOT NULL
);
CREATE TABLE Modules (
    id INTEGER PRIMARY KEY AUTOINCREMENT ,
    name STRING NOT NULL UNIQUE,
    description STRING NOT NULL,
    created_at DATE NOT NULL
);
CREATE TABLE Users_modules (
    id INTEGER PRIMARY KEY AUTOINCREMENT ,
    user_id INTEGER NOT NULL,
    module_id INTEGER NOT NULL
);
CREATE TABLE Feedback_post (
    id INTEGER PRIMARY KEY AUTOINCREMENT ,
    type_id INTEGER NOT NULL,
    title STRING NOT NULL,
    post TEXT NOT NULL,
    created_at DATE NOT NULL,
    done BOOLEAN NOT NULL,
    user_id INTEGER
);
CREATE TABLE Feedback_type (
    id INTEGER PRIMARY KEY AUTOINCREMENT ,
    name STRING NOT NULL UNIQUE,
    created_at DATE NOT NULL
);
-- ALTER TABLE Users_files ADD CONSTRAINTEGER Users_files_fk0 FOREIGN KEY (user_id) REFERENCES Users(id);
-- ALTER TABLE Users_modules ADD CONSTRAINTEGER Users_modules_fk0 FOREIGN KEY (user_id) REFERENCES Users(id);
-- ALTER TABLE Users_modules ADD CONSTRAINTEGER Users_modules_fk1 FOREIGN KEY (module_id) REFERENCES Modules(id);
-- ALTER TABLE Feedback_post ADD CONSTRAINTEGER Feedback_post_fk0 FOREIGN KEY (user_id) REFERENCES Users(id);
-- ALTER TABLE Feedback_post ADD CONSTRAINTEGER Feedback_post_fk1 FOREIGN KEY (type_id) REFERENCES Feedback_type(id);





COMMIT;
PRAGMA ignore_check_constraINTEGERs = ON;
PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;
PRAGMA synchronous = NORMAL;
