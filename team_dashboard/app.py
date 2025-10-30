"""
Team Management Dashboard - Flask Application
Main application file with all routes
"""
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

from config import Config
from utils import (
    login_required, admin_required, hash_password,
    load_json_file, save_json_file, get_next_id,
    format_date, get_today, send_email,
    generate_daily_summary, fetch_jira_issues,
    get_dashboard_stats
)

app = Flask(__name__)
app.config.from_object(Config)

# Initialize scheduler for daily emails
scheduler = BackgroundScheduler()
scheduler.start()

# Schedule daily email at configured time
def send_daily_summary():
    """Send daily summary email"""
    summary_html = generate_daily_summary()
    send_email(
        subject=f"Daily Team Summary - {format_date(get_today())}",
        body=summary_html
    )

# Add job to scheduler
scheduler.add_job(
    func=send_daily_summary,
    trigger="cron",
    hour=Config.EMAIL_SCHEDULE_HOUR,
    minute=Config.EMAIL_SCHEDULE_MINUTE
)

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())


# ============================================================================
# Authentication Routes
# ============================================================================

@app.route('/')
def index():
    """Redirect to dashboard or login"""
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Load users
        users = load_json_file('users.json')
        
        # Authenticate
        hashed_password = hash_password(password)
        user = next((u for u in users if u['username'] == username and u['password'] == hashed_password), None)
        
        if user:
            session['user'] = username
            session['role'] = user['role']
            session['name'] = user['name']
            flash(f'Welcome back, {user["name"]}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html')


@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    flash('You have been logged out successfully', 'info')
    return redirect(url_for('login'))


# ============================================================================
# Dashboard
# ============================================================================

