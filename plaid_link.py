#!/usr/bin/env python3
"""
Plaid Link Integration
Simple Flask server to handle Plaid Link authentication
"""

import os
import json
from flask import Flask, render_template_string, request, jsonify
from dotenv import load_dotenv
from plaid import ApiClient, Configuration
from plaid.api import plaid_api
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Plaid configuration
PLAID_CLIENT_ID = os.getenv('PLAID_CLIENT_ID')
PLAID_SECRET = os.getenv('PLAID_SECRET')
PLAID_ENV = os.getenv('PLAID_ENVIRONMENT', 'sandbox')

# Set Plaid host based on environment
if PLAID_ENV == 'production':
    PLAID_HOST = 'https://production.plaid.com'
else:
    PLAID_HOST = 'https://sandbox.plaid.com'

# Initialize Plaid API client
configuration = Configuration(
    host=PLAID_HOST,
    api_key={
        'clientId': PLAID_CLIENT_ID,
        'secret': PLAID_SECRET,
    }
)
api_client = ApiClient(configuration)
plaid_client = plaid_api.PlaidApi(api_client)

# HTML template for Plaid Link
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>CFTresurary - Connect Your Bank Account</title>
    <script src="https://cdn.plaid.com/link/v3/stable/index.js"></script>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 600px;
            margin: 50px auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            text-align: center;
        }
        .info {
            background: #e3f2fd;
            border-left: 4px solid #2196F3;
            padding: 15px;
            margin: 20px 0;
            border-radius: 4px;
        }
        .button-container {
            text-align: center;
            margin: 30px 0;
        }
        button {
            background-color: #2196F3;
            color: white;
            padding: 12px 30px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
            font-weight: bold;
        }
        button:hover {
            background-color: #1976D2;
        }
        .success {
            background: #4CAF50;
            color: white;
            padding: 15px;
            border-radius: 4px;
            margin: 20px 0;
            display: none;
        }
        .error {
            background: #f44336;
            color: white;
            padding: 15px;
            border-radius: 4px;
            margin: 20px 0;
            display: none;
        }
        .token-display {
            background: #f5f5f5;
            padding: 15px;
            border-radius: 4px;
            margin: 20px 0;
            word-break: break-all;
            display: none;
            font-family: monospace;
            font-size: 12px;
        }
        .copy-button {
            background-color: #4CAF50;
            padding: 8px 15px;
            font-size: 14px;
            margin-top: 10px;
        }
        .copy-button:hover {
            background-color: #45a049;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🏦 CFTresurary - Bank Connection</h1>
        
        <div class="info">
            <strong>ℹ️ How this works:</strong>
            <p>Click the button below to securely connect your bank account to CFTresurary. 
            Your login credentials are only used by your bank—we never see them.</p>
        </div>
        
        <div class="button-container">
            <button onclick="openPlaidLink()">Connect Your Bank Account</button>
        </div>
        
        <div class="success" id="successMessage">
            ✓ <strong>Success!</strong> Your bank account has been connected.
        </div>
        
        <div class="error" id="errorMessage">
            ✗ <strong>Error:</strong> <span id="errorText"></span>
        </div>
        
        <div class="token-display" id="tokenDisplay">
            <strong>Access Token:</strong><br>
            <span id="tokenValue"></span><br>
            <button class="copy-button" onclick="copyToken()">Copy Token</button>
        </div>
    </div>

    <script>
        var linkToken = null;

        // Get link token on page load
        window.onload = function() {
            fetch('/get_link_token')
                .then(response => response.json())
                .then(data => {
                    if (data.link_token) {
                        linkToken = data.link_token;
                    } else {
                        document.getElementById('errorMessage').style.display = 'block';
                        document.getElementById('errorText').textContent = 'Failed to get link token';
                    }
                })
                .catch(error => {
                    document.getElementById('errorMessage').style.display = 'block';
                    document.getElementById('errorText').textContent = error.message;
                });
        };

        function openPlaidLink() {
            if (!linkToken) {
                alert('Link token not yet loaded. Please try again.');
                return;
            }

            Plaid.create({
                token: linkToken,
                onSuccess: (public_token, metadata) => {
                    console.log('Public token:', public_token);
                    // Send public token to backend
                    fetch('/exchange_public_token', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            public_token: public_token
                        })
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.access_token) {
                            document.getElementById('successMessage').style.display = 'block';
                            document.getElementById('tokenDisplay').style.display = 'block';
                            document.getElementById('tokenValue').textContent = data.access_token;
                        } else {
                            document.getElementById('errorMessage').style.display = 'block';
                            document.getElementById('errorText').textContent = data.error || 'Failed to get access token';
                        }
                    })
                    .catch(error => {
                        document.getElementById('errorMessage').style.display = 'block';
                        document.getElementById('errorText').textContent = error.message;
                    });
                },
                onExit: (err, metadata) => {
                    if (err) {
                        document.getElementById('errorMessage').style.display = 'block';
                        document.getElementById('errorText').textContent = err.message || 'Link was closed';
                    }
                },
            }).open();
        }

        function copyToken() {
            const token = document.getElementById('tokenValue').textContent;
            navigator.clipboard.writeText(token).then(() => {
                alert('Token copied to clipboard!');
            });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Serve the Plaid Link page"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/get_link_token', methods=['GET'])
def get_link_token():
    """Generate a Plaid Link token"""
    try:
        request_obj = LinkTokenCreateRequest(
            products=['auth', 'transactions'],
            client_name='CFTresurary',
            country_codes=['US'],
            language='en',
            user={
                'client_user_id': 'cftresurary-user',
            }
        )
        
        response = plaid_client.link_token_create(request_obj)
        return jsonify({
            'link_token': response['link_token']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/exchange_public_token', methods=['POST'])
def exchange_public_token():
    """Exchange public token for access token"""
    try:
        public_token = request.json.get('public_token')
        
        if not public_token:
            return jsonify({'error': 'No public token provided'}), 400
        
        # Exchange public token for access token
        request_obj = ItemPublicTokenExchangeRequest(
            public_token=public_token
        )
        response = plaid_client.item_public_token_exchange(request_obj)
        access_token = response['access_token']
        
        # Save to .env file
        save_access_token(access_token)
        
        return jsonify({
            'access_token': access_token,
            'message': 'Access token saved to .env'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

def save_access_token(access_token):
    """Save access token to .env file"""
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    
    # Read current .env
    env_lines = []
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            env_lines = f.readlines()
    
    # Update or add PLAID_ACCESS_TOKEN
    token_found = False
    for i, line in enumerate(env_lines):
        if line.startswith('PLAID_ACCESS_TOKEN='):
            env_lines[i] = f'PLAID_ACCESS_TOKEN={access_token}\n'
            token_found = True
            break
    
    if not token_found:
        env_lines.append(f'PLAID_ACCESS_TOKEN={access_token}\n')
    
    # Write back to .env
    with open(env_path, 'w') as f:
        f.writelines(env_lines)

if __name__ == '__main__':
    print("\n" + "="*60)
    print("CFTresurary - Plaid Link Server")
    print("="*60)
    print(f"Environment: {PLAID_ENV}")
    print(f"Open your browser and go to: http://localhost:5000")
    print("="*60 + "\n")
    
    app.run(debug=True, port=5000)
