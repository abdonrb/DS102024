import numpy as np
import random

tablero = np.full((10,10),' ',dtype=str)
tablero[(0,1),(1,1)] = 'O'
tablero[(1,3)] = 'O'
tablero[(1,4)] = 'O'
tablero[(1,5)] = 'O'
tablero[(1,6)] = 'O'

disparo1 = int(input('Dime la fila que quieres disparar:')) -1
disparo2 = int(input('Ahora la columna:')) -1

for c in tablero:
    if tablero[(disparo1,disparo2)] == 'O':
        tablero[(disparo1,disparo2)] = 'X'
    elif tablero[(disparo1,disparo2)] == ' ':
        tablero[(disparo1,disparo2)] = '-'

print(tablero)
