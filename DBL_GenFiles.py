#////////////////FIRST SCRIPT//////////////////////
#This script generates the file with the data
import pandas as pd
from scipy import stats
from datetime import datetime
import os, math

WD_Master=os.getcwd()
currdate=datetime.now().strftime("%d-%m-%Y_%I-%M-%S_%p")    #to get the current date and hour
#---------------Fixe Values----------
####shear_exp=input('Which shear exponent us used? ')
shear_exp=0.14
H=90
md=8766                                                 # 365.25*24/1hr
au, bu=2.299, 8.92                                      #Weibull Distr. of u_10m

a1,a2,a3=1.755, 0.184, 1                                #aHC=a1+a2*u^a3
b1,b2,b3=0.534,0.07,1.435                               #bHC=b1+b2*u^b3

th_et,gamma_exp= -0.477, 1
e1,e2,e3= 5.563, 0.798, 1
f1,f2,f3= 3.5, 3.592, 0.735
k1,k2,k3= 0.05, 0.388, -0.321

#----------------FUNCTIONS---------
def read_data(column):                  #To get the data from an excel file
    tmp=pd.read_excel(r'./Data/Data.xlsx',usecols=column)
    tmp1=tmp.dropna()
    n_tmp1=int(tmp1.count())
    outvar=list()
    for i in range(n_tmp1):
        outvar.append(float(tmp1.iloc[i]))
    return outvar

def uten(UHH):                          #To convert the Hub-Height Wind Speed to 10m level of reference
    return float(UHH)/(H/10)**shear_exp

def FUW(u):                             #To calculate the cummulative distribution value
    return 1-math.exp(-1*(u/bu)**au)

def get_N(u):                           #To get the return period of the wind speed
    return 1/((1-FUW(u))*md)

#-----------------Initial Steps-----------------
Uw=read_data('A')
Seed_Uw=read_data('B')
Seed_Wv=read_data('C')

u=list()
for i in range(len(Uw)):
    u.append(uten(Uw[i]))

N=list()
for j in range(len(u)):
    N.append(get_N(u[j]))
    
del i,j
#------------Calculation of the most probable sea state----------
#Parameters for Hs
aHC=list()
bHC=list()

for i in range(len(u)):
    aHC.append(a1+a2*(u[i])**a3)
    bHC.append(b1+b2*(u[i])**b3)

Hs=list()
for j in range(len(u)):
    Hs.append(bHC[j]*(math.log(1-0.5)*-1)**(1/aHC[j]))

del i,j
#Parameters for Tp
#muLTC=list()
#sigmaLTC=list()
#
#for i in range(len(u)):
#    muLTC.append(c1+c2*(Hs[i])**c3)
#    sigmaLTC.append((d1+d2*(math.exp(d3*Hs[i])))**0.5)

Tp=list()    
for j in range(len(u)):
    vTp_h=k1+k2*math.exp(Hs[j]*k3)
    Tp_h=e1+e2*(Hs[j])**e3
    u_h=f1+f2*(Hs[j])**f3
    mu_Tp=Tp_h*(1+th_et*((u[j]-u_h)/u_h)**gamma_exp)
    sigma_Tp=vTp_h*mu_Tp
    sigma_lnTp=(math.log(vTp_h**2+1))**0.5
    mu_lnTp=math.log(mu_Tp/(1+vTp_h**2)**0.5)
    Tp.append(stats.lognorm(sigma_lnTp,scale=math.exp(mu_lnTp)).ppf(0.5))

#Saving values
os.chdir(WD_Master)
os.chdir('./Data/')
Results_title="Results Joint Probability (shear="+str(shear_exp)+") "+currdate+".txt"
Results_file=open(Results_title,'w+')
Results_file.write("Uw[m/s] \t u[m/s] \t N[-] \t Hs[m] \t Tp[m] \n")

for i in range(len(Uw)):
    txt=str(Uw[i])+'\t'+str("{0:.3f}".format(u[i]))+'\t'+str("{0:.8f}".format(N[i]))+'\t'+str("{0:.3f}".format(Hs[i]))+'\t'+str("{0:.3f}".format(Tp[i]))+'\n'
    Results_file.write(txt)
Results_file.close()
del txt, Results_title, sigma_lnTp, mu_lnTp, aHC, bHC,  N
del a1, a2, a3, b1, b2, b3
del j, i, Tp_h, e1, e2, e3, f1, f2, f3, k1, k2, k3, mu_Tp, sigma_Tp
del th_et, u_h, vTp_h, gamma_exp
#del md, H, au, bu
#--------------------Creation of *.inp input files for TurbSim-----------------------
os.chdir(WD_Master)
os.chdir('./5MW_Baseline/InflowWind/TS')
WD_TS=os.getcwd()

