import os
#=======================================================================
C_names = len(open("List_OUTB.txt").readlines(  )) 						#Cant. de Lineas
file = open("List_OUTB.txt","r").read()									#Abrir y leer nombres
CRU_Titles = file.split("\n")											#Guardar en variable los valores

for i in range(C_names):
	if not CRU_Titles[i]:
		pass
	else:
		CRU_Titles[i]=CRU_Titles[i][:-1]								#Nombres sin '\'
#=======================================================================#RECOPILANDO LA INFORMACION Y CONSOLIDANDO
sts_titles=list()

for i in range(C_names):
	ststitle=CRU_Titles[i][:-5]+".sts"
	sts_titles.append(ststitle)											#sts_titles guarda los nombres de los archivos a abrir
print('Que output quiere consolidar?\n\
7 - (Time)\n\
8 - (Wind1VelX)\n\
9 - (Wind1VelY)\n\
10 - (Wind1VelZ)\n\
11 - (OoPDefl1)\n\
12 - (IPDefl1)\n\
13 - (TwstDefl1)\n\
14 - (BldPitch1)\n\
15 - (Azimuth)\n\
16 - (RotSpeed)\n\
17 - (GenSpeed)\n\
18 - (TwHt1TPxi)\n\
19 - (TwHt1TPyi)\n\
20 - (TTDspTwst)\n\
21 - (PtfmSurge)\n\
22 - (PtfmSway)\n\
23 - (PtfmRoll)\n\
24 - (PtfmPitch)\n\
25 - (Spn2MLxb1)\n\
26 - (Spn2MLyb1)\n\
27 - (RootFxc1)\n\
28 - (RootFyc1)\n\
29 - (RootFzc1)\n\
30 - (RootMxc1)\n\
31 - (RootMyc1)\n\
32 - (RootMzc1)\n\
33 - (RotTorq)\n\
34 - (LSSGagMya)\n\
35 - (LSSGagMza)\n\
36 - (YawBrFxp)\n\
37 - (YawBrFyp)\n\
38 - (YawBrFzp)\n\
39 - (YawBrMxp)\n\
40 - (YawBrMyp)\n\
41 - (YawBrMzp)\n\
42 - (RtAeroFxh)\n\
43 - (RtAeroFyh)\n\
44 - (RtAeroFzh)\n\
45 - (RtAeroMxh)\n\
46 - (RtAeroMyh)\n\
47 - (RtAeroMzh)\n\
48 - (GenPwr)\n\
49 - (GenTq)\n\
50 - (Wave1Elev)\n\
51 - (M2N1MKxe)\n\
52 - (M2N1MKye)\n\
53 - (M1N1MKxe)\n\
54 - (M1N1MKye)\n\
55 - (-ReactFXss)\n\
56 - (-ReactFYss)\n\
57 - (-ReactFZss)\n\
58 - (-ReactMXss)\n\
59 - (-ReactMYss)\n\
60 - (-ReactMZss)\n')

data_line=int(input())
datasts_store=list()

for j in range(C_names):
	sts_file=open(sts_titles[j],"r").read()
	sts_txtlines=sts_file.split("\n")
	datasts_store.append(sts_titles[j]+"\t"+sts_txtlines[data_line])						#GUARDAMOS LAS LINEAS CORRESPONDIENTES A UNA MISMA RESPUESTA DINAMICA
# ~ print(datasts_store)	

title_data="Estadisticos Consolidados_response "+str(data_line)+".xls"	#CREANDO ARCHIVO CONSOLIDADO
sts_resumed=open(title_data,"w+")
sts_resumed.write("Ruta \t"+sts_txtlines[6]+"\n")									#PONIENDO CABECERA
for k in range(len(datasts_store)):
	content_sts=datasts_store[k]+"\n"
	sts_resumed.write(content_sts)
sts_resumed.close()
