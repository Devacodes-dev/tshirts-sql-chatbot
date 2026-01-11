# main.py

import streamlit as st
from sqlalchemy import create_engine
from langchain_groq import ChatGroq
from langchain_helper import get_few_shot_db_chain, process_question
import os
import base64
import pandas as pd


# ---------- Background ----------
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
           background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


# ---------- Session ----------
if "history" not in st.session_state:
    st.session_state.history = []

set_bg("bg1.jpg")

st.markdown("""
<style>

/* Tabs container */
.stTabs [data-baseweb="tab-list"] {
    gap: 12px;
    padding: 0.5rem 0;
}

/* Each tab */
.stTabs [data-baseweb="tab"] {
    height: 44px;
    padding: 0 22px;
    background: rgba(255, 255, 255, 0.08);
    border-radius: 999px;
    color: #ddd;
    font-weight: 600;
    border: 1px solid rgba(255,255,255,0.15);
    transition: all 0.25s ease-in-out;
}

/* Hover effect */
.stTabs [data-baseweb="tab"]:hover {
    background: rgba(255,255,255,0.18);
    color: white;
}

/* Active tab */
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #c8ad7f, #e6d3b3);
    color: black !important;
    box-shadow: 0 6px 18px rgba(255,77,77,0.45);
}

/* Remove underline */
.stTabs [data-baseweb="tab-highlight"] {
    display: none;
}

</style>
""", unsafe_allow_html=True)



st.set_page_config(
    page_title="Urban&Urbane-Shirts Q&A",
    page_icon="👕",
    layout="centered"
)

# ---------- Header ----------
st.markdown(
    """
    <h1 style="text-align:center;">👕 Urban&Urbane-Shirts</h1>
    <h3 style="text-align:center;">AI Inventory Assistant</h3>
    <p style="text-align:center; color: gray;">
    Ask natural language questions about our t-shirts
    </p>
    """,
    unsafe_allow_html=True
)

st.divider()

# ---------- Sidebar ----------
st.sidebar.header("🧠 Try these")
example_questions = [
    "How many red t-shirts?",
    "what is the average price of tshirts?",
    "Total number of t-shirts",
    "Show t-shirt count by brand"
]

for q in example_questions:
    if st.sidebar.button(q):
        st.session_state["question"] = q

st.sidebar.divider()
st.sidebar.caption("Groq • LangChain • MySQL")

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

# ---------- Tabs ----------
tab1, tab2, tab3, tab4 = st.tabs(
    ["🔎 Ask Question", "📊 Visual Insights", "🕘 History", "⚙️ SQL Debug"]
)

# ---------- ASK QUESTION ----------
with tab1:
    question = st.text_input(
        "Ask about the T-shirts 👇",
        key="question",
        placeholder="e.g. How many black Adidas t-shirts?"
    )

    if st.button("🚀 Get Answer") and question:
        with st.spinner("🧠 Analyzing inventory..."):
            try:
                data, sql = process_question(
                    question,
                    sql_chain,
                    engine,
                    return_sql=True
                )

                st.session_state["last_sql"] = sql
                st.session_state["last_data"] = data

                st.success("✅ Done!")

                # ----- Natural Language Answer -----
                if isinstance(data, list) and len(data) == 1 and len(data[0]) == 1:
                    value = list(data[0].values())[0]
                    st.markdown(
                        f"🗣️ There are **{value} t-shirts** matching your query."
                    )
                else:
                    st.dataframe(data, use_container_width=True)

                # Save history
                st.session_state.history.append({
                    "question": question,
                    "sql": sql,
                    "result": data
                })

            except Exception as e:
                st.error(f"❌ Error: {e}")

# ---------- VISUAL INSIGHTS ----------
with tab2:
    if "last_data" in st.session_state:
        df = pd.DataFrame(st.session_state["last_data"])

        if df.shape[1] == 2:
            st.subheader("📊 Visual Insight")
            st.bar_chart(df.set_index(df.columns[0]))
        else:
            st.info("📌 Charts appear when data has categories + values")
    else:
        st.info("Ask a question first to see charts")

# ---------- HISTORY ----------
with tab3:
    if st.session_state.history:
        for i, h in enumerate(reversed(st.session_state.history), 1):
            with st.expander(f"{i}. {h['question']}"):
                st.code(h["sql"], language="sql")
                st.write(h["result"])
    else:
        st.info("No history yet")

# ---------- SQL DEBUG ----------
with tab4:
    if "last_sql" in st.session_state:
        st.code(st.session_state["last_sql"], language="sql")
    else:
        st.info("Run a query to see SQL here")
