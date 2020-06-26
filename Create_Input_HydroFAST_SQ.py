#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#THIS PROGRAM IS FOR HYDRODYN AND FAST INPUT FILES CONSIDERING A SQUARE DOMAIN
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#-------------Paso 1: Creacion de los archivos de HydroDyn---------------------
import os 	      #Detecta el Sistema Operativo
cwd = os.getcwd()     #Directorio de trabajo actual
cwd		      # ~ print(cwd) # Muestra el directorio de trabajo actual
os.chdir("./inp_Hydro")     #Cambiando Directorio de trabajo
cwd = os.getcwd()
cwd			    # ~ print(cwd) # Muestra el directorio de trabajo actual

#========= VERIFICANDO LA CANTIDAD DE ESTADOS DE MAR ====================================
fileHs="inp_Hs.txt"
fileTp="inp_Tp.txt"
countHs = len(open(fileHs).readlines(  )) #Cant. de alturas
countTp = len(open(fileTp).readlines(  )) #Cant. de periodos
n_SS=int((countHs+countTp)/2) 		   #Cant. de estados de mar

print("Verificacion! #Hs es igual a #Tp?")
if (countHs==countTp):
	print("SI")
else:
	print("NO")
	
#============LECTURA DE LAS ALTURAS DE OLA=================================================
file = open(fileHs,"r").read()		#Abrir y leer alturas
elementsHs = file.split("\n")		#Guardar en variable los valores
print("--------ALTURAS DE OLA-------")	
for i in range(countHs): 		#los elementos empiezan a contar desde cero
	print("Hs[",i,"] =",elementsHs[i],"m")
#============LECTURA DE LOS PERIODOS DE OLA====================	
file = open(fileTp,"r").read()		#Abrir y leer periodos
elementsTp = file.split("\n")		#Guardar en variable los valores
print("--------PERIODOS DE OLA-------")	
for i in range(countTp): 		#los elementos empiezan a contar desde cero
	print("Tp[",i,"] =",elementsTp[i],"s")
#=========RESUMEN DE LOS ESTADOS DE MAR ANALIZADOS====================
print("Resumen de Estados de Mar   Hs       Tp")	
for i in range(countHs):
	print("Estado de mar ",i,":        ",elementsHs[i],"   ,  ",elementsTp[i])
print("Cant. de alturas:",countHs,"\nCant. de periodos:",countTp,"\nCant. de Estados de Mar:",n_SS) #os.system("pause")
#---------COPY-PASTE PARA ARCHIVO INPUT DE HYDRODYN------------------------
with open("Hydrotxt_1.txt","r") as f:	csup = f.read()	
with open("Hydrotxt_2.txt","r") as f:	cinf = f.read()	
htext1="   WaveHs         - Significant wave height of incident waves (meters) [used only when WaveMod=1, 2, or 3]"
htext2="   WaveTp         - Peak-spectral period of incident waves       (sec) [used only when WaveMod=1 or 2]"

#==========================DATA FOR VARIATION OF Hs AND Tp========================================
#var_coef=range(-20,21,1)#creamos el  rango  de variación -20%, -19%, -18%, -17%.....19%, 20%
var_coef=[0,1,5,10,15]				#Coef. de Coef. de variación
var_Qty=len(var_coef)				#Cant. de Coef. de variación
coef_Hs=list()					#Creación vectores vacios
coef_Tp=list()

for j in range(var_Qty):			#guardamos los factores multiplicadores de Hs y Tp
		coef_Hs.append(round(1+var_coef[j]/100,4))
		coef_Tp.append(round(1+var_coef[j]/100,4))	# ~ print("new Hs\n",coef_Hs)	# ~ print("new Tp\n",coef_Tp)

