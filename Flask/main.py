from flask import Flask, request, redirect
import autobackup, os
from time import sleep
from random import randint

app = Flask(__name__)

@app.route("/")
def hello_world():
    try:
        flask_cors_options = ['*', 'http://localhost:8080', 'https://localhost:8080', 'http://auto-backup-vuejs-1:8081', 'http://10.22.165.29:8081', 'http://auto-backup-express-1:8080', 'http://10.22.165.29:5000']
        flask_cors_options = '*'
        id_backup = request.args.get('id')

        resultado = autobackup.main(id_backup)

        if(resultado == "[ALL OK]"):
            codigo = 200
        if(resultado == "[FINISHED WITH ERRORS]"):
            codigo = 500
        if(resultado == "[NOT OK]"):
            codigo = 500

        #return resultado, codigo, {'Access-Control-Allow-Origin':os.environ['FLASK_CORS_OPTIONS'].split(",")}
        return resultado, codigo, {'Access-Control-Allow-Origin': '*'}
        
        #Ojo: Debemos poner el cors apuntando al origen del axios
    except:
        #return 'Flask', 200, {'Access-Control-Allow-Origin':os.environ['FLASK_CORS_OPTIONS'].split(",")}
        return resultado, codigo, {'Access-Control-Allow-Origin': '*'}
