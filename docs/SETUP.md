# CFTresurary Setup Guide

## Prerequisites

- Python 3.8+
- Git
- Bank account connected to Plaid
- Google Cloud account
- Excel file for accounting data

## Step 1: Clone Repository

```bash
git clone https://github.com/Sgblaine/CFTresurary.git
cd CFTresurary
```

## Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 3: Set Up Plaid

1. Go to https://dashboard.plaid.com
2. Sign up for a free account
3. Create a new application
4. Get your Client ID and Secret
5. Use Plaid Link to connect your bank account and get an access token

## Step 4: Set Up Google Drive

1. Go to Google Cloud Console: https://console.cloud.google.com
2. Create a new project: `CFTresurary`
3. Enable Google Drive API
4. Create a Service Account:
   - Go to Credentials
   - Create Service Account
   - Generate JSON key
   - Save as `google_credentials.json` in project folder
5. Create a folder in your Google Drive for receipts
6. Share that folder with the service account email
7. Get the folder ID from the URL

## Step 5: Configure Environment Variables

Create a `.env` file in the project root:

```env
# Plaid
PLAID_CLIENT_ID=your_client_id_here
PLAID_SECRET=your_secret_here
PLAID_ENVIRONMENT=sandbox
PLAID_ACCESS_TOKEN=your_access_token_from_plaid_link

# Google Drive
GOOGLE_CREDENTIALS_FILE=google_credentials.json
GOOGLE_RECEIPTS_FOLDER_ID=your_folder_id_from_drive_url

# Excel
EXCEL_FILE_PATH=C:\\Users\\YourName\\path\\to\\file.xlsx

# Settings
RECEIPT_MATCH_DAYS=3
DRY_RUN=False
LOG_LEVEL=INFO
```

## Step 6: Test Setup

1. Set `DRY_RUN=True` in `.env`
2. Run: `python main.py`
3. Check that all services initialize correctly
4. Set `DRY_RUN=False` to run live

## Troubleshooting

### Plaid Issues
- Check Client ID and Secret in dashboard
- Ensure access token is valid
- Use sandbox environment for testing

### Google Drive Issues
- Verify service account email is shared with receipts folder
- Check that `google_credentials.json` is in project root
- Ensure Google Drive API is enabled in Cloud Console

### Excel Issues
- Verify file path is correct
- Ensure Excel file is not open when running
- Check that column names match `.env` configuration

## Support

Refer to service documentation:
- Plaid: https://plaid.com/docs/
- Google Drive API: https://developers.google.com/drive/api
- openpyxl: https://openpyxl.readthedocs.io/
