import psycopg2
import numpy as np
import time
from . import neostring

def inject_pgsql(df, data):
    # temp_db = database / datas = table
    conn = psycopg2.connect(host='pgsql', dbname="postgres", user="postgres", password="postgres")
    cur = conn.cursor()
    # Création de table
    tablename = neostring.random(50)
    measurer = np.vectorize(len)
    res1 = dict(zip(df, measurer(df.values.astype(str)).max(axis=0)))

    table_creation = "CREATE TABLE "+tablename+" ("
    for column in data['schema']['fields'][1:]:
        table_creation += column['name']+" VARCHAR("+str(res1[column['name']])+"), " # TODO: Remplacer 100 par la string la plus longue du flux de données
    table_creation = table_creation[:-2]
    table_creation += ", wtf VARCHAR(100));"
    cur.execute(""+table_creation+"")
    # Insertion de valeurs
    start_time = time.time()
    for key in data['data']:
        key.pop('level_0', None)
        data_injection = "INSERT INTO "+tablename+" VALUES ("
        for pair in key.items():
            data_injection += "'"+str(pair[1])+"', "
        data_injection = data_injection[:-2]+");"
        cur.execute(data_injection)
    cur.close()
    conn.commit()
    return (time.time() - start_time)