from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://hlstpdqbdbekbn:0066242495d2ae4bc4ef873bd877aec654223d4e31593a54507bd9ed9a14c780@ec2-3-213-85-90.compute-1.amazonaws.com:5432/d6evpokr06spf9'
db = SQLAlchemy(app)

from models import AccountMovement

db.session.add(AccountMovement(user_id='boon', action='chipotle', amount=-200))
db.session.add(AccountMovement(user_id='boon', action='payday', amount=20000))
db.session.add(AccountMovement(user_id='boom', action='payday', amount=20000))
db.session.commit()