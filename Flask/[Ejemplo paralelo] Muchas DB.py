from datetime import datetime
import logging, configparser
import phantasm
TRAINING = False
#Este script sirve para crear respaldos del servidor de forma automática y mandarlos al servidor de respaldos*
backup_prefix = "respaldo-paralelo"
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
handler = logging.FileHandler('log/'+backup_prefix+'.log', 'a', 'utf-8')
root_logger.addHandler(handler)

#Contraseñas y host
srv_data = configparser.ConfigParser()
srv_data.read("director.ini")
hostname = srv_data['prueba_paralela_db']['hostname']
username = srv_data['prueba_paralela_db']['username']
password = srv_data['prueba_paralela_db']['password']
port = srv_data['prueba_paralela_db']['port']

nas_hostname = srv_data['nas_gestion']['hostname']
nas_username = srv_data['nas_gestion']['username']

#Ruta del respaldo en el NAS
nas_target_folder = srv_data['prueba_paralela_db']['nas_path']

#Generadores de variables para crear comandos, puede ser diferente en cada servidor

#Run As Sudo Header
#Debes concatenar esta cadena a cada comando que quieras ejecutar como sudo
rash = "echo '" + password + "' | sudo -S "
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
    rash + "mkdir -p "+ruta_respaldo+"/$(date '+%Y')/$(date '+%B')",
    rash + "chmod -R 777 " + ruta_respaldo+"/$(date '+%Y')/$(date '+%B')"
]

bloque_mysqldump=[
    rash + "mysqldump -x -upjem_backup -pmPj7Bg7DhF  --routines --triggers --databases --add-drop-table --create-options --flush-logs htsj_administrativo > "+ruta_respaldo+"/$(date '+%Y')/$(date '+%B')/htsj_administrativo.sql",
    rash + "mysqldump -x -upjem_backup -pmPj7Bg7DhF  --routines --triggers --databases --add-drop-table --create-options --flush-logs htsj_gestion > "+ruta_respaldo+"/$(date '+%Y')/$(date '+%B')/htsj_gestion.sql",
    rash + "mysqldump -x -upjem_backup -pmPj7Bg7DhF  --routines --triggers --databases --add-drop-table --create-options --flush-logs htsj_peritos > "+ruta_respaldo+"/$(date '+%Y')/$(date '+%B')/htsj_peritos.sql",
    rash + "mysqldump -x -upjem_backup -pmPj7Bg7DhF  --routines --triggers --databases --add-drop-table --create-options --flush-logs htsj_laboral > "+ruta_respaldo+"/$(date '+%Y')/$(date '+%B')/htsj_laboral.sql"
]

bloque_final = [
    rash + "du -h "+ruta_respaldo+"/$(date '+%Y')/$(date '+%B')/htsj_administrativo.sql",
    rash + "du -h "+ruta_respaldo+"/$(date '+%Y')/$(date '+%B')/htsj_peritos.sql",
    rash + "du -h "+ruta_respaldo+"/$(date '+%Y')/$(date '+%B')/htsj_gestion.sql",
    rash + "du -h "+ruta_respaldo+"/$(date '+%Y')/$(date '+%B')/htsj_laboral.sql",
    rash + "tar -cf "+ruta_respaldo+"/$(date '+%Y')/$(date '+%B')/" + nombre_respaldo + " "+ruta_respaldo+"/$(date '+%Y')/$(date '+%B')/htsj_administrativo.sql "+ruta_respaldo+"/$(date '+%Y')/$(date '+%B')/htsj_peritos.sql "+ruta_respaldo+"/$(date '+%Y')/$(date '+%B')/htsj_gestion.sql "+ruta_respaldo+"/$(date '+%Y')/$(date '+%B')/htsj_peritos.sql "+ruta_respaldo+"/$(date '+%Y')/$(date '+%B')/htsj_gestion.sql ",
    rash + "rm -rf "+ruta_respaldo+"/$(date '+%Y')/$(date '+%B')/htsj_administrativo.sql",
    rash + "rm -rf "+ruta_respaldo+"/$(date '+%Y')/$(date '+%B')/htsj_peritos.sql",
    rash + "rm -rf "+ruta_respaldo+"/$(date '+%Y')/$(date '+%B')/htsj_gestion.sql",
    rash + "rm -rf "+ruta_respaldo+"/$(date '+%Y')/$(date '+%B')/htsj_laboral.sql"
]


if TRAINING==False:
    #Imprimir las variables de log
    logging.info("[BEGIN] - " + str(datetime.now()))
    logging.info("Ruta respaldo: " + ruta_respaldo)
    logging.info("Nombre respaldo: " + nombre_respaldo)
    logging.info("Fecha: " + fecha)
    logging.info("IP del servidor: " + hostname)
    logging.info("IP del almacenamiento: " + nas_hostname)

    #Ejecutar comandos
    '''phantasm.secuential_execute(preparacion, hostname, username, password, port)
    phantasm.parallel_execute(bloque_mysqldump, hostname, username, password, port)
    phantasm.secuential_execute(bloque_final, hostname, username, password, port)'''

    bloque_secuencial = preparacion + bloque_mysqldump + bloque_final
    phantasm.secuential_execute(bloque_secuencial, hostname, username, password, port)

    logging.info("[OK] - " + str(datetime.now()))
else:
    print("Ruta respaldo: " + ruta_respaldo)
    print("Nombre respaldo: " + nombre_respaldo)
    print("Fecha: " + fecha)
    print("IP del servidor: " + hostname)
    print("IP del almacenamiento: " + nas_hostname)

    bloque_secuencial = preparacion + bloque_mysqldump + bloque_final
    for i in bloque_secuencial: print(i)