from sqlmodel import Session, select
from models import engine, Bio, Stats
import pandas as pd

with Session(engine) as session:
    statement = select(Bio)
    records = session.exec(statement).all()

dic_list = []
for record in records:
    player_dict = record.model_dump()
    dic_list.append(player_dict)

df = pd.DataFrame(dic_list)
print(df)