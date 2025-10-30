"""
Configuration file for Team Management Dashboard
"""
import os
from datetime import timedelta

class Config:
    """Base configuration"""
    
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = True
    
    # Session Configuration
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    
    # Data Directory
    DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
    
    # Email Configuration (Gmail SMTP)
    EMAIL_ENABLED = os.environ.get('EMAIL_ENABLED', 'False').lower() == 'true'
    EMAIL_SENDER = os.environ.get('EMAIL_SENDER', 'team.bot@gmail.com')
    EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD', '')  # Use Gmail App Password
    MANAGER_EMAIL = os.environ.get('MANAGER_EMAIL', 'manager@company.com')
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587
    
    # Email Schedule (24-hour format)
    EMAIL_SCHEDULE_HOUR = 18  # 6 PM
    EMAIL_SCHEDULE_MINUTE = 0
    
    # Jira Configuration
    JIRA_ENABLED = os.environ.get('JIRA_ENABLED', 'False').lower() == 'true'
    JIRA_URL = os.environ.get('JIRA_URL', 'https://yourcompany.atlassian.net')
    JIRA_USERNAME = os.environ.get('JIRA_USERNAME', '')
    JIRA_API_TOKEN = os.environ.get('JIRA_API_TOKEN', '')  # Use API token for Jira Cloud
    JIRA_PROJECT_KEY = os.environ.get('JIRA_PROJECT_KEY', 'QA')
    
    # Pagination
    ITEMS_PER_PAGE = 10
    
    # Date Format
    DATE_FORMAT = '%Y-%m-%d'
    DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
    
    # Application Settings
    APP_NAME = 'Team Management Dashboard'
    APP_VERSION = '1.0.0'
