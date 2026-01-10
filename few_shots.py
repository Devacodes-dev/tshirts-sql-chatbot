# few_shots.py

few_shots = [
    {
        "question": "How many Red T-shirts?",
        "sql": "SELECT COUNT(*) FROM t_shirts WHERE color='Red';"
    },
    {
        "question": "How many Nike T-shirts?",
        "sql": "SELECT COUNT(*) FROM t_shirts WHERE brand='Nike';"
    },
    {
        "question": "List all Black T-shirts in stock",
        "sql": "SELECT * FROM t_shirts WHERE color='Black';"
    },
    {
        "question": "How many T-shirts of size M?",
        "sql": "SELECT COUNT(*) FROM t_shirts WHERE size='M';"
    },
    # You can add more few-shot examples here
]
