# ⚡ Quick Start Guide

## 🚀 Get Started in 3 Minutes

### Step 1: Install Dependencies

**Linux/macOS:**
```bash
cd team_dashboard
./run.sh
```

**Windows:**
```cmd
cd team_dashboard
run.bat
```

**Manual installation:**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### Step 2: Access the Application

Open your browser: **http://localhost:5000**

### Step 3: Login

**Admin Account:**
- Username: `admin`
- Password: `admin`

**Team Member Account:**
- Username: `john`
- Password: `john123`

---

## 📋 What You Can Do

### Immediately Available (No Setup Required)
✅ Login and explore the dashboard  
✅ Add/edit leaves  
✅ Log accomplishments  
✅ Manage inventory  
✅ Track test servers  
✅ Monitor builds  
✅ Add useful links  
✅ Post announcements  
✅ Celebrate wins  
✅ Track skills  
✅ Record meeting notes  
✅ Assign tasks  

### Optional Features (Require Configuration)

#### Enable Email Notifications
1. Create `.env` file (copy from `.env.example`)
2. Add Gmail credentials:
   ```
   EMAIL_ENABLED=True
   EMAIL_SENDER=your-email@gmail.com
   EMAIL_PASSWORD=your-app-password
   MANAGER_EMAIL=manager@company.com
   ```
3. Restart the application

#### Enable Jira Integration
1. Edit `.env` file
2. Add Jira credentials:
   ```
   JIRA_ENABLED=True
   JIRA_URL=https://yourcompany.atlassian.net
   JIRA_USERNAME=your-email@company.com
   JIRA_API_TOKEN=your-api-token
   JIRA_PROJECT_KEY=QA
   ```
3. Restart the application

---

## 🗺️ Page Navigation

| Page | URL | Description |
|------|-----|-------------|
| Dashboard | `/dashboard` | Overview and statistics |
| Leaves | `/leaves` | Leave management |
| Accomplishments | `/accomplishments` | Team achievements |
| Inventory | `/inventory` | Hardware tracking |
| Servers | `/servers` | Test server management |
| Builds | `/builds` | Build tracking |
| Links | `/links` | Useful resources |
| Announcements | `/announcements` | Team updates |
| Celebrations | `/celebrations` | Milestones |
| Skills | `/skills` | Skills matrix |
| Meetings | `/meetings` | Meeting notes |
| Tasks | `/tasks` | Task tracker |

---

## 💡 Pro Tips

1. **Change Default Passwords** - Update in `data/users.json`
2. **Backup Data** - Copy the `data/` folder regularly
3. **Customize Theme** - Edit `static/css/style.css`
4. **Daily Emails** - Sent automatically at 6 PM (if configured)
5. **Mobile Friendly** - Access from any device

---

## 🆘 Common Issues

### Port Already in Use
```bash
# Change port in app.py (last line):
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Module Not Found
```bash
pip install -r requirements.txt
```

### Can't Login
- Default credentials: admin/admin or john/john123
- Check `data/users.json` exists

---

## 📚 Full Documentation

For detailed documentation, see [README.md](README.md)

---

**Need Help?** Check the troubleshooting section in README.md
