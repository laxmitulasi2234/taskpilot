from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Task, User
from . import db
from datetime import datetime
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

main = Blueprint('main', __name__)

# ======================
# 🔐 AUTH ROUTES
# ======================

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered!', 'danger')
            return redirect(url_for('main.register'))

        hashed_password = generate_password_hash(password)
        new_user = User(email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('main.login'))

    return render_template('register.html')


@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            flash('Invalid credentials', 'danger')
            return redirect(url_for('main.login'))

        login_user(user)
        flash('Logged in successfully!', 'success')
        return redirect(url_for('main.home'))

    return render_template('login.html')


@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'info')
    return redirect(url_for('main.login'))

# ======================
# 📋 TASK ROUTES
# ======================

@main.route('/')
@login_required
def home():
    search_query = request.args.get('search', '').strip()
    status_filter = request.args.get('status', '')

    tasks = Task.query

    if search_query:
        tasks = tasks.filter(Task.title.ilike(f'%{search_query}%'))

    if status_filter:
        tasks = tasks.filter_by(status=status_filter)

    tasks = tasks.order_by(Task.due_date).all()

    return render_template('modern_home.html', tasks=tasks)


@main.route('/add', methods=['POST'])
@login_required
def add_task():
    title = request.form['title']
    due_date = datetime.strptime(request.form['due_date'], '%Y-%m-%d').date()
    new_task = Task(title=title, due_date=due_date)
    db.session.add(new_task)
    db.session.commit()
    flash('Task added successfully!', 'success')
    return redirect(url_for('main.home'))


@main.route('/edit/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    if request.method == 'POST':
        task.title = request.form['title']
        task.due_date = datetime.strptime(request.form['due_date'], '%Y-%m-%d')
        db.session.commit()
        flash('Task updated successfully!', 'success')
        return redirect(url_for('main.home'))
    return render_template('edit_task.html', task=task)


@main.route('/delete/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted successfully!', 'success')
    return redirect(url_for('main.home'))


@main.route('/toggle/<int:task_id>', methods=['POST'])
@login_required
def toggle_status(task_id):
    task = Task.query.get_or_404(task_id)
    task.status = 'Completed' if task.status != 'Completed' else 'Pending'
    db.session.commit()
    flash('Task status updated.', 'info')
    return redirect(url_for('main.home'))
