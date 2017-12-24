########################################
#
# blockchain.py
#
# Description: create a block chain
#
#
# Author: Josh Fernandes
#
# Created: Dec 23, 2017
#
# Updated:
#
#
########################################
import hashlib as hasher
import datetime as date

class Block:

    def __init__(self,index,timestamp,data,previous_hash):
        self.index          = index
        self.timestamp      = timestamp
        self.data           = data
        self.previous_hash  = previous_hash
        self._hash          = self.hash_def()

    def __repr__(self):
        return 'This is block {}'.format(self.index)

    def __str__(self):
        return 'the block hash is {}'.format(self._hash)

    def hash_def(self):
        sha = hasher.sha256()
        sha.update(str(self.index).encode('utf-8') +
                    str(self.timestamp).encode('utf-8') +
                    str(self.data).encode('utf-8') +
                    str(self.previous_hash).encode('utf-8'))
        return sha.hexdigest()


##########################################

b = Block(0,date.datetime.now(),"genesis block", "0")

print(b) #print returns what is in __str__ method

blockchain = [b]

next_b = Block(len(blockchain), date.datetime.now(),"next block",blockchain[-1]._hash)

blockchain.append(next_b)
print(next_b)


final_b = Block(len(blockchain), date.datetime.now(),"final block",blockchain[-1]._hash)
blockchain.append(final_b)
print(final_b)

print('\n the blockcahin is \n' + repr(blockchain) + '\n') #str() method or repr() returns __repr__
