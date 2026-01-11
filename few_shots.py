few_shots = [

    # ---------- BASIC COUNTS ----------
    {
        "question": "How many red t-shirts are there?",
        "sql": "SELECT COUNT(*) FROM t_shirts WHERE color = 'Red';"
    },

    {
        "question": "How many Nike t-shirts?",
        "sql": "SELECT COUNT(*) FROM t_shirts WHERE brand = 'Nike';"
    },

    # ---------- AGGREGATES ----------
    {
        "question": "What is the average price of t-shirts?",
        "sql": "SELECT AVG(price) FROM t_shirts;"
    },

    {
        "question": "What is the cheapest t-shirt?",
        "sql": "SELECT MIN(price) FROM t_shirts;"
    },

    # ---------- GROUPING ----------
    {
        "question": "How many t-shirts per brand?",
        "sql": "SELECT brand, COUNT(*) FROM t_shirts GROUP BY brand;"
    },

    # ---------- DISCOUNTS (IMPORTANT) ----------
    {
        "question": "What is the price of discounted t-shirts?",
        "sql": """
        SELECT 
            t.brand,
            t.color,
            t.price,
            d.pct_discount,
            (t.price - (t.price * d.pct_discount / 100)) AS discounted_price
        FROM t_shirts t
        JOIN discounts d ON t.t_shirt_id = d.t_shirt_id;
        """
    },

    {
        "question": "Show discounted t-shirts",
        "sql": """
        SELECT 
            t.brand,
            t.color,
            t.price,
            d.pct_discount
        FROM t_shirts t
        JOIN discounts d ON t.t_shirt_id = d.t_shirt_id;
        """
    },

    {
        "question": "Which t-shirts have discounts?",
        "sql": """
        SELECT 
            t.brand,
            t.color,
            d.pct_discount
        FROM t_shirts t
        JOIN discounts d ON t.t_shirt_id = d.t_shirt_id;
        """
    },

    # ---------- SORTING ----------
    {
        "question": "Top 5 cheapest t-shirts",
        "sql": "SELECT brand, price FROM t_shirts ORDER BY price ASC LIMIT 5;"
    },

]
