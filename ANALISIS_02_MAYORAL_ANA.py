# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 17:03:59 2020

@author: Dicssa
"""
#Exportacion origen
#importacion destino
import csv
import numpy as np
###LECTURA DE DATOS
data=[]
with open("synergy_logistics_database.csv","r") as archivo:
     lector=csv.DictReader(archivo)
     for linea in lector:
         data.append(linea)
### ESTADISTICA DESCRIPTIVA###
valor=[]
datos=[]
valores=[]
años=['2018','2019','2020']
for año in años:
    for dato in data:
        if dato["year"]==año:
            valor.append(int(dato["total_value"]))
    datos.append(valor)
    valor=[]
informacion=[]
for fila in datos:
    media=round(np.mean(fila),2)
    mediana=round(np.median(fila),2)
    std=round(np.std(fila),2)
    informacion.append([media,mediana,std])
for dato in data:
   valores.append(int(dato["total_value"]))
print("ESTADÍSTICA DESCRIPTIVA")
print("Historico")
print("Media: ",round(np.mean(valores),2))
print("Mediana: ",round(np.median(valores),2))
print("Desviación estandar: ",round(np.std(valores),2))
for i in range(0,3):
    print(años[i])
    print("Media: "+str(informacion[i][0]))
    print("Mediana: "+str(informacion[i][1]))
    print("Desviación estandar: "+str(informacion[i][2]))

#### FUNCIONES DEL PROGRAMA ####
 #FUNCION PARA OBTENER LA INFORMACION DE LAS RUTAS       
def rutas(direccion="Exports"): #para obtener la informacion para cada ruta
    ruta_contada=[]
    cont=0
    valortotal=0
    info_rutas=[]
    for ruta in data:
        if ruta["direction"]==direccion :
            ruta_actual=[ruta["origin"],ruta["destination"]]
            if ruta_actual not in ruta_contada:
                for dato in data:
                    if ruta_actual==[dato["origin"],dato["destination"]] and dato["direction"]==direccion:
                        cont+=1
                        valortotal+=int(dato["total_value"])
                ruta_contada.append(ruta_actual)
                info_rutas.append([ruta["origin"],ruta["destination"],cont,valortotal])
                cont=0
                valortotal=0  
        else:
            continue
    return info_rutas
def suma(lista): #para obtener la suma de expo o impo
   exptotales=0
   top=0
   sumatop=0
   for elemento in lista:
        exptotales+=elemento[3]
        if top<10:
            sumatop+=elemento[3]
            top+=1
   return([exptotales,sumatop])
def transportes(): #para obtener la informacion de cada transporte
    medio_transportes=[]
    conta=0
    info_transportes=[]
    valorttotal=0
    for dato in data:
        medio_actual=dato["transport_mode"]
        if medio_actual not in medio_transportes:
            for viaje in data:
                if viaje["transport_mode"]==medio_actual:
                    conta+=1
                    valorttotal+=int(viaje["total_value"])
            medio_transportes.append(medio_actual)
            info_transportes.append([medio_actual,conta,valorttotal])
            conta, valorttotal=0,0
    return info_transportes

def porcentaje(datos,totales,exp=1):#opcion 3
    paises=[]
    total=0
    info=[]
    porcentaje=0
    ochenta=[]
    if exp==1:
        for viaje in datos:
            pais_actual=viaje[0]
            if pais_actual not in paises:
                for pais in datos:
                    if pais[0]==pais_actual:
                        total+=int(pais[3])
                paises.append(pais_actual)
                info.append([pais_actual,total])
                total=0
    else:
        for viaje in datos:
            pais_actual=viaje[1]
            if pais_actual not in paises:
                for pais in datos:
                    if pais[1]==pais_actual:
                        total+=int(pais[3])
                paises.append(pais_actual)
                info.append([pais_actual,total])
                total=0
    for elemento in info:
        per=round(elemento[1]*100/totales,3)
        elemento.append(per)
    info.sort(reverse=True,key=lambda x:x[2])
    n=0
    while porcentaje<80.5:
        porcentaje+=info[n][2]
        ochenta.append(info[n])
        n+=1
    return [ochenta,n,len(info),porcentaje]
###FIN DE FUNCIONES####
### RESULTADOS####
exportaciones=rutas(direccion="Exports")
importaciones=rutas(direccion="Imports")
exportaciones.sort(reverse=True,key=lambda x:x[3])
importaciones.sort(reverse=True,key=lambda x:x[3])
top10exp=exportaciones[:10]
top10imp=importaciones[:10]
expinf=suma(exportaciones)
impinf=suma(importaciones)
perexp=porcentaje(exportaciones,expinf[0],1)
perimp=porcentaje(importaciones,impinf[0],0)
    
print("EXPORTACIONES")
for ruta in top10exp:
    print("Ruta: " +ruta[0]+"--> "+ruta[1])
print("El top 10 de exportaciones representa un "+str(round(expinf[1]/expinf[0]*100,3)) +"%")
print("IMPORTACIONES")
for viaje in top10imp:
    print("Ruta: " +viaje[0]+"--> "+viaje[1])
print("El top 10 de importaciones representa un "+str(round(impinf[1]/impinf[0]*100,3)) +"%")

print("EXPORTACIONES")
print("Paises que generan un 80% de las exportaciones totales:")
print(perexp[:-3])
print("Porcentaje: "+str(perexp[-1]))
print("Considera "+str(perexp[-3])+ " paises de "+str(perexp[-2]))
print("IMPORTACIONES")
print("Paises que generan un 80% de las importaciones totales:")
print(perimp[:-3])
print("Porcentaje: "+str(perimp[-1]))
print("Considera "+str(perimp[-3])+ " paises de "+str(perimp[-2]))

print("MEDIOS DE TRANSPORTE")
transporte=transportes()
transporte.sort(reverse=True,key=lambda x:x[2])
print("El orden de transportes es: [medio de transporte,no. viajes,total]")
for medio in transporte:
    print(medio)
print("Considerando el medio de transporte por carretera el menos productivo, si se eliminara su practica se reducirian los ingresos en un "+str(round(transporte[3][2]*100/sum(valores),3))+"%")
print(expinf[0]/impinf[0])