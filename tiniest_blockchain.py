#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 22 22:30:04 2018

@author: abhishek
"""
#tiny blockchain code
# each block is stored with a timestamp and optionally an index
# Coin is named as BoseCoin (contains timestamp and index)
#And to help ensure integrity throughout the blockchain, each block will have a self-identifying hash. 
#ach block’s hash will be a cryptographic hash of the block’s index, timestamp, data, 
#and the hash of the previous block’s hash

import hashlib as hasher
import datetime as date
class Block:
    def __init__(self,index,timestamp,data,previous_hash):
        self.index=index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.hash_block()
        
    def hash_block(self):
        sha = hasher.sha256()
        sha.update(str(self.index).encode('utf-8') + 
           str(self.timestamp).encode('utf-8') + 
           str(self.data).encode('utf-8') + 
           str(self.previous_hash).encode('utf-8'))
        return sha.hexdigest()
    
#block structure is defined above
#Defining the first block or the genesis block

def create_genesis_block():
    #Manually construct a block with zero index and arbitrary previous hash
    return Block(0,date.datetime.now(),"Genesis Block","0")

def next_block(last_block):
    this_index = last_block.index + 1
    this_timestamp = date.datetime.now()
    this_data = "Hey! I'm block " + str(this_index)
    this_hash = last_block.hash
    return Block(this_index, this_timestamp, this_data, this_hash)

#Let's create the blockchain
#first block is the genesis block

blockchain = [create_genesis_block()]
previous_block = blockchain[0]

#Let the number of blocks be twenty
num_of_blocks = 20

#Add blocks to chain

for i in range(0,num_of_blocks):
    block_to_add = next_block(previous_block)
    blockchain.append(block_to_add)
    previous_block = block_to_add
    print("Block #{} has been added to the blockchain!".format(block_to_add.index))
    print("Hash: {}\n".format(block_to_add.hash))












