import psycopg2
from config import DB_con

def connecting():
    return psycopg2.connect(**DB_con)