from hashlib import sha256
from datetime import datetime
import json
import requests
from flask import request

from ..database.database import database

db = database()

class Block:
    def __init__(self, index, time_stamp, transactions, previous_hash, work_proof=0):
        self.index = index

        
        self.time_stamp = time_stamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.work_proof = work_proof

    """ A block is the hash of a string including proof of work"""

    @property 
    def hash(self):

        block_to_hash = str(self.index) + str(self.time_stamp) + str(self.transactions) + str(self.previous_hash) + str(self.work_proof)

        return sha256(block_to_hash.encode()).hexdigest()
    
    """ turns the block class into a dictionary object"""
    def to_dict(self):
        return {'index': self.index, 'time_stamp': self.time_stamp, 'transactions' : self.transactions, 'prevous_hash' : self.previous_hash, 'work_proof' : self.work_proof}
    
    """ Get a dictionary turns it into block class"""
    @classmethod
    def from_dict(cls, data):
        return cls(data['index'], data['time_stamp'],data['transactions'], data['prevous_hash'], data['work_proof'])
                                       
class Blockchain:

    def __init__(self, zeros_leading, new_transactions, chain):

        
        self.zeros_leading = zeros_leading
        self.new_transactions = new_transactions
        self.chain = chain
        
        #if chain is empty this is the first time making the blockchain so need to make a genesis block
        if len(chain) == 0:
            self.new_transactions = []
            self.generate_genesis_block(new_transactions)
        
        
        """A genesis block is the first block in a blockchain, its previous hash would be 0.
        Start with a genesis block by calling Block(0, str(0), [], 0, 0) and appending it to the start of chain""" 
    def generate_genesis_block(self, dictionary):
        block = Block(0, datetime.now().strftime("%m/%d/%Y %H:%M:%S"), {"starting owner":dictionary["owner"], "currentOwner":dictionary["owner"],"image_name":dictionary["image_name"]}, 0, 0)

        self.chain.append(block)
        
        
        """A block is added to the chain in blockchain if the previous hash is valid and the proof of work is valid""" 
    def append_block(self, block):
        if(self.check_proof_of_work_valididty(self.chain[-1])):
            self.chain.append(block)
        
        
        
        """First check if there are any pending new blocks, then determine if the transaction came from a valid logged in user with a valid key. 
        A new transaction is only added in a block by first finding a valid proof of work after which the block is appended to the chain. 
        A proof of work will be valid if the given hash starts with 2 leading zeros. Flush out new transactions array in the end and return new block """
    def mine_transaction(self, transaction):

        if len(self.new_transactions) == 0: 
            if(self.check_transaction_validity(transaction)):


                block = Block(self.zeros_leading,datetime.now().strftime("%m/%d/%Y %H:%M:%S"),transaction,self.chain[-1].hash)
                self.new_transactions.append(block)


                jsnDump = json.dumps(self.to_dict())

                #updates the blockchain in the database to tell that a mining is taking place
                db.query(f"UPDATE blockchain SET chain = '{jsnDump}' WHERE image_id = '{transaction['image_id']}'")

                while block.hash[0] != "0":
                    block.work_proof += 1
                

                self.append_block(block)
                self.new_transactions.clear()
                self.zeros_leading = self.zeros_leading + 1
                jsnDump = json.dumps(self.to_dict())
                db.query(f"UPDATE blockchain SET chain = '{jsnDump}' WHERE image_id = '{transaction['image_id']}'")

                #tells the database the mining is done and adds the hash to the hash list in the database

                blockchain = db.query(f"SELECT *from blockchain WHERE image_id = '{transaction['image_id']}'")[0]
                hashes = db.query(f"SELECT *from hashes WHERE blockchain_id = '{blockchain['blockchain_id']}'")[0]

                hashesChain = json.loads(hashes["hashes"])

                hashesChain.append(block.hash)

                
                db.query(f"UPDATE hashes SET hashes = '{json.dumps(hashesChain)}' WHERE hash_id = '{hashes['hash_id']}'")

                return block


        
        """To verify transaction validity, just match the two sets of keys for the user requesting transaction""" 
    def check_transaction_validity(self, transaction):
        sellerKey = db.query(f"SELECT * from wallet WHERE user_id = '{transaction['sellerID']}'")[0]
        buyerKey = db.query(f"SELECT * from wallet WHERE user_id = '{transaction['buyerID']}'")[0]



        if len(db.query(f"SELECT * from tokens WHERE string_key = '{sellerKey['string_key']}'")) and len(db.query(f"SELECT * from tokens WHERE string_key = '{buyerKey['string_key']}'")):
            return True
        
        return False
        
        """A proof of work is valid if the given hash starts with a leading O"""
    def check_proof_of_work_valididty(self, block):
        if block.hash[0] == "0" or block == self.chain[0]:
            return True
        return False
    
    
        
        """ To validate entire blockchain excluding the genesis block. A chain is valid if all blocks have valid proof of work"""
    def check_chain_validity(self):

        for block in range(1,len(self.chain)):
            if self.chain[block].hash[0] != "0":
                return False
            
        return True

    """ turns the blockchain class into a dictionary object"""
    def to_dict(self):
        returnDict = dict()
        
        returnDict["zero_leading"] = self.zeros_leading
        returnDict["new_transaction"] =  [item.to_dict() for item in self.new_transactions]
        returnDict['chain'] = [item.to_dict() for item in self.chain]

        return returnDict
    
    """ Get a dictionary turns it into blockchain class"""
    @classmethod
    def from_dict(cls, data):
        chain = [Block.from_dict(chain) for chain in data['chain']]
        zero_leading = data["zero_leading"]
        new_transaction = [Block.from_dict(item) for item in data['new_transaction']]

        return cls(zero_leading,new_transaction,chain)
        
