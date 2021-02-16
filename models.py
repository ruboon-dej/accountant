from server import db

class AccountMovement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Text)
    action = db.Column(db.Text)
    amount = db.Column(db.Float)

db.create_all()