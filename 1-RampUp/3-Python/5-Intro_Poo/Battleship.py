class Barco:
    def __init__(self,nombre,tamano):
        self.nombre = nombre
        self.tamano = tamano
        self.posicion = []
        self.golpes = 0

    def recibir_golpe(self):
        self.golpes += 1

    def esta_hundido(self):
        return self.golpes >= self.tamano


class Tablero:
    def __init__(self):
        self.tamano = 10
        self.tablero = [["O"] * self.tamano for _ in range(self.tamano)]
        self.barcos = []

    def colocar_barcos(self,barco,posicion,orientacion):
        fila, columna = posicion
        posiciones = []

        for i in range(barco.tamano):
            if orientacion == "horizontal":
                posiciones.append((fila,columna + i))
            else:
                posiciones.append((fila + i,columna))

        for pos in posiciones:
            f,c = pos
            if f >= self.tamano or c >= self.tamano or self.tablero[f][c] != "O":
                return False  
            
        for pos in posiciones:
            f, c = pos
            self.tablero[f][c] = "B" 
        barco.posicion = posiciones
        self.barcos.append(barco)
        return True
    
    def recibir_ataque(self, fila, columna):
        if self.tablero[fila][columna] == "B":
            self.tablero[fila][columna] = "X"
            for barco in self.barcos:
                if (fila, columna) in barco.posicion:
                    barco.recibir_golpe()
                    return "Golpe" if not barco.esta_hundido() else "Barco hundido"
        elif self.tablero[fila][columna] == "O":
            self.tablero[fila][columna] = "-"
            return "Agua"
        return "Ya atacado"
    
    def mostrar_tablero(self):
        print("   " + " ".join(str(i + 1) for i in range(self.tamano)))
        for idx, fila in enumerate(self.tablero):
            letra = chr(65 + idx)
            print(f"{letra} " + " ".join(fila))


    def todos_barcos_hundidos(self):
        return all(barco.esta_hundido() for barco in self.barcos)
    


class Jugador:
    def __init__(self, nombre):
        self.nombre = nombre
        self.tablero = Tablero()

    def atacar(self, oponente, fila, columna):
        return oponente.tablero.recibir_ataque(fila, columna)


class Juego:
    def __init__(self, jugador1, jugador2):
        self.jugador1 = jugador1
        self.jugador2 = jugador2

    def iniciar_juego(self):
        """Inicia la partida entre dos jugadores, alternando los turnos hasta que uno gane."""
        turno = self.jugador1
        oponente = self.jugador2
        while True:
            print(f"\nTurno de {turno.nombre}")
            turno.tablero.mostrar_tablero()
            fila = int(input("Ingresa fila (1-10): ")) - 1
            columna = int(input("Ingresa columna (1-10): ")) - 1
            resultado = turno.atacar(oponente, fila, columna)
            print(f"Resultado del ataque: {resultado}")
            if oponente.tablero.todos_barcos_hundidos():
                print(f"{turno.nombre} ha ganado el juego!")
                break
            turno, oponente = oponente, turno


jugador1 = Jugador("Jugador 1")
jugador2 = Jugador("Jugador 2")

juego = Juego(jugador1, jugador2)
juego.iniciar_juego()








