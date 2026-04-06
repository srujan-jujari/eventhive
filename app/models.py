from app.database import db

# Define the Event model corresponding to the database table
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    tickets = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return f"<Event {self.name}>"
