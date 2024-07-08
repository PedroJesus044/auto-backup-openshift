from datetime import datetime
import paramiko, logging, configparser
import executor, phantasm
TRAINING = False
#Este script sirve para crear respaldos del servidor de forma automática y mandarlos al servidor de respaldos*
backup_prefix = "respaldo-siara"
#logging.basicConfig(filename='log/'+backup_prefix+'.log', encoding='utf-8', level=logging.INFO)
#logging.info('[BEGIN]')

#Contraseñas y host
srv_data = configparser.ConfigParser()
srv_data.read("director.ini")
hostname = srv_data['siara']['hostname']
username = srv_data['siara']['username']
password = srv_data['siara']['password']
port= srv_data['siara']['port']

#Ruta del respaldo en el NAS
sftp_target_folder = '/Almacenamiento/Respaldos/OJS/'

#Generadores de variables para crear comandos, puede ser diferente en cada servidor

#Run As Sudo Header
#Debes concatenar esta cadena a cada comando que quieras ejecutar como sudo
rash = "echo GF_92K_Dpp | sudo -S "
bakdir_date = str(str(backup_prefix+"_"+str(datetime.now())).replace(" ", "_")).replace(":", "-")


#Comandos a ejecutar
#Solo pon una lista de comandos, créalos para que se adapten a cada server
#Si lo vas a hacer con la herramienta phantasm (ya sea con parallel_execute o secuential_execute), olvídate de poner variables tipo EXPORT o cosas que se
#guarden en el ambiente CLI. Phantasm se la pasa ejecutando diferentes shells
commands = [
    rash + "rsync -a /var/www/html/owncloud resp@10.0.2.12:/mnt/pool1/respaldos/files/",
    rash + "mkdir /tmp/"+bakdir_date+"",
    rash + "mariabackup --backup --target-dir=/tmp/"+bakdir_date+"/mysql --user=backup --password=4dm1n1str4d0r. --host=10.0.2.10",
    rash + "tar -cf /tmp/"+bakdir_date+".tar.gz /tmp/"+bakdir_date,
    rash + "rsync -a /tmp/"+bakdir_date+".tar.gz resp@10.0.2.12:/mnt/pool1/respaldos/db/",
    rash + "rm -rf /tmp/"+bakdir_date+"*"
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

    #logging.info("[OK]")
    client.close()
else:
    for i in commands:
        print(i)