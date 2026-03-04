from sqlmodel import Session, select
from models import engine, Bio, Stats
import pandas as pd
from sqlalchemy import func

with Session(engine) as session:
    avg = func.avg(Bio.weight).label("Average Weight")

    statement = (
        select(Bio.position, avg)
        .group_by(Bio.position)
        .having(avg > 190)
    )
    records = session.exec(statement).all()

df = pd.DataFrame(records)
print(df)