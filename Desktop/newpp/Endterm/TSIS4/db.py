import psycopg2
from config import dbhost, dbport, dbname, dbuser, dbpassword


def connect_db():
    conn = psycopg2.connect(
        host=dbhost,
        port=dbport,
        database=dbname,
        user=dbuser,
        password=dbpassword
    )
    return conn

# базвая балица играка
def create_tables():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS players (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL
        )
    """)
    
    # резудьтаты связные с базвой таблицой
    cur.execute("""
        CREATE TABLE IF NOT EXISTS game_sessions (
            id SERIAL PRIMARY KEY,
            player_id INTEGER REFERENCES players(id),
            score INTEGER NOT NULL,
            level_reached INTEGER NOT NULL,
            played_at TIMESTAMP DEFAULT NOW()
        )
    """)
    conn.commit()
    conn.close()
    print("done")

# Добавляем или получаем игрока
def get_player_id(username):
    conn = connect_db()
    cur = conn.cursor()
    
    # Ищем игрока
    cur.execute("SELECT id FROM players WHERE username = %s", (username,))
    player = cur.fetchone()
    
    if player:
        # возвращаем id
        player_id = player[0]
    else:
        # create нового
        cur.execute("INSERT INTO players (username) VALUES (%s) RETURNING id", (username,))
        player_id = cur.fetchone()[0]
        conn.commit()
    
    conn.close()
    return player_id

# Сохраняем результат игры
def save_result(player_id, score, level):
    conn = connect_db()
    cur = conn.cursor()
    
    cur.execute(
        "INSERT INTO game_sessions (player_id, score, level_reached) VALUES (%s, %s, %s)",
        (player_id, score, level)
    )
    conn.commit()
    conn.close()

# top10
def get_top_10():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT p.username, gs.score, gs.level_reached, gs.played_at
        FROM game_sessions gs
        JOIN players p ON gs.player_id = p.id
        ORDER BY gs.score DESC
        LIMIT 10
    """)
    top_10 = cur.fetchall() # get result
    conn.close()
    return top_10

# get record
def get_best_score(player_id):
    conn = connect_db()
    cur = conn.cursor()
    
    cur.execute(
        "SELECT MAX(score) FROM game_sessions WHERE player_id = %s", # find top result by id
        (player_id,)
    )
    
    result = cur.fetchone() # get cortege
    conn.close()
    
    if result[0] is None: # first result cortege also number of top score
        return 0
    return result[0]