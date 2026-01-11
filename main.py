# main.py

import streamlit as st
from sqlalchemy import create_engine, text
from langchain_groq import ChatGroq
from langchain_helper import get_few_shot_db_chain, process_question
import os
import base64


def set_bg(image_path):
    with open(image_path, "rb") as img_file:
        b64 = base64.b64encode(img_file.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
           background:
        linear-gradient(rgba(0,0,0,0.65), rgba(0,0,0,0.65)),
        url("data:image/jpg;base64,{b64}"); 
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


if "history" not in st.session_state:
    st.session_state.history = []
# 🔥 set background image
set_bg("bg2.jpg")

# ---------- Page Config ----------
st.set_page_config(
    page_title="Urban&Urbane-Shirts Q&A",
    page_icon="👕",
    layout="centered"
)

# ---------- Header ----------
st.markdown(
    """
    <h1 style="text-align:center;">👕Urban&Urbane-Shirts</h1>
    <h2 style="text-align:center;">AI Assistance</h2>
    <p style="text-align:center; color: gray;">
    Ask natural language questions about inventory
    </p>
    """,
    unsafe_allow_html=True
)

st.divider()

# ---------- Sidebar ----------
st.sidebar.header("🧠 Try these examples")
example_questions = [
    "How many red t-shirts?",
    "How many Nike t-shirts are in stock?",
    "Total number of t-shirts",
    "How many black Adidas t-shirts?"
]

for q in example_questions:
    if st.sidebar.button(q):
        st.session_state["question"] = q

st.sidebar.divider()
st.sidebar.caption("Built with Groq + LangChain + MySQL")

# ---------- DB ----------
engine = create_engine(
    "mysql+pymysql://root:2026@localhost/atliq_tshirts"
)

# ---------- LLM ----------
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)

sql_chain = get_few_shot_db_chain(llm)

# ---------- Input ----------
question = st.text_input(
    "Ask about the T-shirts 👇",
    key="question",
    placeholder="e.g. How many red t-shirts?"
)

# ---------- Action ----------
if st.button("🚀 Get Answer") and question:
    with st.spinner("Thinking..."):
        try:
            data, sql = process_question(
                question,
                sql_chain,
                engine,
                return_sql=True
            )

            st.success("✅ Done!")

            # ---------- SQL (Hidden) ----------
            with st.expander("🔍 View Generated SQL"):
                st.code(sql, language="sql")

            # ---------- Result Display ----------
            st.subheader("📊 Result")

            # If COUNT query → show metric
            if (
                isinstance(data, list)
                and len(data) == 1
                and len(data[0]) == 1
            ):
                value = list(data[0].values())[0]
                st.metric(label="Answer", value=value)
            else:
                st.table(data)

        except Exception as e:
            st.error(f"❌ Error: {e}")


    for i, h in enumerate(reversed(st.session_state.history), 1):
        with st.expander(f"{i}. {h['question']}"):
            st.code(h["sql"], language="sql")
            st.write(h["result"])            

# ---------- Footer ----------
st.divider()
st.caption("⚡ Demo-ready AI SQL assistant for AtliQ")
