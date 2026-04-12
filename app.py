from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os
from functools import wraps

app = Flask(__name__)
# Secure standard secret key for simple demo
app.secret_key = 'eventhive_secret_key'
DB_FILE = 'database.db'

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    # Users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    # Events table
    c.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            tickets INTEGER NOT NULL
        )
    ''')
    # Bookings table
    c.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            event_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (event_id) REFERENCES events (id)
        )
    ''')
    # Hardcoded admin init
    c.execute("SELECT * FROM users WHERE username = 'admin'")
    if not c.fetchone():
        c.execute("INSERT INTO users (username, password) VALUES ('admin', 'admin')")
    conn.commit()
    conn.close()

# Auto-initialize the database on startup
init_db()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
    conn = get_db_connection()
    events = conn.execute('SELECT * FROM events').fetchall()
    conn.close()
    return render_template('index.html', events=events)

@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already exists.', 'danger')
        finally:
            conn.close()
            
    return render_template('register.html')

@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
        conn.close()
        
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash('Logged in successfully.', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'danger')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    conn = get_db_connection()
    events = conn.execute('SELECT * FROM events').fetchall()
    
    # User's bookings
    bookings = conn.execute('''
        SELECT events.name FROM bookings 
        JOIN events ON bookings.event_id = events.id 
        WHERE bookings.user_id = ?
    ''', (session['user_id'],)).fetchall()
    conn.close()
    
    return render_template('dashboard.html', events=events, bookings=bookings)

@app.route('/create_event', methods=('GET', 'POST'))
@login_required
def create_event():
    # Only allow admin
    if session.get('username') != 'admin':
        flash('Only admins can create events.', 'danger')
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        name = request.form['name']
        tickets = request.form['tickets']
        
        try:
            tickets_int = int(tickets)
            if tickets_int < 0:
                raise ValueError
        except ValueError:
            flash('Tickets must be a valid positive number.', 'danger')
            return render_template('create_event.html')

        conn = get_db_connection()
        conn.execute('INSERT INTO events (name, tickets) VALUES (?, ?)', (name, tickets_int))
        conn.commit()
        conn.close()
        flash('Event created successfully!', 'success')
        return redirect(url_for('dashboard'))
        
    return render_template('create_event.html')

@app.route('/book/<int:event_id>', methods=('POST',))
@login_required
def book(event_id):
    conn = get_db_connection()
    event = conn.execute('SELECT * FROM events WHERE id = ?', (event_id,)).fetchone()
    
    if event is None:
        flash('Event not found.', 'danger')
    elif event['tickets'] <= 0:
        flash('Sorry, tickets are sold out.', 'danger')
    else:
        # Check for existing booking
        existing_booking = conn.execute('SELECT * FROM bookings WHERE user_id = ? AND event_id = ?', 
                                        (session['user_id'], event_id)).fetchone()
        if existing_booking:
            flash('You have already booked a ticket for this event.', 'warning')
        else:
            # Atomic update
            conn.execute('UPDATE events SET tickets = tickets - 1 WHERE id = ? AND tickets > 0', (event_id,))
            conn.execute('INSERT INTO bookings (user_id, event_id) VALUES (?, ?)', (session['user_id'], event_id))
            conn.commit()
            flash('Ticket booked successfully!', 'success')
            
    conn.close()
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
