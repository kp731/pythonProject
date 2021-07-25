CREATE DATABASE airtravel;
use airtravel;


CREATE TABLE IF NOT EXISTS airtravel (
    `id` int AUTO_INCREMENT PRIMARY KEY,
    `Month` VARCHAR(3) CHARACTER SET utf8,
    `Column_1958` INT,
    `Column_1959` INT,
    `Column_1960` INT
);
INSERT INTO airtravel VALUES
    (1, 'JAN',  340,  360,  417),
    (2, 'FEB',  318,  342,  391),
    (3, 'MAR',  362,  406,  419),
    (4, 'APR',  348,  396,  461),
    (5, 'MAY',  363,  420,  472),
    (6, 'JUN',  435,  472,  535),
    (7, 'JUL',  491,  548,  622),
    (8, 'AUG',  505,  559,  606),
    (9, 'SEP',  404,  463,  508),
    (10,'OCT',  359,  407,  461),
    (11,'NOV',  310,  362,  390),
    (12,'DEC',  337,  405,  432);