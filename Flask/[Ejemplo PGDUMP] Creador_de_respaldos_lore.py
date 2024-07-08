from datetime import datetime
import paramiko, logging, configparser, json
import executor, phantasm
import calendar
TRAINING = True
#Este script sirve para crear respaldos del servidor de forma automática y mandarlos al servidor de respaldos*
backup_prefix = "BIOMETRICOS"
root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('log/'+backup_prefix+'.log', 'w', 'utf-8')
root_logger.addHandler(handler)

#Contraseñas y host
srv_data = configparser.ConfigParser()
srv_data.read("director.ini")
hostname = srv_data['lorena']['hostname']
username = srv_data['lorena']['username']
password = srv_data['lorena']['password']
port = srv_data['lorena']['port']

nas_hostname = srv_data['trueNAS']['hostname']
nas_username = srv_data['trueNAS']['username']

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
ruta_respaldo = nas_hostname+nas_target_folder+"/"+(str(hostname).replace('.', '_'))
nombre_respaldo = bakdir_date+".tar.gz"
fecha = current_datetime.strftime("%d/%m/%Y")

#Comandos a ejecutar
#Solo pon una lista de comandos, créalos para que se adapten a cada server
#Si lo vas a hacer con la herramienta phantasm (ya sea con parallel_execute o secuential_execute), olvídate de poner variables tipo EXPORT o cosas que se
#guarden en el ambiente CLI. Phantasm se la pasa ejecutando diferentes shells
commands = [
    "cd /tmp/",
    rash + "docker exec -t bd-postgres pg_dump -U biometricos > biometricos.sql",
    rash + "tar -czvf "+bakdir_date+".tar.gz /tmp/biometricos.sql",
    rash + "rsync -a --rsync-path='mkdir -p "+nas_target_folder+"/$(date '+%Y')/$(date '+%B') && rsync' "+bakdir_date+".tar.gz backups@10.22.157.67:"+nas_target_folder+"/$(date '+%Y')/$(date '+%B')",
    rash + "du -sh "+bakdir_date+".tar.gz",
    rash + "rm -rf "+bakdir_date+".tar.gz"
]

if TRAINING==False:
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

    logging.info("[OK]")
    client.close()
    #phantasm.secuential_execute(commands, hostname, username, password, port)
else:
    for i in commands:
        print(i)


    print("Ruta respaldo: ", ruta_respaldo)
    print("Nombre respaldo: ", nombre_respaldo)
    print("Fecha: ", fecha)
    print("IP del servidor: ", hostname)
    print("IP del almacenamiento: ", nas_hostname)