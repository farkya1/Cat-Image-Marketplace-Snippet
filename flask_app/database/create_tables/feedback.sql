CREATE TABLE IF NOT EXISTS `feedback` (
`feedback_id`        int(11)       NOT NULL AUTO_INCREMENT 	COMMENT 'The feedback id',
`name`           varchar(100)  NOT NULL                	COMMENT 'The name of the commenter',
`email`          varchar(100)  NOT NULL                	COMMENT 'The email of the commenter',
`feedback`        varchar(500)  NOT NULL                	COMMENT 'The feedback',
PRIMARY KEY  (`feedback_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT="Comments left on the website";