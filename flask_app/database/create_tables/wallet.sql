CREATE TABLE IF NOT EXISTS `wallet` (
`wallet_id`       int(11)      NOT NULL AUTO_INCREMENT	  COMMENT 'the id of this wallet',
`user_id`         int(11)      NOT NULL                   COMMENT 'the id of the user',
`string_key`             varchar(40)  NOT NULL            		  COMMENT 'the key of the wallet',
PRIMARY KEY (`wallet_id`),
FOREIGN KEY (user_id) REFERENCES users(user_id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT="Wallet of the site";


