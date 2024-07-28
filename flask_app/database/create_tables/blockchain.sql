CREATE TABLE IF NOT EXISTS `blockchain` (
`blockchain_id`  int(11)       NOT NULL AUTO_INCREMENT 	COMMENT 'The Blockchain id',
`image_id`       int(11)       NOT NULL 	        COMMENT 'The image id',
`chain`          varchar(10000)  NOT NULL            	COMMENT 'The chain of the blockchain',
PRIMARY KEY  (`blockchain_id`),
FOREIGN KEY (image_id) REFERENCES images(image_id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT="Blockchain for the nft";