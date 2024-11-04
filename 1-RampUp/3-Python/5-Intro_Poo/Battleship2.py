class Barco:
    def __init__(self, nombre, tamano):
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
        self.tablero = [["-"] * self.tamano for _ in range(self.tamano)]
        self.barcos = []

    def colocar_barco(self, barco, posicion, orientacion):
        fila, columna = posicion
        posiciones = []

        for i in range(barco.tamano):
            if orientacion == "horizontal":
                posiciones.append((fila, columna + i))
            else:
                posiciones.append((fila + i, columna))

        for f, c in posiciones:
            if f >= self.tamano or c >= self.tamano or self.tablero[f][c] != "-":
                return False

        for f, c in posiciones:
            self.tablero[f][c] = "B"
        barco.posicion = posiciones
        self.barcos.append(barco)
        return True

    def mostrar_tablero(self, ocultar_barcos=False):
        print("   " + " ".join(str(i + 1) for i in range(self.tamano)))
        for idx, fila in enumerate(self.tablero):
            if ocultar_barcos:
                fila_oculta = ["-" if celda == "B" else celda for celda in fila]
                print(f"{idx + 1:2} " + " ".join(fila_oculta))
            else:
                print(f"{idx + 1:2} " + " ".join(fila))


    def recibir_ataque(self, fila, columna):
        if self.tablero[fila][columna] == "B":
            self.tablero[fila][columna] = "X"
            for barco in self.barcos:
                if (fila, columna) in barco.posicion:
                    barco.recibir_golpe()
                    return "Golpe" if not barco.esta_hundido() else "Barco hundido"
        elif self.tablero[fila][columna] == "-":
            self.tablero[fila][columna] = "O"
            return "Agua"
        return "Ya atacado"

    def todos_barcos_hundidos(self):
        return all(barco.esta_hundido() for barco in self.barcos)


class Jugador:
    def __init__(self, nombre):
        self.nombre = nombre
        self.tablero = Tablero()

    def colocar_barcos_manual(self):
        tipos_barcos = [
            ("Portaaviones", 5),
            ("Acorazado", 4),
            ("Crucero", 3),
            ("Submarino", 3),
            ("Destructor", 2),
        ]
        
        for nombre, tamano in tipos_barcos:
            while True:
                orientacion = input(f"Ingrese la orientacion para {nombre} (horizontal/vertical): ").strip().lower()
                
                if orientacion not in ["horizontal", "vertical"]:
                    print("Debe ingresar 'horizontal' o 'vertical'.")
                    continue
                try:
                    fila = int(input(f"Ingrese la fila inicial para {nombre} (1-10): ")) - 1
                    columna = int(input(f"Ingrese la columna inicial para {nombre} (1-10): ")) - 1
                except ValueError:
                    print("Debe ingresar un número.")
                    continue

                if fila < 0 or fila >= 10 or columna < 0 or columna >= 10:
                    print("La posición está fuera del rango. Debe estar entre 1 y 10.")
                    continue

                barco = Barco(nombre, tamano)
                if self.tablero.colocar_barco(barco, (fila, columna), orientacion):
                    print(f"{nombre} colocado exitosamente.")
                    break
                else:
                    print("Posición no válida o barco superpuesto, intente nuevamente.")


    def atacar(self, oponente, fila, columna):
        return oponente.tablero.recibir_ataque(fila, columna)


class Juego:
    def __init__(self, jugador1, jugador2):
        self.jugador1 = jugador1
        self.jugador2 = jugador2

    def iniciar_juego(self):
        print(f"\n{self.jugador1.nombre}, coloca tus barcos manualmente:")
        self.jugador1.colocar_barcos_manual()
        
        print(f"\n{self.jugador2.nombre} coloca tus barcos manualmente:")
        self.jugador2.colocar_barcos_manual()
        
        turno = self.jugador1
        oponente = self.jugador2
        while True:
            print(f"\nTurno de {turno.nombre}")
            print(f"Tablero de {oponente.nombre}:")
            oponente.tablero.mostrar_tablero(ocultar_barcos=True)
            
            try:
                fila = int(input("Ingresa fila para atacar (1-10): ")) - 1
                columna = int(input("Ingresa columna para atacar (1-10): ")) - 1
            except ValueError:
                print("Debe ingresar un número.")
                continue
            
            resultado = turno.atacar(oponente, fila, columna)
            print(f"Resultado del ataque: {resultado}")
            
            if oponente.tablero.todos_barcos_hundidos():
                print(f"{turno.nombre} ha ganado el juego!")
                break
            turno, oponente = oponente, turno


jugador1 = Jugador("Abdon")
jugador2 = Jugador("Juan")

juego = Juego(jugador1, jugador2)
juego.iniciar_juego()
