from sqlmodel import Session
from models import engine
from stats_list import load_stats

with Session(engine) as session:
    stats = load_stats()
    session.add_all(stats)
    session.commit()