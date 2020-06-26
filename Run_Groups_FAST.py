#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#ESTE PROGRAMA ACTIVA FAST Y LE PASA LOS ARCHIVOS INPUT POR GRUPOS
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
import os
import time
import math
winproc="FAST_Win32.exe"
tmp=os.popen("tasklist").read()											#retorna la cadena  de la lista de tareas

#=======================CREACION DE LOS COMANDOS PARA LLAMAR A FAST EN CADA CASO====================
file=open("Out_ListHydroDats.txt",'r').read()							# lee los nombres de los archivos input
elements=file.split("\n")												#Leer nombres, separar lineas y guardarlos en variable
new_elements=list()

for i in range(len(elements)):											#crea las lineas de comando para ejecutar el FAST
	if not elements[i]:
		pass
	else:
		new_elements.append("start cmd.exe /c  FAST_Win32.exe "+(elements[i])[:-4]+".fst")
							#Lineas de llamada individual por cada caso analizado
		
#=======================================================================
#     EJECUTANDO LOS COMANDOS DE FAST EN PAQUETES
#                DE 'n' GRUPOS CON 's' ELEMENTOS
#=======================================================================
print("Cuantos casos a la vez quieres corer en FAST?")
s_elements=int(input())													#numero de elementos por paquete, es el numero de ventanas FAST
n_group=math.ceil(len(new_elements)/s_elements)							#N° de veces que se correran los 's' comandos

print("Hay un total de ",len(new_elements)," llamados a FAST, si se toman: ",s_elements," por grupo, entonces habrian: ",n_group," grupos")
commands_Fast=list()													#Lista vacia para almacenar los llamados a paquetes

for  r in range(n_group):
	commands_Fast.append(" & ".join(new_elements[(r*(s_elements)):((r+1)*(s_elements))]))	#Guardamos las lineas de llamda a todos los procesos de FAST
	# ~ print("Paquete de comandos [",r,"] es: \n \n",commands_Fast[r],"\n")

#=====================EJECUCION DE FAST==================================
# ~ cwd=os.getcwd() # ~ print("esta en el directorio",cwd) # ~ delayfastmessage=10
c=0																		#Contador
while(c<=n_group):
	if(winproc in tmp):
		print(winproc," sigue activo")									# a las",time.strftime('%H:%M:%S GMT',time.localtime()))
		time.sleep(30)													#Esperar 30 segundos
		tmp=os.popen("tasklist").read()									#Actualizando el status de FAST
	else:
		print("FAST inactivo, lanzando grupo:",c)						#Lanzando el grupo
		os.system(commands_Fast[c])										#Activar FAST
		time.sleep(10)													#Esperando 10 segundos			
		tmp=os.popen("tasklist").read()									#Actualizando el status de FAST
		c=c+1															#Actualizando contador
while(winproc in tmp):
	print(winproc," sigue activo")
	time.sleep(30)
	tmp=os.popen("tasklist").read()

print("FAST termino satisfactoriamente")
