import psycopg2
import pandas as pd

db_url = 'postgresql+psycopg2://mauroassis:Hibisco@12@127.0.0.1:5432/medica'


def connectDB():
    return psycopg2.connect(
        database="medica", user='mauroassis', password='Hibisco@12', host='127.0.0.1', port='5432'
    )


def executeSQL(sql):
    conn = connectDB()
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as e:
        raise e


def getValueFromDb(sql):
    rows = executeSQL(sql)
    for row in rows:
        return row[0]
    return None

def getDictResultset(sql):
    return {row[0]: row[1] for row in executeSQL(sql)}


def getJSONResultset(sql):
    return executeSQL(sql).first()[0]


def getDataframeResultSet(sql):
    return pd.read_sql(sql, connectDB())
