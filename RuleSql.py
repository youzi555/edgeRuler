import sqlite3
import FilterSql
import TransformSql

def initial():
    conn = sqlite3.connect('edge.db')
    print("Opened database successful")
    
    try:
        create_rule_cmd ='''CREATE TABLE IF NOT EXISTS rule
            (ruleId INT PRIMARY KEY  NOT NULL,
             state VARCHAR(10) NOT NULL,
             shortAddress VARCHAR (4) NOT NULL,
             Endpoint VARCHAR (2) NOT NULL);'''
        conn.execute(create_rule_cmd)
    except:
        print("create table failed")
        return False
    
    conn.commit()
    conn.close()
    
def insertRule(rule_dict):
    conn = sqlite3.connect('edge.db')
    c = conn.cursor()
    
    sql = '''INSERT INTO rule (ruleId, state, shortAddress, Endpoint) VALUES (:ruleId, :state, :shortAddress, :Endpoint)'''
    c.execute(sql, rule_dict)
    
    conn.commit()
    conn.close()
    
def selectAllRules():
    conn = sqlite3.connect('edge.db')
    conn.row_factory = dict_factory
    c = conn.cursor()
    
    c.execute('SELECT * FROM rule')
    
    res = c.fetchall()
    return res
    
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


initial()
FilterSql.initial()
TransformSql.initial()
