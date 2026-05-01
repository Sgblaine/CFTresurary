#!/usr/bin/env python3
"""
Email service for sending notifications
DISABLED - Email functionality removed for security
"""

class EmailService:
    """
    Placeholder for email functionality
    Email notifications have been disabled to avoid embedding credentials
    
    Transactions and summaries are logged to console and Excel file instead.
    """
    
    def __init__(self, config):
        """Initialize (disabled)"""
        self.config = config
    
    def send_summary(self, summary):
        """Email functionality disabled. Use console logs and Excel file instead."""
        print("Note: Email notifications are disabled. Check Excel file and console output.")