@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard"""
    stats = get_dashboard_stats()
    
    # Get Jira issues if enabled
    jira_issues = []
    if Config.JIRA_ENABLED:
        jira_issues = fetch_jira_issues()[:5]  # Get top 5
    
    return render_template('dashboard.html', stats=stats, jira_issues=jira_issues)


# ============================================================================
# Leave Management Routes
# ============================================================================

@app.route('/leaves')
@login_required
def leaves():
    """Leave tracking page"""
    leaves_data = load_json_file('leaves.json')
    leaves_data.sort(key=lambda x: x.get('date', ''), reverse=True)
    return render_template('leaves.html', leaves=leaves_data)


@app.route('/leaves/add', methods=['POST'])
@login_required
def add_leave():
    """Add new leave entry"""
    leaves_data = load_json_file('leaves.json')
    
    new_leave = {
        'id': get_next_id(leaves_data),
        'name': request.form.get('name'),
        'date': request.form.get('date'),
        'type': request.form.get('type'),
        'reason': request.form.get('reason'),
        'approval_status': request.form.get('approval_status', 'pending')
    }
    
    leaves_data.append(new_leave)
    save_json_file('leaves.json', leaves_data)
    
    flash('Leave entry added successfully', 'success')
    return redirect(url_for('leaves'))


@app.route('/leaves/edit/<int:leave_id>', methods=['POST'])
@login_required
def edit_leave(leave_id):
    """Edit leave entry"""
    leaves_data = load_json_file('leaves.json')
    
    for leave in leaves_data:
        if leave['id'] == leave_id:
            leave['name'] = request.form.get('name')
            leave['date'] = request.form.get('date')
            leave['type'] = request.form.get('type')
            leave['reason'] = request.form.get('reason')
            leave['approval_status'] = request.form.get('approval_status')
            break
    
    save_json_file('leaves.json', leaves_data)
    flash('Leave entry updated successfully', 'success')
    return redirect(url_for('leaves'))


@app.route('/leaves/delete/<int:leave_id>')
@login_required
def delete_leave(leave_id):
    """Delete leave entry"""
    leaves_data = load_json_file('leaves.json')
    leaves_data = [l for l in leaves_data if l['id'] != leave_id]
    save_json_file('leaves.json', leaves_data)
    
    flash('Leave entry deleted successfully', 'success')
    return redirect(url_for('leaves'))


# ============================================================================
# Accomplishments Routes
# ============================================================================

@app.route('/accomplishments')
@login_required
def accomplishments():
    """Accomplishments page"""
    accomplishments_data = load_json_file('accomplishments.json')
    accomplishments_data.sort(key=lambda x: x.get('date', ''), reverse=True)
    return render_template('accomplishments.html', accomplishments=accomplishments_data)


@app.route('/accomplishments/add', methods=['POST'])
@login_required
def add_accomplishment():
    """Add new accomplishment"""
    accomplishments_data = load_json_file('accomplishments.json')
    
    new_accomplishment = {
        'id': get_next_id(accomplishments_data),
        'date': request.form.get('date'),
        'member_name': request.form.get('member_name'),
        'description': request.form.get('description'),
        'impact': request.form.get('impact'),
        'type': request.form.get('type')
    }
    
    accomplishments_data.append(new_accomplishment)
    save_json_file('accomplishments.json', accomplishments_data)
    
    flash('Accomplishment added successfully', 'success')
    return redirect(url_for('accomplishments'))


@app.route('/accomplishments/edit/<int:acc_id>', methods=['POST'])
@login_required
def edit_accomplishment(acc_id):
    """Edit accomplishment"""
    accomplishments_data = load_json_file('accomplishments.json')
    
    for acc in accomplishments_data:
        if acc['id'] == acc_id:
            acc['date'] = request.form.get('date')
            acc['member_name'] = request.form.get('member_name')
            acc['description'] = request.form.get('description')
            acc['impact'] = request.form.get('impact')
            acc['type'] = request.form.get('type')
            break
    
    save_json_file('accomplishments.json', accomplishments_data)
    flash('Accomplishment updated successfully', 'success')
    return redirect(url_for('accomplishments'))


@app.route('/accomplishments/delete/<int:acc_id>')
@login_required
def delete_accomplishment(acc_id):
    """Delete accomplishment"""
    accomplishments_data = load_json_file('accomplishments.json')
    accomplishments_data = [a for a in accomplishments_data if a['id'] != acc_id]
    save_json_file('accomplishments.json', accomplishments_data)
    
    flash('Accomplishment deleted successfully', 'success')
    return redirect(url_for('accomplishments'))


# ============================================================================
# Inventory Routes
# ============================================================================

@app.route('/inventory')
@login_required
def inventory():
    """Inventory page"""
    inventory_data = load_json_file('inventory.json')
    return render_template('inventory.html', inventory=inventory_data)


@app.route('/inventory/add', methods=['POST'])
@login_required
def add_inventory():
    """Add inventory item"""
    inventory_data = load_json_file('inventory.json')
    
    new_item = {
        'id': get_next_id(inventory_data),
        'item_name': request.form.get('item_name'),
        'assigned_to': request.form.get('assigned_to'),
        'serial_no': request.form.get('serial_no'),
        'condition': request.form.get('condition'),
        'remarks': request.form.get('remarks')
    }
    
    inventory_data.append(new_item)
    save_json_file('inventory.json', inventory_data)
    
    flash('Inventory item added successfully', 'success')
    return redirect(url_for('inventory'))


@app.route('/inventory/edit/<int:item_id>', methods=['POST'])
@login_required
def edit_inventory(item_id):
    """Edit inventory item"""
    inventory_data = load_json_file('inventory.json')
    
    for item in inventory_data:
        if item['id'] == item_id:
            item['item_name'] = request.form.get('item_name')
            item['assigned_to'] = request.form.get('assigned_to')
            item['serial_no'] = request.form.get('serial_no')
            item['condition'] = request.form.get('condition')
            item['remarks'] = request.form.get('remarks')
            break
    
    save_json_file('inventory.json', inventory_data)
    flash('Inventory item updated successfully', 'success')
    return redirect(url_for('inventory'))


@app.route('/inventory/delete/<int:item_id>')
@login_required
def delete_inventory(item_id):
    """Delete inventory item"""
    inventory_data = load_json_file('inventory.json')
    inventory_data = [i for i in inventory_data if i['id'] != item_id]
    save_json_file('inventory.json', inventory_data)
    
    flash('Inventory item deleted successfully', 'success')
    return redirect(url_for('inventory'))


# ============================================================================
# Server Routes
# ============================================================================

@app.route('/servers')
@login_required
def servers():
    """Servers page"""
    servers_data = load_json_file('servers.json')
    return render_template('servers.html', servers=servers_data)


@app.route('/servers/add', methods=['POST'])
@login_required
def add_server():
    """Add server"""
    servers_data = load_json_file('servers.json')
    
    new_server = {
        'id': get_next_id(servers_data),
        'server_name': request.form.get('server_name'),
        'ip': request.form.get('ip'),
        'os': request.form.get('os'),
        'purpose': request.form.get('purpose'),
        'assigned_team': request.form.get('assigned_team'),
        'attached_devices': request.form.get('attached_devices'),
        'status': request.form.get('status')
    }
    
    servers_data.append(new_server)
    save_json_file('servers.json', servers_data)
    
    flash('Server added successfully', 'success')
    return redirect(url_for('servers'))


@app.route('/servers/edit/<int:server_id>', methods=['POST'])
@login_required
def edit_server(server_id):
    """Edit server"""
    servers_data = load_json_file('servers.json')
    
    for server in servers_data:
        if server['id'] == server_id:
            server['server_name'] = request.form.get('server_name')
            server['ip'] = request.form.get('ip')
            server['os'] = request.form.get('os')
            server['purpose'] = request.form.get('purpose')
            server['assigned_team'] = request.form.get('assigned_team')
            server['attached_devices'] = request.form.get('attached_devices')
            server['status'] = request.form.get('status')
            break
    
    save_json_file('servers.json', servers_data)
    flash('Server updated successfully', 'success')
    return redirect(url_for('servers'))


@app.route('/servers/delete/<int:server_id>')
@login_required
def delete_server(server_id):
    """Delete server"""
    servers_data = load_json_file('servers.json')
    servers_data = [s for s in servers_data if s['id'] != server_id]
    save_json_file('servers.json', servers_data)
    
    flash('Server deleted successfully', 'success')
    return redirect(url_for('servers'))


# ============================================================================
# Build Routes
# ============================================================================

@app.route('/builds')
@login_required
def builds():
    """Builds page"""
    builds_data = load_json_file('builds.json')
    builds_data.sort(key=lambda x: x.get('date', ''), reverse=True)
    return render_template('builds.html', builds=builds_data)


@app.route('/builds/add', methods=['POST'])
@login_required
def add_build():
    """Add build"""
    builds_data = load_json_file('builds.json')
    
    new_build = {
        'id': get_next_id(builds_data),
        'build_name': request.form.get('build_name'),
        'version': request.form.get('version'),
        'date': request.form.get('date'),
        'environment': request.form.get('environment'),
        'status': request.form.get('status'),
        'changelog_url': request.form.get('changelog_url')
    }
    
    builds_data.append(new_build)
    save_json_file('builds.json', builds_data)
    
    flash('Build added successfully', 'success')
    return redirect(url_for('builds'))


@app.route('/builds/edit/<int:build_id>', methods=['POST'])
@login_required
def edit_build(build_id):
    """Edit build"""
    builds_data = load_json_file('builds.json')
    
    for build in builds_data:
        if build['id'] == build_id:
            build['build_name'] = request.form.get('build_name')
            build['version'] = request.form.get('version')
            build['date'] = request.form.get('date')
            build['environment'] = request.form.get('environment')
            build['status'] = request.form.get('status')
            build['changelog_url'] = request.form.get('changelog_url')
            break
    
    save_json_file('builds.json', builds_data)
    flash('Build updated successfully', 'success')
    return redirect(url_for('builds'))


@app.route('/builds/delete/<int:build_id>')
@login_required
def delete_build(build_id):
    """Delete build"""
    builds_data = load_json_file('builds.json')
    builds_data = [b for b in builds_data if b['id'] != build_id]
    save_json_file('builds.json', builds_data)
    
    flash('Build deleted successfully', 'success')
    return redirect(url_for('builds'))


# ============================================================================
# Links Routes
# ============================================================================

@app.route('/links')
@login_required
def links():
    """Links page"""
    links_data = load_json_file('links.json')
    return render_template('links.html', links=links_data)


@app.route('/links/add', methods=['POST'])
@login_required
def add_link():
    """Add link"""
    links_data = load_json_file('links.json')
    
    new_link = {
        'id': get_next_id(links_data),
        'title': request.form.get('title'),
        'url': request.form.get('url'),
        'category': request.form.get('category'),
        'description': request.form.get('description')
    }
    
    links_data.append(new_link)
    save_json_file('links.json', links_data)
    
    flash('Link added successfully', 'success')
    return redirect(url_for('links'))


@app.route('/links/edit/<int:link_id>', methods=['POST'])
@login_required
def edit_link(link_id):
    """Edit link"""
    links_data = load_json_file('links.json')
    
    for link in links_data:
        if link['id'] == link_id:
            link['title'] = request.form.get('title')
            link['url'] = request.form.get('url')
            link['category'] = request.form.get('category')
            link['description'] = request.form.get('description')
            break
    
    save_json_file('links.json', links_data)
    flash('Link updated successfully', 'success')
    return redirect(url_for('links'))


@app.route('/links/delete/<int:link_id>')
@login_required
def delete_link(link_id):
    """Delete link"""
    links_data = load_json_file('links.json')
    links_data = [l for l in links_data if l['id'] != link_id]
    save_json_file('links.json', links_data)
    
    flash('Link deleted successfully', 'success')
    return redirect(url_for('links'))


# ============================================================================
# Announcements Routes
# ============================================================================

@app.route('/announcements')
@login_required
def announcements():
    """Announcements page"""
    announcements_data = load_json_file('announcements.json')
    announcements_data.sort(key=lambda x: x.get('date', ''), reverse=True)
    return render_template('announcements.html', announcements=announcements_data)


@app.route('/announcements/add', methods=['POST'])
@login_required
def add_announcement():
    """Add announcement"""
    announcements_data = load_json_file('announcements.json')
    
    new_announcement = {
        'id': get_next_id(announcements_data),
        'date': request.form.get('date'),
        'title': request.form.get('title'),
        'message': request.form.get('message'),
        'posted_by': session.get('name', 'Unknown')
    }
    
    announcements_data.append(new_announcement)
    save_json_file('announcements.json', announcements_data)
    
    flash('Announcement added successfully', 'success')
    return redirect(url_for('announcements'))


@app.route('/announcements/edit/<int:ann_id>', methods=['POST'])
@login_required
def edit_announcement(ann_id):
    """Edit announcement"""
    announcements_data = load_json_file('announcements.json')
    
    for ann in announcements_data:
        if ann['id'] == ann_id:
            ann['date'] = request.form.get('date')
            ann['title'] = request.form.get('title')
            ann['message'] = request.form.get('message')
            break
    
    save_json_file('announcements.json', announcements_data)
    flash('Announcement updated successfully', 'success')
    return redirect(url_for('announcements'))


@app.route('/announcements/delete/<int:ann_id>')
@login_required
def delete_announcement(ann_id):
    """Delete announcement"""
    announcements_data = load_json_file('announcements.json')
    announcements_data = [a for a in announcements_data if a['id'] != ann_id]
    save_json_file('announcements.json', announcements_data)
    
    flash('Announcement deleted successfully', 'success')
    return redirect(url_for('announcements'))


# ============================================================================
# Celebrations Routes
# ============================================================================

@app.route('/celebrations')
@login_required
def celebrations():
    """Celebrations page"""
    celebrations_data = load_json_file('celebrations.json')
    celebrations_data.sort(key=lambda x: x.get('date', ''), reverse=True)
    return render_template('celebrations.html', celebrations=celebrations_data)


@app.route('/celebrations/add', methods=['POST'])
@login_required
def add_celebration():
    """Add celebration"""
    celebrations_data = load_json_file('celebrations.json')
    
    new_celebration = {
        'id': get_next_id(celebrations_data),
        'date': request.form.get('date'),
        'member_name': request.form.get('member_name'),
        'event_type': request.form.get('event_type'),
        'message': request.form.get('message'),
        'photo_url': request.form.get('photo_url', '')
    }
    
    celebrations_data.append(new_celebration)
    save_json_file('celebrations.json', celebrations_data)
    
    flash('Celebration added successfully', 'success')
    return redirect(url_for('celebrations'))


@app.route('/celebrations/edit/<int:cel_id>', methods=['POST'])
@login_required
def edit_celebration(cel_id):
    """Edit celebration"""
    celebrations_data = load_json_file('celebrations.json')
    
    for cel in celebrations_data:
        if cel['id'] == cel_id:
            cel['date'] = request.form.get('date')
            cel['member_name'] = request.form.get('member_name')
            cel['event_type'] = request.form.get('event_type')
            cel['message'] = request.form.get('message')
            cel['photo_url'] = request.form.get('photo_url', '')
            break
    
    save_json_file('celebrations.json', celebrations_data)
    flash('Celebration updated successfully', 'success')
    return redirect(url_for('celebrations'))


@app.route('/celebrations/delete/<int:cel_id>')
@login_required
def delete_celebration(cel_id):
    """Delete celebration"""
    celebrations_data = load_json_file('celebrations.json')
    celebrations_data = [c for c in celebrations_data if c['id'] != cel_id]
    save_json_file('celebrations.json', celebrations_data)
    
    flash('Celebration deleted successfully', 'success')
    return redirect(url_for('celebrations'))


# ============================================================================
# Skills Routes
# ============================================================================

@app.route('/skills')
@login_required
def skills():
    """Skills matrix page"""
    skills_data = load_json_file('skills.json')
    
    # Group skills by team member
    skills_by_member = {}
    for skill in skills_data:
        name = skill.get('name')
        if name not in skills_by_member:
            skills_by_member[name] = []
        skills_by_member[name].append(skill)
    
    return render_template('skills.html', skills=skills_data, skills_by_member=skills_by_member)


@app.route('/skills/add', methods=['POST'])
@login_required
def add_skill():
    """Add skill"""
    skills_data = load_json_file('skills.json')
    
    new_skill = {
        'id': get_next_id(skills_data),
        'name': request.form.get('name'),
        'skill': request.form.get('skill'),
        'level': request.form.get('level'),
        'last_updated': request.form.get('last_updated', get_today())
    }
    
    skills_data.append(new_skill)
    save_json_file('skills.json', skills_data)
    
    flash('Skill added successfully', 'success')
    return redirect(url_for('skills'))


@app.route('/skills/edit/<int:skill_id>', methods=['POST'])
@login_required
def edit_skill(skill_id):
    """Edit skill"""
    skills_data = load_json_file('skills.json')
    
    for skill in skills_data:
        if skill['id'] == skill_id:
            skill['name'] = request.form.get('name')
            skill['skill'] = request.form.get('skill')
            skill['level'] = request.form.get('level')
            skill['last_updated'] = request.form.get('last_updated')
            break
    
    save_json_file('skills.json', skills_data)
    flash('Skill updated successfully', 'success')
    return redirect(url_for('skills'))


@app.route('/skills/delete/<int:skill_id>')
@login_required
def delete_skill(skill_id):
    """Delete skill"""
    skills_data = load_json_file('skills.json')
    skills_data = [s for s in skills_data if s['id'] != skill_id]
    save_json_file('skills.json', skills_data)
    
    flash('Skill deleted successfully', 'success')
    return redirect(url_for('skills'))


# ============================================================================
# Meetings Routes
# ============================================================================

@app.route('/meetings')
@login_required
def meetings():
    """Meetings page"""
    meetings_data = load_json_file('meetings.json')
    meetings_data.sort(key=lambda x: x.get('date', ''), reverse=True)
    return render_template('meetings.html', meetings=meetings_data)


@app.route('/meetings/add', methods=['POST'])
@login_required
def add_meeting():
    """Add meeting"""
    meetings_data = load_json_file('meetings.json')
    
    new_meeting = {
        'id': get_next_id(meetings_data),
        'date': request.form.get('date'),
        'topic': request.form.get('topic'),
        'action_items': request.form.get('action_items'),
        'owner': request.form.get('owner'),
        'status': request.form.get('status')
    }
    
    meetings_data.append(new_meeting)
    save_json_file('meetings.json', meetings_data)
    
    flash('Meeting added successfully', 'success')
    return redirect(url_for('meetings'))


@app.route('/meetings/edit/<int:meeting_id>', methods=['POST'])
@login_required
def edit_meeting(meeting_id):
    """Edit meeting"""
    meetings_data = load_json_file('meetings.json')
    
    for meeting in meetings_data:
        if meeting['id'] == meeting_id:
            meeting['date'] = request.form.get('date')
            meeting['topic'] = request.form.get('topic')
            meeting['action_items'] = request.form.get('action_items')
            meeting['owner'] = request.form.get('owner')
            meeting['status'] = request.form.get('status')
            break
    
    save_json_file('meetings.json', meetings_data)
    flash('Meeting updated successfully', 'success')
    return redirect(url_for('meetings'))


@app.route('/meetings/delete/<int:meeting_id>')
@login_required
def delete_meeting(meeting_id):
    """Delete meeting"""
    meetings_data = load_json_file('meetings.json')
    meetings_data = [m for m in meetings_data if m['id'] != meeting_id]
    save_json_file('meetings.json', meetings_data)
    
    flash('Meeting deleted successfully', 'success')
    return redirect(url_for('meetings'))


# ============================================================================
# Tasks Routes
# ============================================================================

@app.route('/tasks')
@login_required
def tasks():
    """Tasks page"""
    tasks_data = load_json_file('tasks.json')
    return render_template('tasks.html', tasks=tasks_data)


@app.route('/tasks/add', methods=['POST'])
@login_required
def add_task():
    """Add task"""
    tasks_data = load_json_file('tasks.json')
    
    new_task = {
        'id': get_next_id(tasks_data),
        'member_name': request.form.get('member_name'),
        'project': request.form.get('project'),
        'task_description': request.form.get('task_description'),
        'start_date': request.form.get('start_date'),
        'due_date': request.form.get('due_date'),
        'status': request.form.get('status')
    }
    
    tasks_data.append(new_task)
    save_json_file('tasks.json', tasks_data)
    
    flash('Task added successfully', 'success')
    return redirect(url_for('tasks'))


@app.route('/tasks/edit/<int:task_id>', methods=['POST'])
@login_required
def edit_task(task_id):
    """Edit task"""
    tasks_data = load_json_file('tasks.json')
    
    for task in tasks_data:
        if task['id'] == task_id:
            task['member_name'] = request.form.get('member_name')
            task['project'] = request.form.get('project')
            task['task_description'] = request.form.get('task_description')
            task['start_date'] = request.form.get('start_date')
            task['due_date'] = request.form.get('due_date')
            task['status'] = request.form.get('status')
            break
    
    save_json_file('tasks.json', tasks_data)
    flash('Task updated successfully', 'success')
    return redirect(url_for('tasks'))


@app.route('/tasks/delete/<int:task_id>')
@login_required
def delete_task(task_id):
    """Delete task"""
    tasks_data = load_json_file('tasks.json')
    tasks_data = [t for t in tasks_data if t['id'] != task_id]
    save_json_file('tasks.json', tasks_data)
    
    flash('Task deleted successfully', 'success')
    return redirect(url_for('tasks'))


# ============================================================================
# API Routes (for AJAX calls)
# ============================================================================

@app.route('/api/jira/sync')
@login_required
def sync_jira():
    """Sync Jira issues"""
    issues = fetch_jira_issues()
    return jsonify({'success': True, 'issues': issues, 'count': len(issues)})


@app.route('/api/email/test')
@login_required
def test_email():
    """Test email functionality"""
    result = send_email(
        subject="Test Email from Team Dashboard",
        body="<h2>This is a test email</h2><p>If you received this, email is configured correctly.</p>"
    )
    return jsonify({'success': result})


@app.route('/api/email/send-summary')
@login_required
def trigger_email_summary():
    """Manually trigger daily summary email"""
    send_daily_summary()
    return jsonify({'success': True, 'message': 'Daily summary email sent'})


# ============================================================================
# Template Filters
# ============================================================================

@app.template_filter('format_date')
def format_date_filter(date_str):
    """Format date for display"""
    return format_date(date_str)


# ============================================================================
# Error Handlers
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """404 error handler"""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """500 error handler"""
    return render_template('500.html'), 500


# ============================================================================
# Main
# ============================================================================

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
