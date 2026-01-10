from sqlalchemy import create_engine, text

engine = create_engine(
    "mysql+pymysql://root:2026@localhost/atliq_tshirts"
)

with engine.connect() as conn:
    result = conn.execute(text("SELECT COUNT(*) FROM t_shirts"))
    print(result.fetchone())
