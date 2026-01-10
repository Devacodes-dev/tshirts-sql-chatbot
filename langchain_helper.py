from langchain_groq import ChatGroq
from sqlalchemy import text
from few_shots import few_shots

def get_few_shot_db_chain(llm: ChatGroq):
    """
    Returns a function that takes a question and returns SQL using few-shot examples and the LLM.
    """
    def run(question):
        prompt = "You are an AI that converts natural language to SQL for the t_shirts table.\n\n"
        for fs in few_shots:
            prompt += f"Q: {fs['question']}\nSQL: {fs['sql']}\n\n"
        prompt += f"Q: {question}\nSQL:"

        # Use the .invoke() method
        response = llm.invoke(prompt)
        sql_query = response.text.strip().split("\n")[0]
        return sql_query

    return run


def process_question(question, sql_chain, engine, return_sql=False):
    """
    Generates SQL from question and executes it
    """
    raw_sql = sql_chain(question)
    with engine.connect() as conn:
        result = conn.execute(text(raw_sql))
        # Fix: use row._mapping to convert each row to dict safely
        data = [dict(row._mapping) for row in result]
    if return_sql:
        return data, raw_sql
    return data
