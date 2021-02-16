from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from server import user_id

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://hlstpdqbdbekbn:0066242495d2ae4bc4ef873bd877aec654223d4e31593a54507bd9ed9a14c780@ec2-3-213-85-90.compute-1.amazonaws.com:5432/d6evpokr06spf9'
db = SQLAlchemy(app)

class AccountMovement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Text)
    action = db.Column(db.Text)
    amount = db.Column(db.Float)

accounts = AccountMovement.query.filter(user_id=user_id)
for account in accounts:
    action = account.action
    print (action)