from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os 
import sqlite3
import google.generativeai as genai

#Configure genai key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

#Function to load gemini model
def get_gemini_response(question,prompt):
    model = genai.GenerativeModel(model_name= "gemini-2.5-flash-lite")
    response = model.generate_content([prompt[0], question])
    return response.text

#Function to retrieve query from database
def read_sql_query(sql,db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    for row in rows:
        print(row)
    return rows

#Define prompt
prompt = [
    """
    You are an expert at converting English Sentences to SQL code!
    The SQL database has the name STUDENT and following columns- NAME, CLASS, SECTION
    \n\nFor Example, 
    \nExample 1 - How many enteries of records are present?,
    the SQL command would be something like this SELECT COUNT(*) FROM STUDENT;
    \nExample 1 - Tell me all the students studying in Machine Learning class?,
    the SQL command would be something like this SELECT * FROM STUDENT WHERE CLASS = "Machine Learning";
    Also the SQL command should not have ``` in the beginning or end and sql word in output
    """
]

#Streamlit app creation

st.set_page_config("I can retreive any SQL query")
st.header("Gemini Application to retreive SQL data")

question = st.text_input("Input: ",key="niput")
submit = st.button("Ask the question")

#If submit is clicked
if submit:
    response = get_gemini_response(question,prompt)
    print(response)
    response = read_sql_query(response,"student.db")

    st.subheader("Response:")
    for row in response:
        print(row)
        st.header(row)