import datetime
import json
import hashlib
from flask import Flask,jsonify

class Blockchain:
    def __init__(self):
        #keep block group
        self.chain = [] #list keep block
        self.transaction = 0
        #genesis block
        self.create_block(nonce=1,previous_hash="0")
        
        
    #for create block into system
    def create_block(self,nonce,previous_hash):
        #เก็บส่วนประกอบของ block แต่ละ block
        block = {
            "index":len(self.chain)+1,
            "timestamp":str(datetime.datetime.now()),
            "nonce":nonce,
            "data": self.transaction,
            "previous_hash":previous_hash
        }
        self.chain.append(block)
        return block
    
    #service about block
    def get_previous_block(self):
        return self.chain[-1]

    #encrypt block
    def hash(self,block):
        #sort data in block and covert py obj to json obj
        encode_block = json.dumps(block,sort_keys=True).encode()
        #sha-256
        return hashlib.sha256(encode_block).hexdigest()

    def proof_of_work(self,previous_nonce):
        #need nonce for taget hash 4 positon = 0000xxxxxx
        new_nonce=1 #nonce needed
        check_proof = False #check nonce same target

        #problem solving in mathematic
        while check_proof is False:
            #hexa decimal 1 set
            hashoperation = hashlib.sha256(str(new_nonce**2 - previous_nonce**2).encode()).hexdigest()
            if hashoperation[:4] == "0000":
                check_proof = True
            else:
                new_nonce += 1
        return new_nonce

    def is_chain_valid(self,chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block["previous_hash"] != self.hash(previous_block):
                return False

            previous_nonce = previous_block["nonce"] # nonce block ก่อนหน้า
            nonce = block["nonce"] 
            # nonce ของ block ที่ตรวจสอบ
            hashoperation = hashlib.sha256(str(nonce**2 - previous_nonce**2).encode()).hexdigest()
            if hashoperation[:4] != "0000":
                return False
            previous_block=block
            block_index+=1
        return True


#web server
app = Flask(__name__)
#using blockchain
blockchain = Blockchain()

@app.route('/')
def hello():
    return "<h1> Hello Blockchain </h1>"


@app.route('/get_chain', methods=["GET"])
def get_chain():
    response = {
        "chain": blockchain.chain,
        "length": len(blockchain.chain)
    }
    return jsonify(response), 200


@app.route('/mining' , methods=["GET"])
def mining_block():
    amount = 1000000  # จำนวนเงินในการทำธุรกรรม
    blockchain.transaction = blockchain.transaction+amount
    #pow
    previous_block = blockchain.get_previous_block()
    previous_nonce = previous_block["nonce"]
    #nonce
    nonce = blockchain.proof_of_work(previous_nonce)
    #hash block ก่อนหน้า
    previous_hash = blockchain.hash(previous_block)
    #update block ใหม่
    block = blockchain.create_block(nonce, previous_hash)
    response = {
        "message": "Mining Block เรียบร้อย",
        "index": block["index"],
        "timestamp": block["timestamp"],
        "data": block["data"],
        "nonce": block["nonce"],
        "previous_hash": block["previous_hash"]
    }
    return jsonify(response), 200


@app.route('/is_valid', methods=["GET"])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {"message": "Blockchain Is Valid"}
    else:
        response = {"message": "Have Problem , Blockchain Is Not Valid"}
    return jsonify(response), 200


#run server
if __name__ == "__main__":
    app.run()
