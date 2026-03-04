from sqlmodel import Session, select
from models import engine, Bio, Stats
import pandas as pd
from sqlalchemy import func

with Session(engine) as session:
    statement = (
        select(Bio.first_name, Bio.last_name, Stats.GP, Stats.G, Stats.A, Stats.PTS)
        .join(Stats, (Bio.first_name == Stats.first_name)&(Bio.last_name == Stats.last_name))
    )
    records = session.exec(statement).all()

df = pd.DataFrame(records)
print(df)