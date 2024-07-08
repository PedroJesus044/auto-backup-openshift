from datetime import datetime
import paramiko, logging, configparser, json
import executor, phantasm
TRAINING = True
#Este script sirve para crear respaldos del servidor de forma automática y mandarlos al servidor de respaldos*
backup_prefix = "GESTION"
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
handler = logging.FileHandler('log/'+backup_prefix+'.log', 'a', 'utf-8')
root_logger.addHandler(handler)

#Contraseñas y host
srv_data = configparser.ConfigParser()
srv_data.read("director.ini")
hostname = srv_data['lorena']['hostname']
username = srv_data['lorena']['username']
password = srv_data['lorena']['password']
port = srv_data['lorena']['port']

nas_hostname = srv_data['nas_gestion']['hostname']
nas_username = srv_data['nas_gestion']['username']

#Ruta del respaldo en el NAS
nas_target_folder = '/mnt/Respaldos_Pure/Test'

#Generadores de variables para crear comandos, puede ser diferente en cada servidor

#Run As Sudo Header
#Debes concatenar esta cadena a cada comando que quieras ejecutar como sudo
rash = "echo "+password+" | sudo -S "

current_datetime = datetime.now()
current_date_time = current_datetime.strftime("%d%m%Y")
bakdir_date = str(str(backup_prefix+"_"+str(current_date_time)).replace(" ", "_")).replace(":", "-")

#Variables de log
#Aquí puedes generar información importante para guardar en los logs
#Puedes usarlas en la generación de comandos
ruta_respaldo = nas_target_folder+"/"+(str(hostname).replace('.', '_'))
nombre_respaldo = bakdir_date+".tar.gz"
fecha = current_datetime.strftime("%d/%m/%Y")

#Comandos a ejecutar
#Solo pon una lista de comandos, créalos para que se adapten a cada server
#Si lo vas a hacer con la herramienta phantasm (ya sea con parallel_execute o secuential_execute), olvídate de poner variables tipo EXPORT o cosas que se
#guarden en el ambiente CLI. Phantasm se la pasa ejecutando diferentes shells
commands = [
    rash + "docker exec GestionTemporal mkdir -p /var/log/mysql/respaldo/mysql",
    rash + "docker exec GestionTemporal mariabackup --backup --user=root --password=Acceso123 --target-dir=/var/log/mysql/respaldo/mysql",
    rash + "tar -cvf "+nombre_respaldo+" /home/shernandez/Gestion01042023/logs/",
    rash + "du -sh "+nombre_respaldo,
    rash + "rsync -a --rsync-path='mkdir -p "+ruta_respaldo+"/$(date '+%Y')/$(date '+%B') && rsync' "+nombre_respaldo+" backups@10.22.157.67:"+ruta_respaldo+"/$(date '+%Y')/$(date '+%B')",
    rash + "rm -rf "+nombre_respaldo,
    rash + "rm -rf /home/shernandez/Gestion01042023/logs/respaldo"
]

if TRAINING==False:
    #Imprimir las variables de log
    logging.info('[BEGIN]')
    logging.info("Ruta respaldo: " + ruta_respaldo)
    logging.info("Nombre respaldo: " + nombre_respaldo)
    logging.info("Fecha: " + fecha)
    logging.info("IP del servidor: " + hostname)
    logging.info("IP del almacenamiento: " + nas_hostname)

    #Abrir el cliente del servidor a respaldar
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=hostname, username=username, password=password, port=port)
    except:
        print("[!] Cannot connect to the SSH Server")
        exit()

    #logging.info("Ejecutando los comandos por SSH...")
    executor.execute(client, commands)
    client.close()

    logging.info("[OK]")
else:
    print("Ruta respaldo: ", ruta_respaldo)
    print("Nombre respaldo: ", nombre_respaldo)
    print("Fecha: ", fecha)
    print("IP del servidor: ", hostname)
    print("IP del almacenamiento: ", nas_hostname)
    for i in commands:
        print(i)