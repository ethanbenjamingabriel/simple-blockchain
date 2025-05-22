from flask import Flask, jsonify, render_template
from blockchain import Blockchain

app = Flask(__name__, static_folder='static', template_folder='templates')
blockchain = Blockchain()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/mine_block', methods=['GET'])
def mine_block():
    prev_block = blockchain.get_previous_block()
    proof = blockchain.proof_of_work(prev_block['proof'])
    block = blockchain.create_block(proof, prev_block['hash'])
    response = {
        'message': 'A block is MINED',
        'index': block['index'],
        'timestamp': block['timestamp'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
        'hash': block['hash']
    }
    return jsonify(response), 200

@app.route('/get_chain', methods=['GET'])
def display_chain():
    return jsonify({'chain': blockchain.chain, 'length': len(blockchain.chain)}), 200

@app.route('/valid', methods=['GET'])
def valid():
    valid = blockchain.chain_valid(blockchain.chain)
    return jsonify({'message': 'The Blockchain is valid.'} if valid
                   else {'message': 'The Blockchain is not valid.'}), 200

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)