for s in range(n_SS):						#barrido de los estados de mar
	for ih in range(var_Qty):				#barrido de alturas
		for it in range(var_Qty):			#barrido de periodos
			ah=float(elementsHs[s])			#La altura del estado de mar 's'
			bh=float(coef_Hs[ih])			#El Coef. Var. de Hs
			tempHs="{0:.3f}".format(ah*bh)		#Multiplica el Hs por su respectivo Coef. Var. # ~ print("tempHs",tempHs)
			
			at=float(elementsTp[s])			#El periodo del estado de mar 's'
			bt=float(coef_Tp[it])			#El Coef. Var. de Tp
			tempTp="{0:.3f}".format(at*bt)		#Multiplica el Tp por su respectivo Coef. Var.	# ~ print("tempTp",tempTp)
			
			           # Sea State          Coef Var Hs/Tp
			namehydro="SS"+str(s)+"_Hs"+str("{0:.0f}".format((coef_Hs[ih]-1)*100))+"_Tp"+str("{0:.0f}".format((coef_Tp[it]-1)*100))+".dat"	#Titulo del Archivo HydroDyn
			contenthydro=csup+"\n         "+str(tempHs)+htext1+"\n         "+str(tempTp)+htext2+"\n"+cinf		#Contenido del archivo input HydroDyn
			hydrofile=open(namehydro,"w+")	#Creacion de un file extension .dat
			hydrofile.write(contenthydro)	#Escritura del contenido en archivo input HydroDyn
		f.close()		# ~ print("Te  quedaste en la ruta:",cwd)
os.chdir("../")				#Me muevo al nivel superior de la carpeta
cwd=os.getcwd()				# ~ print("Ahora estas de nuevo en:",cwd)
#======================CREACION DE ARCHIVO CONTENEDOR DE NOMBRES=====================
namefiledat="Out_ListHydroDats.txt"			
f=open(namefiledat,"w+")		#Creamos un archivo
for file in os.listdir("./inp_Hydro"):	#Buscando en la carpeta inp_Hydro
		if file.endswith(".dat"):	#Solo listamos los archivos *.dat
			x=os.path.join(file,"\n")	#Los reunimos y guardamos con saltos de linea
			f.write(x)			#Escribiendo en archivo
f.close()						#El archivo txt almacenará los nombres de los *.dat de 
							#HydroDyn, pero con un '\' al final de cada registro
#======================ELIMINACION DE '\' DE LOS NOMBRES DE ARCHIVO=====================
n_lines = len(open(namefiledat).readlines(  ))		#numero de lineas *.dat
file = (open(namefiledat,"r").read())			#Se guarda un unico elemento con todo el contenido
ListHydroNm = file.split("\n")				#Se parte el elemento en varios divididos por '\n'
real_ListHydroNm=list()					#lista vacia que almacena nombres sin el '\'

for i in range(n_lines):
	real_ListHydroNm.append((ListHydroNm[i])[:-1])	#Quitando ultimo caracter '\n' y guardando en variable

# ~ for j in range(len(real_ListHydroNm)):
	# ~ print("Archivo [",j,"]=",real_ListHydroNm[j])	#Mostrando los nombres en pantalla

g=open(namefiledat,"w+")	#Creando lista de nombres
for k in range(len(real_ListHydroNm)):
	g.write(real_ListHydroNm[k]+"\n")	#Escribiendo lista de nombres
g.close()
#---------COPY-PASTE PARA ARCHIVO INPUT DE FAST------------------------
with open("fstext_1.txt","r") as f:	csup = f.read()	
with open("fstext_2.txt","r") as f:	cinf = f.read()	
ctext1="    HydroFile       - Name of file containing hydrodynamic input parameters (quoted string)"
#===================Creacion de los archivos  *.fst para FAST==============================
for m in range(len(real_ListHydroNm)):
	namefast=(real_ListHydroNm[m])[:-4]+".fst"	#Quitando extension .dat y poniendo .fst
	content=csup+"\n"+'"inp_Hydro'+'/'+real_ListHydroNm[m]+'"                        '+ctext1+"\n"+cinf	#Creando el contenido del archivo .fst
	fastfile=open(namefast,"w+")	#Creando archivo *.fst
	fastfile.write(content)		#Escribiendo el contenido en el archivo					
fastfile.close()
