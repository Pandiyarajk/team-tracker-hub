"""
Utility functions for Team Management Dashboard
"""
import json
import os
from datetime import datetime, date
from functools import wraps
from flask import session, redirect, url_for, flash
import hashlib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
from requests.auth import HTTPBasicAuth

from config import Config


def login_required(f):
    """Decorator to require login for routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        if session.get('role') != 'admin':
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function


def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()


def load_json_file(filename):
    """Load data from JSON file"""
    filepath = os.path.join(Config.DATA_DIR, filename)
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []


def save_json_file(filename, data):
    """Save data to JSON file"""
    filepath = os.path.join(Config.DATA_DIR, filename)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2, default=str)


def get_next_id(data_list):
    """Get next available ID for a list of items"""
    if not data_list:
        return 1
    return max(item.get('id', 0) for item in data_list) + 1


def format_date(date_str):
    """Format date string for display"""
    if not date_str:
        return ''
    try:
        dt = datetime.strptime(str(date_str), Config.DATE_FORMAT)
        return dt.strftime('%b %d, %Y')
    except:
        return date_str


def get_today():
    """Get today's date in standard format"""
    return date.today().strftime(Config.DATE_FORMAT)


def send_email(subject, body, to_email=None):
    """Send email via Gmail SMTP"""
    if not Config.EMAIL_ENABLED:
        print(f"Email disabled. Would have sent: {subject}")
        return False
    
    if not Config.EMAIL_PASSWORD:
        print("Email password not configured")
        return False
    
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = Config.EMAIL_SENDER
        msg['To'] = to_email or Config.MANAGER_EMAIL
        
        # Attach HTML body
        html_part = MIMEText(body, 'html')
        msg.attach(html_part)
        
        # Send email
        with smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT) as server:
            server.starttls()
            server.login(Config.EMAIL_SENDER, Config.EMAIL_PASSWORD)
            server.send_message(msg)
        
        print(f"Email sent successfully: {subject}")
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


