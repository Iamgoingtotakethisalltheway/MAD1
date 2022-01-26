import sqlite3
from sqlalchemy import create_engine
from sqlalchemy import text

# engine = create_engine("sqlite+pysqlite:///./play.sqlite3", echo=True, future=True)
engine = create_engine("sqlite:///./play.sqlite3", future=True)

# "commit as you go" style - by default rollsback at the end of the transactional block.
# To commit, specify connection.commit() explicitly at the end of the block.
with engine.connect() as conn:
    result = conn.execute(text("select 'hello world'"))
    print(result.all())
    conn.execute(text("DROP TABLE IF EXISTS some_table"))
    conn.commit()
    conn.execute(text("CREATE TABLE IF NOT EXISTS some_table (x int unique, y int unique)"))
    conn.execute(
        text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
        [{"x": 1, "y": 1}, {"x": 2, "y": 4}]
        )
    conn.commit()

# "begin once" style - by default commits at the end of the transactional block
with engine.begin() as conn:
    conn.execute(
        text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
        [{"x": 6, "y": 8}, {"x": 9, "y": 10}]
    )

# y_dict = {"y": 4}
with engine.connect() as conn:
    result = conn.execute(
        text("SELECT x, y FROM some_table")
        )
    # Can pass dictionaries as arguments to text(). 
    # In the code below, ":y" is the new parameter to which y_dict is bound.
    # result = conn.execute(
    #     text("SELECT x, y FROM some_table WHERE y > :y"),
    #     y_dict
    #     )
    # print(list(result))
    # print(result.all())
    for row in result:
        print(f"x: {row.x} y: {row.y}")