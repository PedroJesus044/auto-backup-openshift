import logging, paramiko, re, mariadb, os
#Se encarga de ejecutar comandos en un servidor remoto por SSH.
#Requiere un cliente de SSH hecho con el módulo Paramiko de Python

#Ejecuta un arreglo de varios comandos, por ejemplo:
#commands = ['mkdir /any_dir', 'touch /anydir/anyfile' ,'rm -rf /any_dir']

import logging
logger = logging.getLogger(__name__)

#Esto decodificará la bytestring por fuerza bruta
def force_decode(string, codecs=['utf8', 'ascii', 'cp1252']):
    for i in codecs:
        try:
            return string.decode(i)
        except UnicodeDecodeError:
            pass

    logging.warn("cannot decode url %s" % ([string]))

#Esto nos ayudará a saber qué funciones se ejecutaron y así recibir una salida
def function_handler(command, out, extra):
    #Se crean conexiones justo para esto
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

    cur = conn.cursor()


    #En caso de que se haya ejecutado un du -s
    logger.info("Salida: " + out)
    if(re.match(r"du -s .*", command)):
                    
                    out = out.replace("\t", ' ')
                    size = re.search('[0-9]+', out)
                    file = re.sub(r"([0-9]+ )", "", out)
                    if(size and file):
                        size = int(size.group())
                        #file = file.group()
                        
                        #print(size, file)
                        
                        extra.update({'archivo':file})
                        extra.update({'peso':int(size)}) 
                    logger.info("Se ejecuta un [du -s], enviando a la DB, Peso: "+str(size)+" Archivo: "+file)
                    query = "INSERT INTO file_traces (id_backup, size, file) VALUES ("+ str(extra["id_backup"]) +", "+ str(extra["peso"]) +", '"+ str(extra["archivo"]) +"')"
                    cur.execute(query)
                    logger.info(out, extra=extra)

    #En caso de ejecutar un dir /s /-c *        
    if(re.match(r"dir \/s \/-c .*", command)):
        out = out.replace("\t", ' ')
        focus = re.search(r"[0-9]+ [^\s]+\.[^\s]+", out).group()
        size = int(int(focus.split(" ")[0])/1024)
        file = focus.split(" ")[1]
        if(size and file):
            size = int(size)            
            extra.update({'archivo':file})
            extra.update({'peso':size})

            logger.info("Se ejecuta un [dir \/s \/-c], enviando a la DB, Peso: "+str(size)+" Archivo: "+file)
            query = "INSERT INTO file_traces (id_backup, size, file) VALUES ("+ str(extra["id_backup"]) +", "+ str(extra["peso"]) +", '"+ str(extra["archivo"]) +"')"
            cur.execute(query)
            logger.info(out, extra=extra)

    conn.commit()
    conn.close()


def execute(client, commands, extra):
    status = 0
    try:
        for command in commands:
            logger.info("Ejecutando: "+command, extra=extra)
            
            stdin, stdout, stderr = client.exec_command(command, get_pty=False)
            stdin.close()
            
            #Creamos la función force_decode porque en windows, la decodificación es diferente
            out = force_decode(stdout.read()).rstrip()
            if out:
                function_handler(command, out, extra)
            logger.debug(out, extra=extra)
            if(stdout.channel.recv_exit_status()!=0):
                err = force_decode(stderr.read())
                out = force_decode(stdout.read())
                if out:
                    logger.info(out, extra=extra)
                if err:
                    logger.error("Proceso terminado con errores: " + str(stdout.channel.recv_exit_status()), extra=extra)
                    logger.error("Error: "+err, extra=extra)
                    status = 1
                    raise Exception("Falla en execute, el comando regresó errores")
        return status
    except Exception as e:
        logger.critical("Fallo al ejecutar execute "+ repr(e), extra=extra)
        raise Exception('Fallo al ejecutar execute - ' + repr(e))

#Ejecuta un solo comando, por ejemplo:
#command = 'touch anyfile'
def execute_single(client, command, extra):
    status = 0
    try:
        logger.info("Ejecutando: "+command, extra=extra)
        stdin, stdout, stderr = client.exec_command(command, get_pty=False)
        stdin.close()
        out = force_decode(stdout.read()).rstrip()
        if out:
            function_handler(command, out, extra)
        logger.debug(out, extra=extra)
        if(stdout.channel.recv_exit_status()!=0):
            err = force_decode(stderr.read())
            if err:
                logger.error("Proceso terminado con errores: " + str(stdout.channel.recv_exit_status()), extra=extra)
                logger.error("Error: "+err, extra=extra)
                status = 1
                raise Exception("Falla en execute_single, el comando regresó errores")
        return status
    except Exception as e:
        logger.critical("Fallo al ejecutar execute_single - ", extra=extra)
        raise Exception('Fallo al ejecutar execute_single - ' + repr(e))

def execute_dedicated(command, hostname, username, password, port, extra):
    #Hazte un cliente paramiko nuevo, a fuerzas
    #Tiene que ser nuevo
    #Nuevo!!!!
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=hostname, username=username, password=password, port=port)

        #logging.info("Ejecutando los comandos por SSH...")
        execute_single(client, command, extra)

        #logging.info("[OK]")
        client.close()
    except Exception as e:
        logger.critical("[!] Cannot connect to the SSH Server", extra=extra)
        raise Exception('Fallo al ejecutar execute_dedicated - ' + repr(e))