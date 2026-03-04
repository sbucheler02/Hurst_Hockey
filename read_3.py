from sqlmodel import Session, select
from models import engine, Bio, Stats
import pandas as pd
from sqlalchemy import func

with Session(engine) as session:
    statement = (
        select(Bio.position, func.count().label("Number of Players"))
        .group_by(Bio.position)
        .order_by(func.count().desc())
    )
    records = session.exec(statement).all()

df = pd.DataFrame(records)
print(df)