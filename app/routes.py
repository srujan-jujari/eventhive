from flask import Blueprint, render_template, request, redirect, url_for
from app.models import Event
from app.database import db

# Create a Blueprint object for routing
main = Blueprint('main', __name__)

@main.route('/')
def index():
    # Fetch all events from the database to display on the home page
    events = Event.query.all()
    return render_template('index.html', events=events)

@main.route('/add', methods=['POST'])
def add_event():
    # Retrieve form data
    name = request.form.get('name')
    tickets = request.form.get('tickets')
    
    if name and tickets:
        # Create a new event object and add it to the database
        new_event = Event(name=name, tickets=int(tickets))
        db.session.add(new_event)
        db.session.commit()
    
    # Redirect back to the home page
    return redirect(url_for('main.index'))

@main.route('/book/<int:id>', methods=['POST'])
def book_ticket(id):
    # Fetch the event by its ID
    event = Event.query.get_or_404(id)
    
    # If there are available tickets, decrease the count and save
    if event.tickets > 0:
        event.tickets -= 1
        db.session.commit()
        
    return redirect(url_for('main.index'))
