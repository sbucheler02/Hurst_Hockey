from sqlmodel import Session
from models import engine
from bio_list import load_bios

with Session(engine) as session:
    bios = load_bios()
    session.add_all(bios)
    session.commit()