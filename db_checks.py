def initVelibTable(conn):
    """
    Delete all rows in the data in table
    """
    try:
        sql = 'DROP TABLE IF EXISTS velib;'
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()    
    except:
        sql = 'CREATE TABLE velib'
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()