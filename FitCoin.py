#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 27 01:23:10 2018

@author: abhishek
"""

#All transactions are in the json format.Contains a to,from and amount sent.
#Each block's field will be a list of transactions

"""
we’ll create a simple HTTP server so that any user can 
let our nodes know that a new transaction has occurred. 
A node will be able to accept a POST request with a transaction (
like above) as the request body. 
"""

from flask import Flask
from flask import request
from tiniest_blockchain import Block
from tiniest_blockchain import create_genesis_block
from tiniest_blockchain import next_block
import hashlib as hasher
import datetime as date
import json
import requests

    
node = Flask(__name__)
peer_nodes = []
# A variable to deciding if we're mining or not
mining = True

# Store the transactions that
# this node has in a list
this_nodes_transactions = []

@node.route('/txion',methods=['POST'])
def transaction():
    if request.method == 'POST':
        #on each new request we 
        #extract the transaction data
        new_txion = request.get_json()
        this_nodes_transactions.append(new_txion)
        #for successfull transaction
        print("New transaction")
        print("From: {}".format(new_txion['from']))
        print("To: {}".format(new_txion['to']))
        print("Amount: {}".format(new_txion['amount']))
        #send acknowledgment
        return "Transaction submission successfull\n"   


"""
 A Proof-of-Work algorithm is essentially 
 an algorithm that generates an item that is 
 difficult to create but easy to verify
"""

#creating a proof of work algorithm for mining

blockchain = [create_genesis_block()]
#previous_block = blockchain[0]
#
##Let the number of blocks be twenty
#num_of_blocks = 30

#Add blocks to chain

#for i in range(0,num_of_blocks):
#    block_to_add = next_block(previous_block)
#    blockchain.append(block_to_add)
#    previous_block = block_to_add
#    print("Block #{} has been added to the blockchain!".format(block_to_add.index))
#    print("Hash: {}\n".format(block_to_add.hash))


miner_address = "q3nf394hjg-random-miner-address-34nf3i4nflkn3oi"


#mining function which creates a new coin when the incrementor number is divisible by 9 and the proof number of last block
def proof_of_work(last_proof):
    incrementor = last_proof+1
    while not (incrementor % 9 ==0 and incrementor % (last_proof+1) ==0):
        incrementor+=1
        
    return incrementor

@node.route('/mine',methods=['GET'])
def mine():
    #get the last proof of work
    last_block = blockchain[len(blockchain)-1]  
    last_proof = last_block.data['proof-of-work']
    proof = proof_of_work(last_proof)
    # Once we find a valid proof of work,
  # we know we can mine a block so 
  # we reward the miner by adding a transaction
    this_nodes_transactions.append(
    { "from": "network", "to": miner_address, "amount": 1 }
  )
    # Now we can gather the data needed
  # to create the new block
    new_block_data = {
    "proof-of-work": proof,
    "transactions": list(this_nodes_transactions)
  }
    new_block_index = last_block.index + 1
    new_block_timestamp = this_timestamp = date.datetime.now()
    last_block_hash = last_block.hash
    this_nodes_transactions[:] = []
    #now creating the new block
    mined_block = Block(new_block_index,new_block_timestamp,new_block_data,last_block_hash)
    blockchain.append(mined_block)
    #let the client know we mined a block
    return json.dumps({
      "index": new_block_index,
      "timestamp": str(new_block_timestamp),
      "data": new_block_data,
      "hash": last_block_hash
  }) + "\n"
    
    
#to make it decentralized , we make each node broadcast it's version of the chain
#to the others to recieve the chains of other nodes
#After that each node has to verify the other nodes' chains so that every node in the network
#can come to a consensus of what the resulting blockchain will look like
#this is called the consensus algorithm




"""
Consensus algorithm: if a nodes chain is different from another's , the the longest chain in the
network stays and the shorter chains will be deleted
If there is no conflict between the chains in our network then we carry on
"""


@node.route('/blocks', methods=['GET'])
def get_blocks():
  chain_to_send = blockchain
  # Convert our blocks into dictionaries
  # so we can send them as json objects later
  for i in range(len(chain_to_send)):
    block = chain_to_send[i]
    block_index = str(block.index)
    block_timestamp = str(block.timestamp)
    block_data = str(block.data)
    block_hash = block.hash
    chain_to_send[i] = {
      "index": block_index,
      "timestamp": block_timestamp,
      "data": block_data,
      "hash": block_hash
    }
  chain_to_send = json.dumps(chain_to_send)
  return chain_to_send



def find_new_chains():
  # Get the blockchains of every
  # other node
  other_chains = []
  for node_url in peer_nodes:
    # Get their chains using a GET request
    block = requests.get(node_url + "/blocks").content
    # Convert the JSON object to a Python dictionary
    block = json.loads(block)
    # Add it to our list
    other_chains.append(block)
  return other_chains

def consensus():
  # Get the blocks from other nodes
  other_chains = find_new_chains()
  # If our chain isn't longest,
  # then we store the longest chain
  longest_chain = blockchain
  for chain in other_chains:
    if len(longest_chain) < len(chain):
      longest_chain = chain
  # If the longest chain wasn't ours,
  # then we set our chain to the longest
  blockchain = longest_chain
  
    
node.run()