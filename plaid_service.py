#!/usr/bin/env python3
"""
Plaid service for fetching bank transactions
"""

from datetime import datetime, timedelta
from plaid import ApiClient, Configuration
from plaid.api import transactions_api
from plaid.model.transactions_get_request import TransactionsGetRequest

class PlaidService:
    """
    Service for interacting with Plaid API
    Fetches transactions and manages access tokens
    """
    
    def __init__(self, config):
        """Initialize Plaid service with configuration"""
        self.config = config
        self.client_id = config.plaid_client_id
        self.secret = config.plaid_secret
        self.environment = config.plaid_environment
        
        # Initialize Plaid API client
        self._setup_plaid_client()
    
    def _setup_plaid_client(self):
        """Setup Plaid API client"""
        configuration = Configuration(
            host=self._get_plaid_host(),
            api_key={
                'clientId': self.client_id,
                'secret': self.secret,
            }
        )
        self.api_client = ApiClient(configuration)
        self.transactions_api = transactions_api.TransactionsApi(self.api_client)
    
    def _get_plaid_host(self):
        """Get Plaid API host based on environment"""
        if self.environment == 'production':
            return 'https://production.plaid.com'
        return 'https://sandbox.plaid.com'
    
    def get_transactions(self, days_back=30):
        """
        Fetch transactions from Plaid for the specified number of days
        
        Args:
            days_back (int): Number of days to look back (default: 30)
        
        Returns:
            list: List of transaction dictionaries
        """
        if not self.config.plaid_access_token:
            print("⚠️  No Plaid access token found. Please link a bank account first.")
            print("   Use Plaid Link to authenticate: https://plaid.com/docs/api/")
            return []
        
        try:
            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=days_back)
            
            request = TransactionsGetRequest(
                access_token=self.config.plaid_access_token,
                start_date=start_date,
                end_date=end_date,
            )
            
            response = self.transactions_api.transactions_get(request)
            transactions = response['transactions']
            
            # Format transactions
            formatted = []
            for txn in transactions:
                formatted.append({
                    'date': txn['date'],
                    'merchant': txn.get('merchant_name', txn['name']),
                    'amount': abs(txn['amount']),
                    'description': txn.get('name', ''),
                    'category': txn.get('personal_finance_category', {}).get('primary', 'Other'),
                    'plaid_id': txn['transaction_id'],
                })
            
            return formatted
        
        except Exception as e:
            print(f"Error fetching transactions from Plaid: {str(e)}")
            return []
    
    def match_receipts_to_transactions(self, transactions, receipts, days_tolerance=3):
        """
        Match receipts to transactions based on date and amount proximity
        
        Args:
            transactions (list): List of transaction dicts
            receipts (list): List of receipt dicts from Google Drive
            days_tolerance (int): Number of days to consider for matching
        
        Returns:
            list: Transactions with matched receipt links
        """
        for txn in transactions:
            txn['receipt_link'] = None
            txn_date = datetime.strptime(txn['date'], '%Y-%m-%d')
            
            for receipt in receipts:
                receipt_date = receipt.get('date')
                if not receipt_date:
                    continue
                
                # Check if dates are within tolerance
                date_diff = abs((txn_date - receipt_date).days)
                if date_diff <= days_tolerance:
                    # Link the receipt
                    txn['receipt_link'] = receipt['web_view_link']
                    break
        
        return transactions
