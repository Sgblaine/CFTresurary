#!/usr/bin/env python3
"""
Google Drive service for managing receipt images
"""

from datetime import datetime
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

class DriveService:
    """
    Service for interacting with Google Drive API
    Fetches receipt files and manages Google Drive operations
    """
    
    def __init__(self, config):
        """Initialize Drive service with configuration"""
        self.config = config
        self.credentials_file = config.google_credentials_file
        self.receipts_folder_id = config.google_receipts_folder_id
        self._setup_drive_client()
    
    def _setup_drive_client(self):
        """Setup Google Drive API client"""
        try:
            # Authenticate using service account
            scopes = ['https://www.googleapis.com/auth/drive']
            credentials = Credentials.from_service_account_file(
                self.credentials_file,
                scopes=scopes
            )
            self.drive_service = build('drive', 'v3', credentials=credentials)
            print("✓ Connected to Google Drive")
        except Exception as e:
            raise Exception(f"Failed to authenticate with Google Drive: {str(e)}")
    
    def get_receipts(self):
        """
        Fetch all receipt files from the Google Drive receipts folder
        
        Returns:
            list: List of receipt file dictionaries with metadata
        """
        try:
            query = f"'{self.receipts_folder_id}' in parents and trashed=false"
            results = self.drive_service.files().list(
                q=query,
                spaces='drive',
                fields='files(id, name, webViewLink, createdTime, modifiedTime)',
                pageSize=1000
            ).execute()
            
            files = results.get('files', [])
            
            # Format and parse receipts
            formatted_receipts = []
            for file in files:
                try:
                    # Try to parse date from filename or use creation date
                    date = self._parse_receipt_date(file['name'], file['createdTime'])
                    formatted_receipts.append({
                        'id': file['id'],
                        'name': file['name'],
                        'web_view_link': file['webViewLink'],
                        'date': date,
                        'created_time': file['createdTime'],
                    })
                except Exception as e:
                    print(f"Warning: Could not parse receipt {file['name']}: {str(e)}")
            
            return formatted_receipts
        
        except Exception as e:
            print(f"Error fetching receipts from Google Drive: {str(e)}")
            return []
    
    def _parse_receipt_date(self, filename, created_time):
        """
        Parse receipt date from filename or creation date
        
        Args:
            filename (str): Name of the receipt file
            created_time (str): ISO format creation time from Drive API
        
        Returns:
            datetime: Parsed date
        """
        # Try to extract date from filename (YYYY-MM-DD format)
        import re
        date_pattern = r'(\d{4})[-/](\d{2})[-/](\d{2})'
        match = re.search(date_pattern, filename)
        
        if match:
            year, month, day = match.groups()
            return datetime(int(year), int(month), int(day))
        
        # Fall back to created time
        return datetime.fromisoformat(created_time.replace('Z', '+00:00'))
