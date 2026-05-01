#!/usr/bin/env python3
"""
CFTresurary - Contrary Forest Treasury Management System
Main application entry point
"""

import sys
from datetime import datetime
from config import Config
from plaid_service import PlaidService
from excel_service import ExcelService
from drive_service import DriveService

def main():
    """
    Main application function
    Orchestrates transaction fetching, receipt matching, and data updates
    """
    print("\n" + "="*60)
    print("CFTresurary - Contrary Forest Treasury Management")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60 + "\n")
    
    try:
        # Initialize configuration
        config = Config()
        print(f"✓ Configuration loaded")
        print(f"  - Excel file: {config.excel_file_path}")
        print(f"  - Google receipts folder: {config.google_receipts_folder_id}")
        print(f"  - Plaid environment: {config.plaid_environment}\n")
        
        # Initialize services
        plaid = PlaidService(config)
        excel = ExcelService(config)
        drive = DriveService(config)
        
        print("✓ All services initialized\n")
        
        # Fetch transactions from Plaid
        print("-" * 60)
        print("STEP 1: Fetching transactions from Plaid...")
        print("-" * 60)
        transactions = plaid.get_transactions()
        print(f"✓ Fetched {len(transactions)} transactions\n")
        
        if not transactions:
            print("No transactions found. Exiting.")
            return
        
        # Display transactions
        for i, txn in enumerate(transactions, 1):
            print(f"{i}. {txn['date']} | {txn['merchant']} | ${txn['amount']:.2f}")
        print()
        
        # Fetch receipts from Google Drive
        print("-" * 60)
        print("STEP 2: Fetching receipts from Google Drive...")
        print("-" * 60)
        receipts = drive.get_receipts()
        print(f"✓ Found {len(receipts)} receipt files\n")
        
        if receipts:
            for i, receipt in enumerate(receipts, 1):
                print(f"{i}. {receipt['name']} (ID: {receipt['id']})")
            print()
        
        # Match receipts to transactions
        print("-" * 60)
        print("STEP 3: Matching receipts to transactions...")
        print("-" * 60)
        matched_transactions = plaid.match_receipts_to_transactions(
            transactions, receipts, config.receipt_match_days
        )
        
        matched_count = sum(1 for t in matched_transactions if t.get('receipt_link'))
        print(f"✓ Matched {matched_count} receipts to transactions\n")
        
        # Update Excel with new transactions
        print("-" * 60)
        print("STEP 4: Updating Excel file with transactions...")
        print("-" * 60)
        added_count = excel.add_transactions(matched_transactions)
        print(f"✓ Added {added_count} new transactions to Excel\n")
        
        # Display summary
        print("="*60)
        print("SUMMARY")
        print("="*60)
        print(f"Transactions processed: {len(transactions)}")
        print(f"Receipts found: {len(receipts)}")
        print(f"Receipts matched: {matched_count}")
        print(f"New rows added to Excel: {added_count}")
        print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
