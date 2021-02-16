from server import db
from models import AccountMovement

db.session.add(AccountMovement(user_id='boon', action='chipotle', amount=-200))
db.session.add(AccountMovement(user_id='boon', action='payday', amount=20000))
db.session.add(AccountMovement(user_id='boom', action='payday', amount=20000))
db.session.commit()