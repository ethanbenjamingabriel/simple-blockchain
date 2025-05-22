import datetime
import hashlib
import json

class Blockchain:

    def __init__(self):
        self.chain = []
        self.create_block(proof=1, previous_hash='0')

    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'proof': proof,
            'previous_hash': previous_hash
        }
        block['hash'] = self.hash(block)
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1
        while True:
            guess = str(new_proof**3 - previous_proof**3).encode()
            guess_hash = hashlib.sha256(guess).hexdigest()
            if guess_hash[:5] == '00000':
                return new_proof
            new_proof += 1

    def hash(self, block):
        block_copy = block.copy()
        block_copy.pop('hash', None)
        encoded = json.dumps(block_copy, sort_keys=True).encode()
        return hashlib.sha256(encoded).hexdigest()

    def chain_valid(self, chain):
        for idx in range(1, len(chain)):
            prev = chain[idx - 1]
            curr = chain[idx]
            if curr['previous_hash'] != prev['hash']:
                return False
            valid_proof = hashlib.sha256(
                str(curr['proof']**3 - prev['proof']**3).encode()
            ).hexdigest()
            if valid_proof[:5] != '00000':
                return False
            if curr['hash'] != self.hash(curr):
                return False
        return True