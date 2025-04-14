from flask import Flask, request, jsonify
from flask_cors import CORS
from aptos_sdk.account import Account
from aptos_sdk.transactions import TransactionPayload
import time

app = Flask(__name__)
CORS(app)

@app.route('/create_project', methods=['POST'])
def create_project():
    try:
        data = request.json
        private_key = data.get('private_key')
        goal = int(data.get('goal'))
        deadline = int(time.time()) + 30 * 24 * 60 * 60  # 30 days from now

        # Initialize Aptos client
        client = AptosClient("https://fullnode.mainnet.aptoslabs.com")
        
        # Create account from private key
        account = Account(bytes.fromhex(private_key))
        
        # Create transaction payload
        payload = TransactionPayload(
            module_address=account.address(),
            module_name="project_management",
            function_name="create_project",
            type_arguments=[],
            arguments=[
                "My Project",  # name
                "Project Description",  # description
                str(goal),  # funding_goal
                str(deadline)  # deadline
            ]
        )
        
        # Create and sign transaction
        transaction = client.submit_transaction(account, payload)
        
        return jsonify({"success": True, "transaction": transaction.hash})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/contribute', methods=['POST'])
def contribute():
    try:
        data = request.json
        private_key = data.get('private_key')
        project_owner = data.get('project_owner')
        amount = int(data.get('amount'))

        # Initialize Aptos client
        client = AptosClient("https://fullnode.mainnet.aptoslabs.com")
        
        # Create account from private key
        account = Account(bytes.fromhex(private_key))
        
        # Create transaction payload
        payload = TransactionPayload(
            module_address=account.address(),
            module_name="project_management",
            function_name="contribute",
            type_arguments=[],
            arguments=[
                project_owner,
                str(amount)
            ]
        )
        
        # Create and sign transaction
        transaction = client.submit_transaction(account, payload)
        
        return jsonify({"success": True, "transaction": transaction.hash})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    app.run(debug=True) 
