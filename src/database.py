import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime

def init_database():
    engine = create_engine('sqlite:///qa_database.db')
    df = pd.read_csv('data/question_answer.csv')
    df.to_sql('qa_table', con=engine, if_exists='replace', index=False)

    history_df = pd.DataFrame(columns=["user", "chatbot", "timestamp", "sources"]) 
    history_df.to_sql('history_table', con=engine, if_exists='replace', index=False)

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

def save_history(user, chatbot, sources):
    engine = create_engine('sqlite:///qa_database.db')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    history_df = pd.DataFrame([{
        "user": user,
        "chatbot": chatbot,
        "sources": ", ".join(sources),  # Lưu danh sách sources dưới dạng chuỗi
        "timestamp": timestamp
    }])

    history_df.to_sql('history_table', con=engine, if_exists='append', index=False)

def get_history():
    engine = create_engine('sqlite:///qa_database.db')
    return pd.read_sql_table('history_table', engine)

# init_database()
# add_data_to_database("data/data.csv")

# df = get_qa_data()
# print(df)