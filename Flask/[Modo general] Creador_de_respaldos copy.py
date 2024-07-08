from datetime import datetime
import logging, configparser
import phantasm
import logstash, sys
import mariadb

#Logger para logstash
host = 'localhost'
global test_logger
test_logger = logging.getLogger()
test_logger.setLevel(logging.INFO)
handler = logstash.LogstashHandler(host, 5000, version=1)
test_logger.addHandler(handler)


def main():
    extra = {}
    backup = 1

    try:
        conn = mariadb.connect(
            user="auto-backup",
            password="auto-backup",
            host="127.0.0.1",
            port=3306,
            database="auto-backup"

        )

    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

    # Get Cursor
    cur = conn.cursor()

    #Selecciona la cadena perteneciente al hostname del respaldo especificado
    cur.execute("SELECT ip_servidor from metadata where id_backup=?", (backup,))
    hostname = cur.fetchone()[0]

    #Selecciona la cadena perteneciente al username del respaldo especificado
    cur.execute("SELECT user_servidor from metadata where id_backup=?", (backup,))
    username = cur.fetchone()[0]

    #Selecciona la cadena perteneciente al password del respaldo especificado
    cur.execute("SELECT pw_servidor from metadata where id_backup=?", (backup,))
    password = cur.fetchone()[0]

    #Selecciona la cadena perteneciente al puerto del respaldo especificado
    cur.execute("SELECT port from metadata where id_backup=?", (backup,))
    port = cur.fetchone()[0]

    #Selecciona la cadena perteneciente al rash del respaldo especificado
    cur.execute("SELECT rash from metadata where id_backup=?", (backup,))
    rash = cur.fetchone()[0]

    #Selecciona la cantidad de bloques
    cur.execute("SELECT COUNT(*) as cant_bloques from (SELECT * from codigo where id_backup=? group by no_bloque) cant_bloques", (backup,))
    cant_bloques = int(cur.fetchone()[0])

    #Selecciona la cantidad de reintentos
    cur.execute("SELECT reintentos_maximos from metadata where id_backup=?", (backup,))
    reintentos = int(cur.fetchone()[0])

    cur.execute("SELECT name from backup where id_backup=?", (backup,))
    respaldo = cur.fetchone()[0]

    extra = {
        'respaldo':respaldo
    }
    '''Logstash Fin'''

    '''for i in range(reintentos):
        while True:
            try:
                # do stuff
            except:
                continue
            break'''


    #Hace el recorrido por cada uno de los bloques del respaldo especificado
    for i in range(1,cant_bloques+1):
        #Revisa si el código es paralelo
        cur.execute("select paralelo from codigo where id_backup=? and no_bloque=? LIMIT 1;", (backup,i,))
        result = cur.fetchone()
        paralelo = bool(int(result[0]))

        #Selecciona todas las líneas de código de uno de los bloques
        cur.execute("select run_as_sudo, linea from codigo where id_backup=? and no_bloque=? order by no_linea", (backup,i,))
        aux = []
        for run_as_sudo, linea in cur:
            if(bool(run_as_sudo)==True):
                aux.append(rash + linea)
            else: aux.append(linea)
        
        if(paralelo):
            phantasm.parallel_execute(aux, hostname, username, password, port, extra)
        else:
            phantasm.secuential_execute(aux, hostname, username, password, port, extra)
        
        #global test_logger
        #test_logger.critical("Fallo al ejecutar respaldo: ", extra=extra)

    conn.close()

if __name__ == '__main__':
    main()