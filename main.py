# main.py

import streamlit as st
from sqlalchemy import create_engine
from langchain_groq import ChatGroq
from langchain_helper import get_few_shot_db_chain, process_question

# ---------------- Streamlit Setup ----------------
st.set_page_config(page_title="AtliQ T-Shirts Q&A", layout="wide")
st.title("👕 AtliQ T-Shirts: Ask anything!")

# ---------------- MySQL Setup ----------------
# Update your MySQL password if needed
engine = create_engine("mysql+pymysql://root:2026@localhost/atliq_tshirts")

# ---------------- LLM Setup ----------------
# Use the latest Groq model (replace with active model from https://console.groq.com/)
llm = ChatGroq(model="llama-3.3-70b-versatile")  
sql_chain = get_few_shot_db_chain(llm)

# ---------------- User Input ----------------
question = st.text_input("Ask about the T-shirts (e.g., 'How many Red T-shirts?')")

if st.button("Get Answer") and question:
    with st.spinner("Generating SQL and fetching results..."):
        try:
            # Get data and SQL
            data, sql = process_question(question, sql_chain, engine, return_sql=True)
            
            st.success("✅ Done!")
            st.write("### Generated SQL:")
            st.code(sql)
            st.write("### Query Result:")
            st.table(data)
        except Exception as e:
            st.error(f"❌ Error: {e}")
