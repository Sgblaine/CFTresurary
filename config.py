#!/usr/bin/env python3
"""
Configuration management for CFTresurary
Loads and validates environment variables
"""

import os
from dotenv import load_dotenv
from pathlib import Path

class Config:
    """
    Configuration class that loads and stores all application settings
    from environment variables in .env file
    """
    
    def __init__(self):
        """Load and validate configuration from .env file"""
        
        # Load .env file
        env_path = Path(__file__).parent / '.env'
        load_dotenv(env_path)
        
        # Plaid Configuration
        self.plaid_client_id = os.getenv('PLAID_CLIENT_ID')
        self.plaid_secret = os.getenv('PLAID_SECRET')
        self.plaid_environment = os.getenv('PLAID_ENVIRONMENT', 'sandbox')
        self.plaid_country_codes = os.getenv('PLAID_COUNTRY_CODES', 'US')
        self.plaid_access_token = os.getenv('PLAID_ACCESS_TOKEN')
        
        # Google Drive Configuration
        self.google_credentials_file = os.getenv('GOOGLE_CREDENTIALS_FILE')
        self.google_receipts_folder_id = os.getenv('GOOGLE_RECEIPTS_FOLDER_ID')
        
        # Excel Configuration
        self.excel_file_path = os.getenv('EXCEL_FILE_PATH')
        self.excel_date_column = os.getenv('EXCEL_DATE_COLUMN', 'Date of Expense')
        self.excel_location_column = os.getenv('EXCEL_LOCATION_COLUMN', 'Expense Location')
        self.excel_category_column = os.getenv('EXCEL_CATEGORY_COLUMN', 'Expense Category')
        self.excel_description_column = os.getenv('EXCEL_DESCRIPTION_COLUMN', 'Expense Description')
        self.excel_receipt_link_column = os.getenv('EXCEL_RECEIPT_LINK_COLUMN', 'Link to Expense Image')
        self.excel_amount_column = os.getenv('EXCEL_AMOUNT_COLUMN', 'Expense Amount')
        self.excel_running_total_column = os.getenv('EXCEL_RUNNING_TOTAL_COLUMN', 'Running Total')
        
        # Application Configuration
        self.receipt_match_days = int(os.getenv('RECEIPT_MATCH_DAYS', '3'))
        self.log_level = os.getenv('LOG_LEVEL', 'INFO')
        self.dry_run = os.getenv('DRY_RUN', 'False').lower() == 'true'
        
        # Validate required fields
        self._validate_config()
    
    def _validate_config(self):
        """Validate that all required configuration fields are present"""
        required_fields = [
            ('PLAID_CLIENT_ID', self.plaid_client_id),
            ('PLAID_SECRET', self.plaid_secret),
            ('GOOGLE_CREDENTIALS_FILE', self.google_credentials_file),
            ('GOOGLE_RECEIPTS_FOLDER_ID', self.google_receipts_folder_id),
            ('EXCEL_FILE_PATH', self.excel_file_path),
        ]
        
        missing_fields = [field for field, value in required_fields if not value]
        
        if missing_fields:
            raise ValueError(
                f"Missing required configuration fields: {', '.join(missing_fields)}\n"
                f"Please ensure these are set in your .env file."
            )
    
    def __repr__(self):
        return (
            f"Config(plaid_env={self.plaid_environment}, "
            f"excel_file={self.excel_file_path}, "
            f"dry_run={self.dry_run})"
        )
