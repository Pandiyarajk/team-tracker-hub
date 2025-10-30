# ✅ Installation Verification Guide

Use this checklist to verify your Team Management Dashboard installation.

## 📋 Pre-Installation Checklist

- [ ] Python 3.11+ installed (`python --version`)
- [ ] pip installed (`pip --version`)
- [ ] Internet connection (for installing dependencies)

## 🔍 File Structure Verification

### Core Application Files
- [ ] `app.py` - Main Flask application (800+ lines)
- [ ] `config.py` - Configuration file
- [ ] `utils.py` - Utility functions (300+ lines)
- [ ] `requirements.txt` - Dependencies list

### Templates (17 files)
- [ ] `templates/base.html` - Base template
- [ ] `templates/login.html` - Login page
- [ ] `templates/dashboard.html` - Dashboard
- [ ] `templates/leaves.html` - Leave management
- [ ] `templates/accomplishments.html` - Accomplishments
- [ ] `templates/inventory.html` - Inventory
- [ ] `templates/servers.html` - Servers
- [ ] `templates/builds.html` - Builds
- [ ] `templates/links.html` - Links
- [ ] `templates/announcements.html` - Announcements
- [ ] `templates/celebrations.html` - Celebrations
- [ ] `templates/skills.html` - Skills
- [ ] `templates/meetings.html` - Meetings
- [ ] `templates/tasks.html` - Tasks
- [ ] `templates/404.html` - Error page
- [ ] `templates/500.html` - Error page

### Static Assets
- [ ] `static/css/style.css` - Custom styles
- [ ] `static/js/script.js` - JavaScript utilities

### Data Files (12 files)
- [ ] `data/users.json` - User accounts
- [ ] `data/leaves.json` - Leave records
- [ ] `data/accomplishments.json` - Accomplishments
- [ ] `data/inventory.json` - Inventory items
- [ ] `data/servers.json` - Test servers
- [ ] `data/builds.json` - Build tracking
- [ ] `data/links.json` - Useful links
- [ ] `data/announcements.json` - Announcements
- [ ] `data/celebrations.json` - Celebrations
- [ ] `data/skills.json` - Skills matrix
- [ ] `data/meetings.json` - Meeting notes
- [ ] `data/tasks.json` - Task tracker

### Documentation
- [ ] `README.md` - Full documentation
- [ ] `CHANGELOG.md` - Version history
- [ ] `QUICK_START.md` - Quick start guide
- [ ] `PROJECT_SUMMARY.md` - Project overview
- [ ] `INSTALLATION_VERIFICATION.md` - This file

### Configuration
- [ ] `.env.example` - Environment template
- [ ] `.gitignore` - Git ignore rules
- [ ] `run.sh` - Linux/macOS startup script
- [ ] `run.bat` - Windows startup script

## 🚀 Installation Steps

### Step 1: Navigate to Project
```bash
cd team_dashboard
```
- [ ] Command executed successfully

### Step 2: Create Virtual Environment
```bash
python -m venv venv
```
- [ ] Virtual environment created
- [ ] `venv/` directory exists

### Step 3: Activate Virtual Environment

**Linux/macOS:**
```bash
source venv/bin/activate
```

**Windows:**
```cmd
venv\Scripts\activate
```
- [ ] Virtual environment activated
- [ ] Prompt shows `(venv)`

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```
- [ ] All packages installed successfully
- [ ] No error messages

### Step 5: Verify Installation
```bash
pip list
```

Check for these packages:
- [ ] Flask (3.0.0)
- [ ] Werkzeug (3.0.1)
- [ ] APScheduler (3.10.4)
- [ ] requests (2.31.0)
- [ ] python-dotenv (1.0.0)

### Step 6: Run Application
```bash
python app.py
```
- [ ] Application starts without errors
- [ ] Shows: `Running on http://127.0.0.1:5000`
- [ ] No error messages in console

## 🌐 Browser Verification

### Step 1: Access Application
Open browser and go to: `http://localhost:5000`
- [ ] Page loads successfully
- [ ] Redirected to login page
- [ ] No 404 or 500 errors

### Step 2: Login Page
- [ ] Login form displays correctly
- [ ] Username and password fields visible
- [ ] "Team Management Dashboard" title shows
- [ ] Bootstrap styling applied

### Step 3: Test Login (Admin)
Credentials: `admin` / `admin`
- [ ] Login successful
- [ ] Redirected to dashboard
- [ ] Welcome message appears

### Step 4: Dashboard Verification
- [ ] Statistics cards display (4 cards)
- [ ] Navigation menu visible
- [ ] Quick actions section shows
- [ ] No console errors (F12)

### Step 5: Navigation Test
Visit each page and verify it loads:
- [ ] Dashboard (`/dashboard`)
- [ ] Leaves (`/leaves`)
- [ ] Accomplishments (`/accomplishments`)
- [ ] Inventory (`/inventory`)
- [ ] Servers (`/servers`)
- [ ] Builds (`/builds`)
- [ ] Links (`/links`)
- [ ] Announcements (`/announcements`)
- [ ] Celebrations (`/celebrations`)
- [ ] Skills (`/skills`)
- [ ] Meetings (`/meetings`)
- [ ] Tasks (`/tasks`)