with open('TS1.dbarretol') as f: ts_1=f.read()
with open('TS2.dbarretol') as f: ts_2=f.read()
with open('TS3.dbarretol') as f: ts_3=f.read()
with open('TS4.dbarretol') as f: ts_4=f.read()

var_tstitle=list()
for i in range(len(Seed_Uw)):
    for j in range(len(Uw)):
        TS_title="Uw"+str(j)+"_SeedUw"+str(i)
        var_tstitle.append(TS_title)
        TS_content=ts_1+str(int(Seed_Uw[i]))+ts_2+str(Uw[j])+ts_3+str(shear_exp)+ts_4
        TS_file=open(TS_title+".inp",'w+')
        TS_file.write(TS_content)
        TS_file.close()

del ts_1, ts_2, ts_3, ts_4, TS_title, TS_content, i, j
#--------------------Creation of *.dat input files for InflowWind-----------------------
os.chdir(WD_Master)
os.chdir('./5MW_Baseline/InflowWind')
WD_IF=os.getcwd()

with open('IF1.dbarretol') as f: if_1=f.read()
with open('IF2.dbarretol') as f: if_2=f.read()

for i in range(len(var_tstitle)):
    IF_content=if_1+var_tstitle[i]+".bts"+if_2
    IF_file=open(var_tstitle[i]+'.dat','w+')
    IF_file.write(IF_content)
    IF_file.close()

del i, IF_content, if_1, if_2
#--------------------Creation of *.dat input files for HydroDyn-----------------------
os.chdir(WD_Master)
os.chdir('./5MW_Baseline/HydroData')
WD_HYD=os.getcwd()

with open('HD1.dbarretol') as f: hd_1=f.read()
with open('HD2.dbarretol') as f: hd_2=f.read()
with open('HD3.dbarretol') as f: hd_3=f.read()
with open('HD4.dbarretol') as f: hd_4=f.read()
with open('HD5.dbarretol') as f: hd_5=f.read()
with open('HD6.dbarretol') as f: hd_6=f.read()
with open('HD7.dbarretol') as f: hd_7=f.read()

var_hdtitle=list()
for ss in range(len(Uw)):
    for i in range(len(Seed_Wv)):
        hd_title="SS"+str(ss)+"_SeedWv"+str(i)
        var_hdtitle.append(hd_title)
        lowcoff=0.25*(2*math.pi/Tp[ss])
        hicoff=5.1*(2*math.pi/Tp[ss])
        seedwv2=Seed_Wv[i]+10
        hd_cnt1=hd_1+str("{0:.3f}".format(Hs[ss]))+hd_2+str("{0:.3f}".format(Tp[ss]))
        hd_cnt2=hd_3+str("{0:.3f}".format(lowcoff))+hd_4+str("{0:.3f}".format(hicoff))
        hd_cnt3=hd_5+str(int(Seed_Wv[i]))+hd_6+str(int(seedwv2))+hd_7
        HD_file=open(hd_title+".dat",'w+')
        HD_file.write(hd_cnt1+hd_cnt2+hd_cnt3)
        HD_file.close()

del seedwv2, hicoff, lowcoff, i, ss
del hd_1, hd_2, hd_3, hd_4, hd_5, hd_6, hd_7
del hd_cnt1, hd_cnt2, hd_cnt3, hd_title
#--------------------------Creation of *.fst input files for FAST 8--------------
os.chdir(WD_Master)

with open('FST1.dbarretol') as f: fst_1=f.read()
with open('FST1_d.dbarretol') as f: fst_1d=f.read()
with open('FST2.dbarretol') as f: fst_2=f.read()
with open('FST3.dbarretol') as f: fst_3=f.read()

for k in range(len(Uw)):
    if(Uw[k]>=19):
        edyn='pitch20'
    else:
        if(Uw[k]>=13):
            edyn='pitch10'
        else:edyn='pitch0'
    
    for i in range(len(Seed_Uw)):
        for j in range(len(Seed_Wv)):
            iftxt="Uw"+str(k)+"_SeedUw"+str(i)+".dat"
            hdtxt="SS"+str(k)+"_SeedWv"+str(j)+".dat"
            fst_title="EC"+str(k)+"_SeedUw"+str(i)+"_SeedWv"+str(j)+".fst"
            fst_content=fst_1+edyn+fst_1d+iftxt+fst_2+hdtxt+fst_3
            fst_file=open(fst_title,'w+')
            fst_file.write(fst_content)
            fst_file.close()
del fst_1, fst_2, fst_3, fst_content, fst_title, hdtxt, iftxt