CREATE TABLE IF NOT EXISTS `tokens` (
`token_id`      int(11)      NOT NULL auto_increment	  COMMENT 'the id of this token',
`string_key`           varchar(40)  NOT NULL            		  COMMENT 'the id of the key',
`token`         int(11)      NOT NULL                   COMMENT 'the token amount',
PRIMARY KEY (`token_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT="Tokens of the site";