### Step 6: Functionality Test

**Test Adding Data:**
1. Go to Leaves page
   - [ ] Click "Add Leave" button
   - [ ] Modal opens
   - [ ] Fill in form
   - [ ] Submit successfully
   - [ ] New entry appears in table

2. Go to Accomplishments page
   - [ ] Click "Add Accomplishment" button
   - [ ] Modal opens
   - [ ] Fill in form
   - [ ] Submit successfully
   - [ ] New card appears

**Test Editing Data:**
- [ ] Click edit button on any entry
- [ ] Modal opens with existing data
- [ ] Modify and save
- [ ] Changes appear immediately

**Test Deleting Data:**
- [ ] Click delete button
- [ ] Confirmation dialog appears
- [ ] Confirm deletion
- [ ] Entry removed from view

### Step 7: Logout Test
- [ ] Click user dropdown (top right)
- [ ] Click "Logout"
- [ ] Redirected to login page
- [ ] Session cleared

## 🔧 Optional Features Verification

### Email Configuration (Optional)

1. Create `.env` file:
```bash
cp .env.example .env
```
- [ ] `.env` file created

2. Edit `.env` with Gmail credentials
- [ ] EMAIL_ENABLED=True
- [ ] EMAIL_SENDER configured
- [ ] EMAIL_PASSWORD configured
- [ ] MANAGER_EMAIL configured

3. Restart application
- [ ] No email errors in console

4. Test email (visit `/api/email/test` while logged in)
- [ ] Email sent successfully
- [ ] Check inbox for test email

### Jira Integration (Optional)

1. Edit `.env` file
- [ ] JIRA_ENABLED=True
- [ ] JIRA_URL configured
- [ ] JIRA_USERNAME configured
- [ ] JIRA_API_TOKEN configured

2. Restart application
- [ ] Dashboard shows Jira section
- [ ] Issues display correctly
- [ ] Sync button works

## 🎨 UI/UX Verification

### Desktop View
- [ ] All elements aligned properly
- [ ] Cards display in grid
- [ ] Navigation menu readable
- [ ] Buttons properly sized
- [ ] Modal dialogs centered

### Mobile View (Resize browser or use DevTools)
- [ ] Navigation collapses to hamburger menu
- [ ] Cards stack vertically
- [ ] Tables scroll horizontally
- [ ] Buttons remain clickable
- [ ] Forms usable on small screens

### Browser Compatibility
Test in different browsers:
- [ ] Chrome/Edge
- [ ] Firefox
- [ ] Safari (if available)

## 📊 Data Verification

### Check Sample Data Loaded

1. Dashboard shows:
   - [ ] Team Members: 3
   - [ ] Total Devices: 4
   - [ ] Active Builds: 2

2. Pages show sample entries:
   - [ ] Leaves: 3 entries
   - [ ] Accomplishments: 3 entries
   - [ ] Inventory: 4 items
   - [ ] Servers: 3 servers
   - [ ] Links: 6 links
   - [ ] Skills: 6 skills

## 🔒 Security Verification

- [ ] Can't access pages without login
- [ ] Login required for all routes (except login)
- [ ] Session expires after timeout
- [ ] Passwords are hashed in users.json
- [ ] No sensitive data in console

## ✅ Final Checklist

- [ ] Application starts successfully
- [ ] All pages load without errors
- [ ] Can login with default credentials
- [ ] Can add/edit/delete data
- [ ] Sample data displays correctly
- [ ] Navigation works smoothly
- [ ] UI looks professional
- [ ] Responsive on mobile
- [ ] No console errors
- [ ] Documentation is clear

## 🎉 Success Criteria

If all items above are checked ✅, your installation is **SUCCESSFUL**!

## 🆘 Troubleshooting

### Application won't start
- Check Python version: `python --version` (need 3.11+)
- Reinstall dependencies: `pip install -r requirements.txt`
- Check for port conflicts (default: 5000)

### Pages show errors
- Verify all JSON files exist in `data/` directory
- Check JSON file syntax (use online validator)
- Review console for error messages

### Can't login
- Check `data/users.json` exists
- Verify credentials: admin/admin or john/john123
- Clear browser cache

### Styling looks broken
- Check `static/css/style.css` exists
- Verify internet connection (for Bootstrap CDN)
- Clear browser cache

### Need More Help?
- See [README.md](README.md) for detailed documentation
- See [QUICK_START.md](QUICK_START.md) for setup guide
- Check application logs in terminal

---

## 📝 Installation Notes

**Date Installed:** _______________  
**Python Version:** _______________  
**Issues Encountered:** _______________  
**Resolved:** _______________  
**Notes:** _______________

---

**Installation Verified By:** _______________  
**Date:** _______________  
**Status:** ⬜ Passed / ⬜ Failed

---

**Congratulations!** 🎉

Your Team Management Dashboard is ready to use!

Next Steps:
1. Change default passwords
2. Add your team data
3. Configure email (optional)
4. Set up Jira integration (optional)
5. Customize styling (optional)

**Enjoy managing your team!** 🚀
