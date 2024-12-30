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

def add_data_to_database(path_data):
    engine = create_engine('sqlite:///qa_database.db')
    df_new = pd.read_csv(path_data)

    # Thêm dữ liệu vào bảng, đảm bảo không trùng lặp
    existing_data = pd.read_sql_table('qa_table', engine)
    combined_data = pd.concat([existing_data, df_new]).drop_duplicates()

    combined_data.to_sql('qa_table', con=engine, if_exists='replace', index=False)

# init_database()
add_data_to_database("/home/loylp/project/UIT-InfoBot/data/data.csv")

df = get_qa_data()
print(df)