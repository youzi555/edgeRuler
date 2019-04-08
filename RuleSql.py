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
    
def selectRules(condition):
    conn = sqlite3.connect('edge.db')
    c = conn.cursor()

    
initial()
FilterSql.initial()
TransformSql.initial()
