from datetime import datetime
import logging, configparser
import phantasm
import logstash, sys, os
import mariadb

#Logger para logstash
host = 'localhost'
global test_logger
test_logger = logging.getLogger()
test_logger.setLevel(logging.INFO)

log_to_logstash = False
TRAINING = False
if(log_to_logstash):
    handler = logstash.LogstashHandler(host, 5000, version=1)
    test_logger.addHandler(handler)
else:
    handler = logging.FileHandler('log/log_general.log', 'a', 'utf-32')
    test_logger.setLevel(logging.DEBUG)
    test_logger.addHandler(handler)

def main(backup):
    backup_finished = False
    extra = {}
    try:
        conn = mariadb.connect(
            user=os.environ['ABKP_DB_USER'],
            password=os.environ['ABKP_DB_PASS'],
            host=os.environ['ABKP_DB_HOST'],
            port=3306,
            database=os.environ['ABKP_DB_NAME']
        )

    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        return ('Error connecting to MariaDB Platform:')

    # Get Cursor
    cur = conn.cursor()

    #Selecciona la cadena perteneciente al hostname del respaldo especificado
    cur.execute("SELECT ip_servidor from metadatas where id_backup=?", (backup,))
    hostname = cur.fetchone()[0]

    #Selecciona la cadena perteneciente al username del respaldo especificado
    cur.execute("SELECT user_servidor from metadatas where id_backup=?", (backup,))
    username = cur.fetchone()[0]

    #Selecciona la cadena perteneciente al password del respaldo especificado
    cur.execute("SELECT pw_servidor from metadatas where id_backup=?", (backup,))
    password = cur.fetchone()[0]

    #Selecciona la cadena perteneciente al puerto del respaldo especificado
    cur.execute("SELECT port from metadatas where id_backup=?", (backup,))
    port = cur.fetchone()[0]

    #Selecciona la cadena perteneciente al rash del respaldo especificado
    cur.execute("SELECT rash from metadatas where id_backup=?", (backup,))
    rash = cur.fetchone()[0]

    '''#Selecciona la cantidad de bloques
    cur.execute("SELECT COUNT(*) as cant_bloques from (SELECT * from codigos where id_backup=? group by no_bloque) cant_bloques", (backup,))
    cant_bloques = int(cur.fetchone()[0])'''

    #No seleccionaremos la cantidad de bloques, en vez de eso seleccionaremos los distintos no_bloques
    cur.execute("SELECT DISTINCT no_bloque as block_array from codigos where id_backup=? ORDER BY block_array", (backup,))
    array_bloques = cur.fetchall()
    global test_logger

    #Selecciona la cantidad de reintentos
    cur.execute("SELECT reintentos_maximos from metadatas where id_backup=?", (backup,))
    reintentos = int(cur.fetchone()[0])

    cur.execute("SELECT name from backups where id=?", (backup,))
    respaldo = cur.fetchone()[0]

    extra = {
        'id_backup': backup,
        'respaldo':respaldo
    }
    '''Logstash Fin'''

    global errores
    errores = False
    for i in range(0,reintentos):
        query = "INSERT INTO backup_traces (id_backup, last_status) values (" + backup + ", '[RUNNING]')"
        cur.execute(query)
        conn.commit()
        try:
            #Arreglo de comandos final
            command_book = []

            #Hace el recorrido por cada uno de los bloques del respaldo especificado
            if(len(array_bloques)<1):
                raise Exception("No se encontró código a ejecutar")
            for i in array_bloques:
                test_logger.info(i[0])
                #Revisa si el código es paralelo
                cur.execute("select paralelo from codigos where id_backup=? and no_bloque=? LIMIT 1;", (backup,i[0],))
                result = cur.fetchone()
                paralelo = bool(int(result[0]))

                #Selecciona todas las líneas de código de uno de los bloques
                cur.execute("select run_as_sudo, linea from codigos where id_backup=? and no_bloque=? order by no_linea", (backup,i[0],))
                aux = []
                for run_as_sudo, linea in cur:
                    if(run_as_sudo==1):
                        aux.append(rash + linea)
                    else:
                        aux.append(linea)
                
                if(TRAINING == False):
                    if(paralelo):
                        if(phantasm.parallel_execute(aux, hostname, username, password, port, extra)!=0):
                            errores = True
                    else:
                        if(phantasm.secuential_execute(aux, hostname, username, password, port, extra)!=0):
                            errores = True
                else:
                    command_book.append(aux)
            if(TRAINING == False and errores == False):
                query = "INSERT INTO backup_traces (id_backup, last_status) values (" + backup + ", '[ALL OK]')"
                cur.execute(query)
                conn.commit()
                conn.close()
                return ('[ALL OK]')
            elif(TRAINING == False and errores == True):
                query = "INSERT INTO backup_traces (id_backup, last_status) values (" + backup + ", '[FINISHED WITH ERRORS]')"
                cur.execute(query)
                conn.commit()
                conn.close()
                return ('[FINISHED WITH ERRORS]')
            else:
                query = ""
                cur.execute(query)
                conn.commit()
                conn.close()
                return(command_book)
        except:
            #global test_logger
            test_logger.critical("Fallo al ejecutar respaldo: ", extra=extra)
            continue
    query = "INSERT INTO backup_traces (id_backup, last_status) values (" + backup + ", '[NOT OK]')"
    cur.execute(query)
    conn.commit()
    conn.close()
    return ('[NOT OK]')
    


if __name__ == '__main__':
    main(1)