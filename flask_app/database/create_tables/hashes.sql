CREATE TABLE IF NOT EXISTS `hashes` (
`hash_id`        int(11)        NOT NULL AUTO_INCREMENT 	COMMENT 'The hash id',
`blockchain_id`  int(11)        NOT NULL 	        COMMENT 'The blockchain id',
`hashes`         varchar(1000)  NOT NULL            	COMMENT 'The chain of the blockchain',
PRIMARY KEY  (`hash_id`),
FOREIGN KEY (blockchain_id) REFERENCES blockchain(blockchain_id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT="Blockchain for the nft";