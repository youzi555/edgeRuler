import sqlite3


def initial():
    conn = sqlite3.connect('edge.db')
    print("Opened database successful")
    
    try:
        create_rule_cmd = '''CREATE TABLE IF NOT EXISTS transform
            (transformId INT PRIMARY KEY  NOT NULL,
             ruleId INT NOT NULL,
             name VARCHAR (31) NOT NULL,
             url VARCHAR (255) DEFAULT NULL,
             method VARCHAR (31) DEFAULT NULL ,
             body VARCHAR (255) NOT NULL ,
             FOREIGN KEY (ruleId) REFERENCES rule(ruleId))'''
        conn.execute(create_rule_cmd)
    except:
        print("create table failed")
        return False
    
    conn.commit()
    conn.close()

def insertManyTransform(transform_dicts):
    conn = sqlite3.connect('edge.db')
    c = conn.cursor()
    
    sql = '''INSERT INTO transform (transformId, ruleId, name, url, method, body) VALUES (:transformId, :ruleId, :name, :url, :method, :body )'''
    c.executemany(sql, transform_dicts)
    
    conn.commit()
    conn.close()


def selectTransforms(ruleId):
    conn = sqlite3.connect('edge.db')
    conn.row_factory = dict_factory
    c = conn.cursor()
    
    c.execute('SELECT * FROM transform WHERE ruleId =?', (ruleId, ))
   
    res = c.fetchall()
    return res

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d