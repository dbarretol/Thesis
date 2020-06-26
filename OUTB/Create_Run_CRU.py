import os, time
cwd=os.getcwd()
cwd
#=======================================================================
f=open("List_OUTB.txt","w+")											#Creando archivo
for file in os.listdir(cwd):
	if file.endswith(".outb"):
		rutas=os.path.join(file,"\n")
		f.write(rutas)
f.close()																#Listando los nombres en el archivo pero con '\'
#=======================================================================
C_names = len(open("List_OUTB.txt").readlines(  )) 						#Cant. de Lineas
file = open("List_OUTB.txt","r").read()									#Abrir y leer nombres
CRU_Titles = file.split("\n")											#Guardar en variable los valores

for i in range(C_names):
	CRU_Titles[i]=CRU_Titles[i][:-1]									#Nombres sin '\'
#=======================================================================# CREANDO LOS FILES *.CRU
with open("cru_txt.txt","r") as f:	crusup = f.read()

for k in range(C_names):
	crutitle=CRU_Titles[k][:-5]+".cru"
	crucontent=crusup+"\n"+CRU_Titles[k]
	crufile=open(crutitle,"w+")
	crufile.write(crucontent)
crufile.close()
#=======================================================================#CREANDO COMANDOS PARA LLAMAR A CRUNCH
commands_cru=list()
for j in range(C_names):
	if not CRU_Titles[i]:
		pass
	else:
		commands_cru.append("start cmd.exe /c Crunch_win32.exe "+(CRU_Titles[j])[:-5]+".cru")
# ~ print(commands_cru)
#=======================================================================#CORRIENDO CRUNCH Y GENERANDO STS
for h in range(len(commands_cru)):
	os.system(commands_cru[h])
	# ~ time.sleep(2)	
