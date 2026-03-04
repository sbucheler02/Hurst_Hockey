from sqlmodel import Session, select
from models import engine, Bio, Stats
import pandas as pd

with Session(engine) as session:
    statement = select(Bio.first_name, Bio.last_name, Bio.position)
    records = session.exec(statement).all()

df = pd.DataFrame(records, columns=["first_name", "last_name", "position"])
print(df)