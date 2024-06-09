import math
import sys
import csv
import numpy as np
from randomV import Exponential


#Descripcion del problema donde el tiempo de servicio posee una distribucion
#Exponencial y el tiempo de llegada una distribucion de Poisson. Ademas se tiene
#un costo inicial del programa y un costo por hora para cada ordenador inactivo


def Simulation(exponentialLambda:float, poissonLambda:float, timeLimit:float):
    time:float = 0
    entryTime:float = 0
    exitTime:float = 0
    numberOfEntries:int = 0
    numberOfExits:int = 0
    Entries:{int,float} = {}
    Exits:{int,float} = {}
    queue:int = 0
    maxQueueValue:int = 0
    initialTime = Exponential(poissonLambda)
    entryTime = initialTime
    exitTime = math.inf
    
    #todo export to csv to work with statistics later
    while True:
        
        if(entryTime<=exitTime and entryTime <= timeLimit):
            time = entryTime
            numberOfEntries+=1
            queue+=1
            if(queue>maxQueueValue):
                maxQueueValue = queue
            next = Exponential(poissonLambda)
            entryTime = time + next

            if(queue==1):
                ex = Exponential(exponentialLambda)
                exitTime = time+ex
            Entries[numberOfEntries] = time #? esto deberia subirse
        
        if(exitTime<entryTime):
            time = exitTime
            numberOfExits+=1
            queue-=1

            if(queue==0): 
                exitTime = math.inf
            else:
                next = Exponential(exponentialLambda)
                exitTime = time+next
            Exits[numberOfExits] = time
        
        if(min(entryTime,exitTime) == entryTime and entryTime>timeLimit):
            entryTime = math.inf
        
            while(queue>0):
                time = exitTime
                numberOfExits+=1
                queue-=1
        
                if(queue>0):
                    exitTime = time + Exponential(exponentialLambda)
        
                Exits[numberOfExits] = time
        
            return (Entries, Exits, maxQueueValue)


def Compute(initialCost, partialCost, lambdaE:float, lambdaP:float, topTime:float):
    Entries, Exits, maxQueueValue = Simulation(lambdaE, lambdaP, topTime)
    counter = 0
    for i in range(len(Entries)):
        counter += abs(Entries[i+1]-Exits[i+1])
        # print("costo hasta ahora", counter)
    cost = initialCost + counter*partialCost
    return (cost, maxQueueValue)