
ALTER TABLE phonebook
ADD COLUMN birthday DATE;

CREATE TABLE groups (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

ALTER TABLE phonebook
ADD COLUMN group_id INTEGER REFERENCES groups(id);

INSERT INTO groups (name) VALUES
('Family'),
('Work'),
('Friend'),
('Other');
