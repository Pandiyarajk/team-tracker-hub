# 🧭 Team Management Dashboard

A comprehensive Flask-based web application for managing QA Automation teams with features for tracking leaves, accomplishments, inventory, test servers, builds, and more.

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

### Core Functionality
- **🏠 Dashboard** - Overview of team statistics, recent activities, and quick actions
- **📅 Leave Management** - Track leaves, work from home, sick leave, and personal leave
- **🏆 Accomplishments** - Log and showcase team achievements
- **💻 Inventory Tracking** - Manage hardware and devices assigned to team members
- **🖥️ Test Servers** - Track server configurations and availability
- **📦 Build Tracking** - Monitor testing and release builds
- **🔗 Useful Links** - Quick access to team resources (Jenkins, Jira, etc.)
- **📢 Announcements** - Team-wide updates and notices
- **🎉 Celebrations** - Recognize milestones and achievements
- **🎓 Skills Matrix** - Track team member skills and training
- **📝 Meeting Notes** - Record action items from meetings
- **📋 Task Tracker** - Monitor resource allocation and task progress

### Additional Features
- **🔐 Authentication** - Simple login system with role-based access
- **📧 Email Notifications** - Daily summary emails via Gmail
- **🔄 Jira Integration** - Sync and display Jira issues
- **📱 Responsive Design** - Mobile-friendly Bootstrap 5 interface
- **🎨 Modern UI** - Clean and intuitive user interface

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or higher
- pip (Python package manager)
- Gmail account (for email notifications, optional)
- Jira account (for integration, optional)

### Installation

1. **Clone or download the project**
```bash
cd team_dashboard
```

2. **Create a virtual environment**
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables (optional)**

Create a `.env` file in the project root:
```bash
# Flask Configuration
SECRET_KEY=your-secret-key-here

# Email Configuration
EMAIL_ENABLED=True
EMAIL_SENDER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
MANAGER_EMAIL=manager@company.com

# Jira Configuration
JIRA_ENABLED=True
JIRA_URL=https://yourcompany.atlassian.net
JIRA_USERNAME=your-email@company.com
JIRA_API_TOKEN=your-jira-api-token
JIRA_PROJECT_KEY=QA
```

5. **Run the application**
```bash
python app.py
```

6. **Access the application**

Open your browser and navigate to:
```
http://localhost:5000
```

## 👤 Default Login Credentials

### Admin Account
- **Username:** `admin`
- **Password:** `admin`

### Team Member Account
- **Username:** `john`
- **Password:** `john123`

> ⚠️ **Important:** Change these credentials in production by updating the password hashes in `data/users.json`

## 📁 Project Structure

```
team_dashboard/
├── app.py                 # Main Flask application
├── config.py              # Configuration settings
├── utils.py               # Utility functions
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (create this)
│
├── static/
│   ├── css/
│   │   └── style.css     # Custom styles
│   └── js/
│       └── script.js     # Custom JavaScript
│
├── templates/
│   ├── base.html         # Base template
│   ├── login.html        # Login page
│   ├── dashboard.html    # Dashboard page
│   ├── leaves.html       # Leave management
│   ├── accomplishments.html
│   ├── inventory.html
│   ├── servers.html
│   ├── builds.html
│   ├── links.html
│   ├── announcements.html
│   ├── celebrations.html
│   ├── skills.html
│   ├── meetings.html
│   ├── tasks.html
│   ├── 404.html          # Error pages
│   └── 500.html
│
└── data/
    ├── users.json        # User accounts
    ├── leaves.json       # Leave records
    ├── accomplishments.json
    ├── inventory.json
    ├── servers.json
    ├── builds.json
    ├── links.json
    ├── announcements.json
    ├── celebrations.json
    ├── skills.json
    ├── meetings.json
    └── tasks.json
```

## 🔧 Configuration

### Email Setup (Gmail)

1. Enable 2-factor authentication on your Gmail account
2. Generate an App Password:
   - Go to Google Account Settings → Security
   - Select "2-Step Verification" → "App passwords"
   - Generate a new app password for "Mail"
3. Use this app password in your `.env` file

### Jira Integration

1. Generate a Jira API token:
   - Go to https://id.atlassian.com/manage-profile/security/api-tokens
   - Create API token
2. Add credentials to `.env` file
3. Set `JIRA_ENABLED=True`

### Daily Email Schedule

The application sends daily summary emails at 6:00 PM by default. To change this:

Edit `config.py`:
```python
EMAIL_SCHEDULE_HOUR = 18  # 24-hour format
EMAIL_SCHEDULE_MINUTE = 0
```

## 📊 Data Storage

All data is stored in JSON files in the `data/` directory. This makes it easy to:
- Backup data (just copy the `data/` folder)
- Migrate to a database later if needed
- Version control your data
- Edit data manually if required

## 🔒 Security Notes

### For Production Use:

1. **Change Secret Key**
   ```python
   SECRET_KEY=generate-a-strong-random-key
   ```

2. **Update Default Passwords**
   - Use the hash_password function in utils.py to generate new hashes
   - Update `data/users.json` with new hashed passwords

3. **Enable HTTPS**
   - Use a reverse proxy (Nginx/Apache)
   - Configure SSL certificates

4. **Set Debug to False**
   ```python
   DEBUG = False
   ```

5. **Restrict File Permissions**
   ```bash
   chmod 600 data/*.json
   ```

## 🎨 Customization

### Changing Colors/Theme

Edit `static/css/style.css` to customize:
- Primary colors
- Card styles
- Button styles
- Typography

### Adding New Features

1. Add route in `app.py`
2. Create template in `templates/`
3. Update navigation in `base.html`
4. Create JSON data file if needed

## 📱 Mobile Support

The application is fully responsive and works on:
- Desktop browsers
- Tablets
- Mobile phones

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## 📄 License

This project is licensed under the MIT License.

## 🆘 Troubleshooting

### Application won't start
- Check Python version: `python --version`
- Verify all dependencies are installed: `pip list`
- Check for port conflicts (default: 5000)

### Email not sending
- Verify Gmail credentials
- Check app password (not regular password)
- Ensure `EMAIL_ENABLED=True`

### Jira integration not working
- Verify API token is valid
- Check Jira URL format
- Ensure `JIRA_ENABLED=True`

### Data not persisting
- Check file permissions on `data/` directory
- Verify JSON files are not corrupted
- Check application logs for errors

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the code comments
3. Check Flask documentation: https://flask.palletsprojects.com/

## 🗺️ Roadmap

Future enhancements:
- [ ] Export data to Excel/CSV
- [ ] Advanced reporting and analytics
- [ ] Slack integration
- [ ] REST API for external integrations
- [ ] Database migration option
- [ ] Advanced role-based permissions
- [ ] File upload support
- [ ] Calendar view for leaves
- [ ] Charts and visualizations

## 📝 Version History

See [CHANGELOG.md](CHANGELOG.md) for detailed version history.

## 👏 Acknowledgments

- Flask framework
- Bootstrap 5
- Bootstrap Icons
- APScheduler
- All open-source contributors

---

**Built with ❤️ for QA Automation Teams**

*Last Updated: October 30, 2025*
