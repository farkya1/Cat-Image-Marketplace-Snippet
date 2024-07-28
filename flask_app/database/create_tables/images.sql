CREATE TABLE IF NOT EXISTS `images` (
`image_id`       int(11)      NOT NULL AUTO_INCREMENT 	COMMENT 'The image id',
`image_name`     varchar(100)  NOT NULL                	COMMENT 'The filename of the image',
`description`    varchar(100)  NOT NULL                	COMMENT 'The description of the image',
`tokens`         int(11)       NOT NULL                 COMMENT 'The token cost of the image',
`user_id`        int(11)       NOT NULL            	    COMMENT 'The owner of the image',
PRIMARY KEY  (`image_id`),
FOREIGN KEY (user_id) REFERENCES users(user_id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT="Images of the nft";