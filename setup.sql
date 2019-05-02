CREATE TABLE IF NOT EXISTS jsonobjects (
    id INT AUTO_INCREMENT,
    pid INT,
    type VARCHAR(16),
    json VARCHAR(2048),
    PRIMARY KEY (id)
) ENGINE = MEMORY;
