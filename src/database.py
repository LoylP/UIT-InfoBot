import pandas as pd
from sqlalchemy import create_engine

def init_database():
    engine = create_engine('sqlite:///qa_database.db')
    df = pd.read_csv('data/question_answer.csv')
    df.to_sql('qa_table', con=engine, if_exists='replace', index=False)
    return df

def get_qa_data():
    engine = create_engine('sqlite:///qa_database.db')
    return pd.read_sql_table('qa_table', engine)

# init_database()
# df = get_qa_data()
# print(df)