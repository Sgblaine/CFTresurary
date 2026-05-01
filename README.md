# CFTresurary - Contrary Forest Treasury Management System

## Overview

CFTresurary is an automated treasury management system for Contrary Forest Association. It:

- **Fetches transactions** from your bank via Plaid API
- **Matches receipts** from Google Drive based on date and amount
- **Updates accounting spreadsheet** with transaction data
- **Maintains running totals** of expenses

## Features

✅ Automatic transaction retrieval from Plaid-connected bank accounts
✅ Receipt matching based on date proximity
✅ Excel file integration with running totals
✅ Google Drive receipt folder management
✅ Console and file logging
✅ Dry-run mode for testing
✅ No email credentials embedded (security-first)

## Architecture

```
main.py          - Application entry point
config.py        - Configuration management
plaid_service.py - Bank transaction fetching
drive_service.py - Receipt retrieval from Google Drive
excel_service.py - Spreadsheet management
email_service.py - Logging (email disabled)
```

## Setup Instructions

See [SETUP.md](docs/SETUP.md) for detailed setup instructions.

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure .env file** with:
   - Plaid API credentials
   - Google Drive folder ID and credentials
   - Excel file path

3. **Run the application:**
   ```bash
   python main.py
   ```

## Configuration (.env)

Required environment variables:

```
# Plaid
PLAID_CLIENT_ID=your_client_id
PLAID_SECRET=your_secret
PLAID_ENVIRONMENT=sandbox  # or production

# Google Drive
GOOGLE_CREDENTIALS_FILE=google_credentials.json
GOOGLE_RECEIPTS_FOLDER_ID=your_folder_id

# Excel
EXCEL_FILE_PATH=/path/to/your/file.xlsx

# Application
RECEIPT_MATCH_DAYS=3
DRY_RUN=False
```

## Usage

### Run transactions sync:
```bash
python main.py
```

### Test mode (dry-run):
Set `DRY_RUN=True` in `.env` to preview changes without modifying files.

## Security

- ✅ All credentials stored in `.env` (not committed to Git)
- ✅ No passwords embedded in code
- ✅ Service account for Google Drive (no user credentials)
- ✅ Plaid sandbox for testing

## Support

For issues or questions, check the logs or review the SETUP documentation.
