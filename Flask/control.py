from datetime import datetime

#Recibe un mes del datetime.now() en formato %m
#Te regresa el mes en español
def get_month(month):
    months = ['ENERO','FEBRERO','MARZO','ABRIL','MAYO','JUNIO','JULIO','AGOSTO','SEPTIEMBRE','OCTUBRE','NOVIEMBRE','DICIEMBRE']
    return months[int(month)-1]