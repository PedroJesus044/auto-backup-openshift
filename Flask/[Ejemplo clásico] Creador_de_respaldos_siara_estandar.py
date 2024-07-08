from datetime import datetime
import logging, configparser
import phantasm
TRAINING = True
#Este script sirve para crear respaldos del servidor de forma automática y mandarlos al servidor de respaldos*
backup_prefix = "SIARA"
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
handler = logging.FileHandler('log/'+backup_prefix+'.log', 'a', 'utf-8')
root_logger.addHandler(handler)

#Contraseñas y host
#Esto es leído desde director.ini
srv_data = configparser.ConfigParser()
srv_data.read("director.ini")
hostname = srv_data['siara']['hostname']
username = srv_data['siara']['username']
password = srv_data['siara']['password']
port = srv_data['siara']['port']

#Ruta del respaldo en el NAS
nas_target_folder = srv_data['siara']['nas_path']

nas_hostname = srv_data['trueNAS']['hostname']
nas_username = srv_data['trueNAS']['username']

#Generadores de variables para crear comandos, puede ser diferente en cada servidor

#Run As Sudo Header
#Debes concatenar esta cadena a cada comando que quieras ejecutar como sudo
#Probado en; Centos, Rocky
rash = "echo "+password+" | sudo -S "

#Variables de log
#Se generan solitas, no es necesario cambiar nada
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
#Si lo vas a hacer con la herramienta Phantasm.parallel_execute(), olvídate de poner variables tipo EXPORT o cosas que se
#guarden en el ambiente CLI. Phantasm.parallel_execute() se la pasa ejecutando diferentes shells.
commands = [
    rash + "rsync -a /var/www/html/owncloud resp@10.0.2.12:/mnt/pool1/respaldos/files/",
    rash + "mkdir /tmp/"+bakdir_date+"",
    rash + "mariabackup --backup --target-dir=/tmp/"+bakdir_date+"/mysql --user=backup --password=4dm1n1str4d0r. --host=10.0.2.10",
    rash + "tar -cf /tmp/"+nombre_respaldo+" /tmp/"+bakdir_date,
    rash + "du -sh /tmp/"+nombre_respaldo,
    rash + "rsync -a /tmp/"+nombre_respaldo+" resp@10.0.2.12:/mnt/pool1/respaldos/db/",
    rash + "rm -rf /tmp/"+bakdir_date+"*"
]

if TRAINING==False:
    logging.info("[BEGIN]")

    #Imprimir las variables de log
    logging.info("Ruta respaldo: " + ruta_respaldo)
    logging.info("Nombre respaldo: " + nombre_respaldo)
    logging.info("Fecha: " + fecha)
    logging.info("IP del servidor: " + hostname)
    logging.info("IP del almacenamiento: " + nas_hostname)

    #Ejecutar comandos
    phantasm.secuential_execute(commands, hostname, username, password, port)

    logging.info("[OK]")
else:
    for i in commands:
        print(i)
    print("Ruta respaldo: ", ruta_respaldo)
    print("Nombre respaldo: ", nombre_respaldo)
    print("Fecha: ", fecha)
    print("IP del servidor: ", hostname)
    print("IP del almacenamiento: ", nas_hostname)