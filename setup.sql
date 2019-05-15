CREATE TABLE IF NOT EXISTS jsonobjects (
    id INT AUTO_INCREMENT,
    pid INT,
    type VARCHAR(16),
    json VARCHAR(2048),
    ts TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3),
    skey VARCHAR(16) DEFAULT null,
    PRIMARY KEY (id)
) ENGINE = MEMORY;
