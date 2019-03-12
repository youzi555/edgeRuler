import sqlite3

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
