import sqlite3

def initial():
    conn = sqlite3.connect('edge.db')
    print("Opened database successful")
    
    try:
        create_rule_cmd = '''CREATE TABLE IF NOT EXISTS filter
            (filterId INT PRIMARY KEY  NOT NULL,
             ruleId INT NOT NULL,
             filterCode VARCHAR (255) NOT NULL,
             FOREIGN KEY (ruleId) REFERENCES rule(ruleId))'''
        conn.execute(create_rule_cmd)
    except:
        print("create table failed")
        return False
    
    conn.commit()
    conn.close()
    
def insertManyFilter(filter_dicts):
    conn = sqlite3.connect('edge.db')
    c = conn.cursor()
    
    sql = '''INSERT INTO filter (filterId, ruleId, filterCode) VALUES (:filterId, :ruleId, :filterCode)'''
    c.executemany(sql, filter_dicts)
    
    conn.commit()
    conn.close()

