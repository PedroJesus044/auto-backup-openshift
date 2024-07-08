from datetime import datetime
import logging, configparser
import phantasm
import logstash, sys

def main():
    TRAINING = True
    #Este script sirve para crear respaldos del servidor de forma automática y mandarlos al servidor de respaldos*
    backup_prefix = "respaldo-siara"
    logging.basicConfig(level=logging.INFO, filename='log/'+backup_prefix+'.log',filemode="a", format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')



    '''Logstash Inicio'''
    host = 'localhost'
    
    global test_logger
    test_logger = logging.getLogger()

    test_logger.setLevel(logging.INFO)
    handler = logstash.LogstashHandler(host, 5000, version=1)
    #handler.setFormatter(logging.Formatter)
    test_logger.addHandler(handler)
    extra = {
        'respaldo':"Siara - Paralelo"
    }
    '''Logstash Fin'''




    #Contraseñas y host
    srv_data = configparser.ConfigParser()
    srv_data.read("director.ini")
    hostname = srv_data['siara']['hostname']
    username = srv_data['siara']['username']
    password = srv_data['siara']['password']
    port = srv_data['siara']['port']

    nas_hostname = srv_data['trueNAS']['hostname']
    nas_username = srv_data['trueNAS']['username']

    #Ruta del respaldo en el NAS
    nas_target_folder = srv_data['siara']['nas_path']

    #Generadores de variables para crear comandos, puede ser diferente en cada servidor

    #Run As Sudo Header
    #Debes concatenar esta cadena a cada comando que quieras ejecutar como sudo
    rash = "echo GF_92K_Dpp | sudo -S "
    bakdir_date = str(str(backup_prefix+"_"+str(datetime.now())).replace(" ", "_")).replace(":", "-")

    #Variables de log
    #Aquí puedes generar información importante para guardar en los logs
    #Puedes usarlas en la generación de comandos
    current_datetime = datetime.now()
    current_date_time = current_datetime.strftime("%d%m%Y")
    bakdir_date = str(str(backup_prefix+"_"+str(current_date_time)).replace(" ", "_")).replace(":", "-")
    ruta_respaldo = nas_target_folder+"/"+(str(hostname).replace('.', '_'))
    nombre_respaldo = bakdir_date+".tar.gz"
    fecha = current_datetime.strftime("%d/%m/%Y")

    #Comandos a ejecutar
    #Solo pon una lista de comandos, créalos para que se adapten a cada server
    #Si lo vas a hacer con la herramienta phantasm (ya sea con parallel_execute o secuential_execute), olvídate de poner variables tipo EXPORT o cosas que se
    #guarden en el ambiente CLI. Phantasm se la pasa ejecutando diferentes shells
    preparacion = [
        rash + "mkdir /tmp/"+bakdir_date
    ]

    bloque_paralelo=[
        rash + "rsync -a /var/www/html/owncloud resp@10.0.2.12:"+nas_target_folder+"files/",
        rash + "mariabackup --backup --target-dir=/tmp/"+bakdir_date+"/mysql --user=backup --password=4dm1n1str4d0r. --host=10.0.2.10"
    ]

    bloque_final = [
        rash + "tar -cf /tmp/"+nombre_respaldo+" /tmp/"+bakdir_date,
        rash + "rsync -a /tmp/"+nombre_respaldo+" resp@10.0.2.12:"+nas_target_folder,
        rash + "rm -rf /tmp/"+bakdir_date+"*"
    ]

    if TRAINING==False:
        test_logger.info("[BEGIN]")

        #Imprimir las variables de log
        test_logger.info("Ruta respaldo: " + ruta_respaldo, extra = extra)
        test_logger.info("Nombre respaldo: " + nombre_respaldo, extra = extra)
        test_logger.info("Fecha: " + fecha, extra = extra)
        test_logger.info("IP del servidor: " + hostname, extra = extra)
        test_logger.info("IP del almacenamiento: " + nas_hostname, extra = extra)

        try:
            phantasm.secuential_execute(preparacion, hostname, username, password, port)
            phantasm.parallel_execute(bloque_paralelo, hostname, username, password, port)
            phantasm.secuential_execute(bloque_final, hostname, username, password, port)
        except Exception as e:
            test_logger.critical("Fallo al ejecutar respaldo " + repr(e), extra=extra)

        test_logger.info("[END]")
    else:
        test_logger.info("Ruta respaldo: " + ruta_respaldo, extra = extra)
        test_logger.info("Nombre respaldo: " + nombre_respaldo, extra = extra)
        test_logger.info("Fecha: " + fecha, extra = extra)
        test_logger.info("IP del servidor: " + hostname, extra = extra)
        test_logger.info("IP del almacenamiento: " + nas_hostname, extra = extra)

        bloque_secuencial = preparacion + bloque_paralelo + bloque_final
        for i in bloque_secuencial: print(i)

if __name__ == '__main__':
    main()