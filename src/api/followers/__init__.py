from app import db
from src.config import MAX_USERS
import random

class Followers(db.Model):
    follower_id = db.Column(db.Integer, primary_key=True)
    from_id = db.Column(db.Integer)
    to_id = db.Column(db.Integer)

def generate_followers(target=None):
    IDS = list(range(1, MAX_USERS + 1))

    if target:
        for user_id in [random.choice(IDS) for _ in range(random.randint(1, MAX_USERS // 4))]:
            if not target == user_id:
                db.session.add(Followers(from_id=user_id, to_id=target))
    else:
        for user_id in IDS:
            for follow_id in [random.choice(IDS) for _ in range(random.randint(1, MAX_USERS // 4))]:
                if not user_id == follow_id:
                    db.session.add(Followers(from_id=user_id, to_id=follow_id))
    
    db.session.commit()