def generate_daily_summary():
    """Generate daily summary email content"""
    today = get_today()
    
    # Load data
    leaves = load_json_file('leaves.json')
    accomplishments = load_json_file('accomplishments.json')
    announcements = load_json_file('announcements.json')
    builds = load_json_file('builds.json')
    
    # Filter today's data
    today_leaves = [l for l in leaves if l.get('date') == today]
    today_accomplishments = [a for a in accomplishments if a.get('date') == today]
    recent_announcements = sorted(announcements, key=lambda x: x.get('date', ''), reverse=True)[:3]
    active_builds = [b for b in builds if b.get('status') in ['testing', 'release']]
    
    # Generate HTML email
    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
            h2 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
            h3 {{ color: #34495e; margin-top: 20px; }}
            .section {{ margin-bottom: 30px; }}
            .item {{ background: #f8f9fa; padding: 10px; margin: 10px 0; border-left: 4px solid #3498db; }}
            .empty {{ color: #7f8c8d; font-style: italic; }}
        </style>
    </head>
    <body>
        <h2>📊 Daily Team Summary - {format_date(today)}</h2>
        
        <div class="section">
            <h3>🏖️ Leave & Attendance</h3>
            {_format_leaves_html(today_leaves)}
        </div>
        
        <div class="section">
            <h3>🎯 Accomplishments</h3>
            {_format_accomplishments_html(today_accomplishments)}
        </div>
        
        <div class="section">
            <h3>📢 Recent Announcements</h3>
            {_format_announcements_html(recent_announcements)}
        </div>
        
        <div class="section">
            <h3>🔧 Active Builds</h3>
            {_format_builds_html(active_builds)}
        </div>
        
        <hr>
        <p style="color: #7f8c8d; font-size: 12px;">
            This is an automated summary from Team Management Dashboard.<br>
            Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        </p>
    </body>
    </html>
    """
    
    return html


def _format_leaves_html(leaves):
    """Format leaves for email"""
    if not leaves:
        return '<p class="empty">No leaves today</p>'
    
    html = ''
    for leave in leaves:
        html += f"""
        <div class="item">
            <strong>{leave.get('name')}</strong> - {leave.get('type')}<br>
            Reason: {leave.get('reason', 'N/A')}<br>
            Status: {leave.get('approval_status', 'pending')}
        </div>
        """
    return html


def _format_accomplishments_html(accomplishments):
    """Format accomplishments for email"""
    if not accomplishments:
        return '<p class="empty">No accomplishments logged today</p>'
    
    html = ''
    for acc in accomplishments:
        html += f"""
        <div class="item">
            <strong>{acc.get('member_name')}</strong> - {acc.get('type')}<br>
            {acc.get('description')}<br>
            <em>Impact: {acc.get('impact', 'N/A')}</em>
        </div>
        """
    return html


def _format_announcements_html(announcements):
    """Format announcements for email"""
    if not announcements:
        return '<p class="empty">No recent announcements</p>'
    
    html = ''
    for ann in announcements:
        html += f"""
        <div class="item">
            <strong>{ann.get('title')}</strong> - {format_date(ann.get('date'))}<br>
            {ann.get('message')}<br>
            <em>Posted by: {ann.get('posted_by')}</em>
        </div>
        """
    return html


def _format_builds_html(builds):
    """Format builds for email"""
    if not builds:
        return '<p class="empty">No active builds</p>'
    
    html = ''
    for build in builds:
        html += f"""
        <div class="item">
            <strong>{build.get('build_name')}</strong> v{build.get('version')}<br>
            Environment: {build.get('environment')} | Status: {build.get('status')}<br>
            Date: {format_date(build.get('date'))}
        </div>
        """
    return html


def fetch_jira_issues(assignee=None):
    """Fetch issues from Jira"""
    if not Config.JIRA_ENABLED:
        return []
    
    if not Config.JIRA_API_TOKEN or not Config.JIRA_USERNAME:
        print("Jira credentials not configured")
        return []
    
    try:
        # Build JQL query
        if assignee:
            jql = f'assignee="{assignee}" AND status != Done'
        else:
            jql = f'project={Config.JIRA_PROJECT_KEY} AND status != Done'
        
        # API endpoint
        url = f"{Config.JIRA_URL}/rest/api/3/search"
        params = {
            'jql': jql,
            'maxResults': 50,
            'fields': 'summary,status,assignee,priority,created'
        }
        
        # Make request
        auth = HTTPBasicAuth(Config.JIRA_USERNAME, Config.JIRA_API_TOKEN)
        response = requests.get(url, params=params, auth=auth, timeout=10)
        response.raise_for_status()
        
        # Parse response
        data = response.json()
        issues = []
        for issue in data.get('issues', []):
            issues.append({
                'key': issue['key'],
                'summary': issue['fields']['summary'],
                'status': issue['fields']['status']['name'],
                'assignee': issue['fields']['assignee']['displayName'] if issue['fields'].get('assignee') else 'Unassigned',
                'priority': issue['fields']['priority']['name'] if issue['fields'].get('priority') else 'None',
                'created': issue['fields']['created'][:10]
            })
        
        return issues
    except Exception as e:
        print(f"Error fetching Jira issues: {e}")
        return []


def get_dashboard_stats():
    """Get statistics for dashboard"""
    today = get_today()
    
    # Load all data
    users = load_json_file('users.json')
    leaves = load_json_file('leaves.json')
    accomplishments = load_json_file('accomplishments.json')
    inventory = load_json_file('inventory.json')
    servers = load_json_file('servers.json')
    builds = load_json_file('builds.json')
    
    # Calculate stats
    team_members = [u for u in users if u.get('role') != 'admin']
    on_leave_today = [l for l in leaves if l.get('date') == today and l.get('approval_status') == 'approved']
    pending_approvals = [l for l in leaves if l.get('approval_status') == 'pending']
    total_devices = len(inventory)
    available_servers = [s for s in servers if s.get('status') == 'available']
    active_builds = [b for b in builds if b.get('status') in ['testing', 'release']]
    recent_accomplishments = [a for a in accomplishments if a.get('date') == today]
    
    return {
        'total_team_members': len(team_members),
        'on_leave_today': len(on_leave_today),
        'pending_approvals': len(pending_approvals),
        'total_devices': total_devices,
        'available_servers': len(available_servers),
        'active_builds': len(active_builds),
        'today_accomplishments': len(recent_accomplishments),
        'on_leave_names': [l.get('name') for l in on_leave_today],
        'recent_accomplishments_list': recent_accomplishments[:5]
    }
