import time
import sys
import os

#Funcion para limpiar la consola
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def input_entero(prompt, opciones_validas=None):
    #Lee un entero y valida que esté en opciones_validas (si se indica).
    while True:
        entrada = input(prompt)
        if entrada.isdigit():
            valor = int(entrada)
            if opciones_validas is None or valor in opciones_validas:
                return valor
            else:
                print(f"Opción inválida. Elige entre {sorted(opciones_validas)}.")
        else:
            print("Entrada inválida. Ingresa un número.")

#  CLASES
class Cafetera:
    def encendido(self):
        op = input_entero("¿Encender cafetera?\n 1: Sí\n 0: No\n> ", {0, 1})
        if op == 1:
            print("Cafetera encendida.")
            return True
        print("Cafetera apagada.")
        return False

class SensorAgua:
    #Gestiona el tanque de agua. El nivel solo baja cuando se llena la jarra.

    def __init__(self):
        self.nivel = 0
    def ingresar_agua(self):
        while True:
            entrada = input("Ingrese la cantidad de agua (ml): ")
            if entrada.isdigit() and int(entrada) > 0:
                self.nivel += int(entrada)
                print(f"Tanque actualizado: {self.nivel} ml.")
                return
            print("Entrada inválida. Ingresa un número positivo.")

    def hay_suficiente(self):
        #Retorna True si hay >= 150 ml
        return self.nivel >= 150

    def consumir(self):
        #Descuenta 150 ml del tanque (solo al llenar la jarra).
        self.nivel -= 150
        print(f"Se usaron 150 ml. Agua restante en tanque: {self.nivel} ml.")

class SensorJarra:
    def __init__(self):
        self.puesta = True  #estado físico de la jarra
    def jarra_puesta(self):
        while True:
            op = input_entero("¿La jarra está puesta?\n 1: Sí\n 2: No\n> ", {1, 2})
            if op == 1:
                self.puesta = True
                print("Jarra en base.")
                return
            print("Coloca la jarra y confirma cuando esté lista.")

class Filtro:
    def verificar(self):
        #Confirma filtro de papel, café molido y posición en compartimento.
        while True:
            op = input_entero("¿Está el filtro de papel puesto?\n 1: Sí\n 2: No\n> ", {1, 2})
            if op == 1:
                print("Filtro de papel: ✓")
                break
            print("Coloca el filtro de papel.")

        while True:
            op = input_entero("¿Hay café molido en el filtro?\n 1: Sí\n 2: No\n> ", {1, 2})
            if op == 1:
                print("Café molido: ✓")
                break
            cucharadas = input("¿Cuántas cucharadas de café agregas? ")
            if cucharadas.isdigit() and int(cucharadas) > 0:
                print(f"Se agregaron {cucharadas} cucharadas.")
            else:
                print("Entrada inválida, intenta de nuevo.")

        while True:
            op = input_entero("¿El filtro está en el compartimento?\n 1: Sí\n 2: No\n> ", {1, 2})
            if op == 1:
                print("Filtro en compartimento: ✓")
                return
            print("Coloca el filtro en el compartimento.")


class Calentador:
    #Temperatura arranca en 0 grados y sube linealmente.
    #Rango óptimo de temperatura: 85-96 grados
    #Modo mantenimiento: baja hasta < 79 grados
    #Apagado total: baja hasta 0 grados
    PASO_CALOR  = 5.0
    PASO_ENFRIO = 2.0

    def __init__(self):
        self.temperatura  = 0.0
        self.encendido    = False  #estado de la resistencia

    def calentar(self):
        self.encendido = True
        while self.temperatura < 85:
            self.temperatura += self.PASO_CALOR
            if self.temperatura > 96:
                self.temperatura = 96.0
            sys.stdout.write(f"\rCalentando agua... {self.temperatura:.1f} °C   ")#Animacion de la subida linea de la temperatura del agua en grados
            sys.stdout.flush()
            time.sleep(0.3)
        print(f"\nTemperatura óptima alcanzada: {self.temperatura:.1f} °C ")

    def mantener(self):
        #Modo mantenimiento: baja hasta < 79 grados
        print("Modo mantenimiento: enfriando resistencia...")
        self.encendido = False
        while self.temperatura >= 79:
            self.temperatura -= self.PASO_ENFRIO
            if self.temperatura < 0:
                self.temperatura = 0.0
            sys.stdout.write(f"\rEnfriando... {self.temperatura:.1f} °C   ")#Animacion del enfriamiento
            sys.stdout.flush()
            time.sleep(0.3)
        print(f"\nResistencia en reposo: {self.temperatura:.1f} °C (< 79 °C) ")

    def apagado_total(self):
        #Bajón completo hasta 0 grados (fin de programa).
        print("Apagando resistencia eléctrica...")
        self.encendido = False
        while self.temperatura > 0:
            self.temperatura -= self.PASO_ENFRIO * 2   #baja más rápido al apagar
            if self.temperatura < 0:
                self.temperatura = 0.0
            sys.stdout.write(f"\rApagando... {self.temperatura:.1f} °C   ")
            sys.stdout.flush()
            time.sleep(0.2)
        print("\nResistencia apagada. Temperatura: 0.0 °C")

    def prender(self):
        #Vuelve a encender la resistencia (tras reponer la jarra)
        self.encendido = True
        print("Resistencia eléctrica encendida de nuevo.")
        if self.temperatura < 85:
            self.calentar()
        else:
            print(f"Temperatura actual: {self.temperatura:.1f} °C — lista para continuar.")

class SensorPresion:
    #Peso base de la jarra vacía: 1.25 kg.
    #Cada preparación agrega 0.15 kg.
    #Tope máximo: 3.25 kg, modo mantenimiento.
    PESO_BASE   = 1.25
    PESO_MAXIMO = 3.25
    INCREMENTO  = 0.15

    def __init__(self):
        self.peso_jarra  = self.PESO_BASE
        self.jarra_puesta = True   #estado físico sincronizado con SensorJarra

    def verificar_presion(self):
        estado = "JARRA AUSENTE" if not self.jarra_puesta else f"{self.peso_jarra:.2f} kg"#se verifica si esta la jarra en funcion de las interacciones del menu
        print(f"Sensor de presión: OK. Peso detectado: {estado}")

    def retirar_jarra(self):
        #Registra que la jarra fue retirada físicamente.
        self.jarra_puesta = False
        print(f"Jarra retirada. Último peso registrado: {self.peso_jarra:.2f} kg")

    def reponer_jarra(self):
        #Registra que la jarra fue repuesta.
        self.jarra_puesta = True
        print(f"Jarra repuesta. Peso actual: {self.peso_jarra:.2f} kg")

    def llenar_jarra(self):
        #Llena la jarra linealmente (+0.15 kg en 10 pasos).
        #Retorna False si se alcanzó el tope máximo.
        pasos = 10
        incremento_por_paso = self.INCREMENTO / pasos
        for i in range(pasos):
            self.peso_jarra += incremento_por_paso
            sys.stdout.write(f"\rLlenando jarra... {self.peso_jarra:.3f} kg   ")
            sys.stdout.flush()
            time.sleep(1)
        print()

        if self.peso_jarra >= self.PESO_MAXIMO:
            self.peso_jarra = self.PESO_MAXIMO
            print(f"Jarra llena al máximo ({self.PESO_MAXIMO} kg). Modo mantenimiento activado.")
            return False
        print(f"Café añadido. Peso de la jarra: {self.peso_jarra:.2f} kg ")
        return True

    def servir_cafe(self):
        #Descuenta la última porción servida y muestra la conversión
        volumen_ml = self.INCREMENTO * 1000
        self.peso_jarra -= self.INCREMENTO
        if self.peso_jarra < self.PESO_BASE:
            self.peso_jarra = self.PESO_BASE
        print(f"Café servido: {volumen_ml:.0f} ml / {self.INCREMENTO:.2f} L")
        print(f"Peso de la jarra tras servir: {self.peso_jarra:.2f} kg")
        time.sleep(2)

class Valvula:
    def __init__(self):
        self.abierta = False

    def abrir(self):
        if not self.abierta:
            self.abierta = True
            print("Valvula abierta. El cafe fluye hacia la jarra.")

    def cerrar(self):
        if self.abierta:
            self.abierta = False
            print("Valvula cerrada.")

class BarraProgreso:
    def preparar(self):
        for i in range(101):
            barra = "#" * (i // 2)
            sys.stdout.write(f"\rPreparando: [{barra:<50}] {i}%")
            sys.stdout.flush()
            time.sleep(0.05)
        print("\n¡Café listo!")

#  PANEL DE ESTADO

def mostrar_estado(sensor_agua, calentador, sensor_presion, valvula):
    resistencia = "ON " if calentador.encendido else "OFF"
    jarra_txt   = f"{sensor_presion.peso_jarra:.2f} kg" if sensor_presion.jarra_puesta else "RETIRADA"
    print("──────────────────────────────────")
    print("          ESTADO ACTUAL           ")
    print(f"  Agua en tanque  : {sensor_agua.nivel:>6} ml      ")# el :>6 funciona para alinear los valores dentro de la tabla 
    print(f"  Temperatura     : {calentador.temperatura:>6.1f} °C     ")#Union de los caracteres de alineacion y la impresion de un float .1f
    print(f"  Resistencia     :    {resistencia}          ")
    print(f"  Peso jarra      : {jarra_txt:<10}      ")
    print(f"  Válvula         : {'Abierta  ' if valvula.abierta else 'Cerrada  '}         ")
    print("──────────────────────────────────")

#  MENÚ DE INTERACCIONES EXTERNAS--------------------------
#  Aparece justo debajo del estado

def menu_externo(sensor_agua, calentador, sensor_presion, valvula, sensor_jarra):
    
    #Muestra las opciones de interacción física disponibles.
    #El usuario puede elegir una acción o continuar con el flujo normal.
    #Retorna False si se debe terminar el programa, True si se continúa.
    print("┌─────────────────────────────────-┐")
    print("| Interacciones externas           |")
    print("│  1: Continuar                    │")
    print("│  2: Quitar la jarra              │")
    print("│  3: Apagar la cafetera           │")
    print("└──────────────────────────────────┘")

    op = input_entero("> ", {1, 2, 3})

    #Opción 1: continuar normalmente 
    if op == 1:
        return True

    #Opción 2: quitar la jarra 
    if op == 2:
        valvula.cerrar()                   #seguridad: cierra válvula si estaba abierta
        sensor_presion.retirar_jarra()
        sensor_jarra.puesta = False
        calentador.mantener()              #resistencia baja a < 79 °C mientras jarra fuera
        time.sleep(3)
        clear()
        mostrar_estado(sensor_agua, calentador, sensor_presion, valvula)
        print("Jarra fuera del sensor de presión.")

        op2 = input_entero(
            "¿Desea reponer la jarra?\n 1: Sí (continuar)\n 0: No (apagar cafetera)\n> ",
            {0, 1}
        )

        if op2 == 1:
            sensor_presion.reponer_jarra()
            sensor_jarra.puesta = True
            calentador.prender()           #resistencia vuelve a encenderse
            clear()
            mostrar_estado(sensor_agua, calentador, sensor_presion, valvula)
            print("Jarra repuesta. Reanudando proceso...\n")
            return True                    #sigue el flujo normal

        else:
            # Apagado completo
            _secuencia_apagado(calentador, valvula)
            return False                   #señal para terminar el programa

    #Opción 3: apagar la cafetera 
    if op == 3:
        _secuencia_apagado(calentador, valvula)
        return False


def _secuencia_apagado(calentador, valvula):
    #Cierra válvula y baja temperatura hasta 0 grados
    print("\nIniciando secuencia de apagado...")
    valvula.cerrar()
    calentador.apagado_total()
    print("Cafetera apagada completamente. ¡Hasta luego!")

#PROGRAMA PRINCIPAL

def main():
    cafetera       = Cafetera()
    sensor_agua    = SensorAgua()
    sensor_jarra   = SensorJarra()
    filtro         = Filtro()
    barra          = BarraProgreso()
    calentador     = Calentador()
    sensor_presion = SensorPresion()
    valvula        = Valvula()

    clear()
    print("══════════════════════════════════════════")
    print("       SIMULADOR DE CAFETERA                ")
    print("══════════════════════════════════════════\n")

    # ── 1 Encender ────
    while not cafetera.encendido():
        print("Enciende la cafetera para continuar.\n")

    # ── 2 Agua inicial ──────
    clear()
    print("── Configuración inicial ──")
    sensor_agua.ingresar_agua()
    sensor_presion.verificar_presion()

    # ── 3 Bucle principal ─────
    while True:
        clear()
        mostrar_estado(sensor_agua, calentador, sensor_presion, valvula)

        #Menú externo 
        if not menu_externo(sensor_agua, calentador, sensor_presion, valvula, sensor_jarra):
            return

        #Jarra puesta
        clear()
        sensor_jarra.jarra_puesta()

        clear()
        mostrar_estado(sensor_agua, calentador, sensor_presion, valvula)

        #Menú externo (paso: tras confirmar jarra)
        if not menu_externo(sensor_agua, calentador, sensor_presion, valvula, sensor_jarra):
            return

        #Agua suficiente (sin descontar todavía)
        while not sensor_agua.hay_suficiente():
            print(f" Agua insuficiente ({sensor_agua.nivel} ml). Se necesitan 150 ml.")
            op = input_entero("¿Desea agregar agua?\n 1: Sí\n 0: Apagar cafetera\n> ", {0, 1})
            if op == 0:
                _secuencia_apagado(calentador, valvula)
                return
            sensor_agua.ingresar_agua()

        clear()
        mostrar_estado(sensor_agua, calentador, sensor_presion, valvula)

        #Menú externo (paso: agua verificada) 
        if not menu_externo(sensor_agua, calentador, sensor_presion, valvula, sensor_jarra):
            return

        #Calentamiento
        if calentador.temperatura < 85:
            calentador.calentar()
        else:
            print(f"Agua ya caliente: {calentador.temperatura:.1f} °C ✓")

        clear()
        mostrar_estado(sensor_agua, calentador, sensor_presion, valvula)

        #Menú externo (paso: agua caliente) 
        if not menu_externo(sensor_agua, calentador, sensor_presion, valvula, sensor_jarra):
            return

        #Presión + filtro
        sensor_presion.verificar_presion()
        filtro.verificar()
        clear()

        #Llenando jarra
        barra.preparar()

        #Llenar jarra — el agua baja AQUÍ
        valvula.abrir()
        sensor_agua.consumir()
        tope_alcanzado = sensor_presion.llenar_jarra()
        valvula.cerrar()

        clear()
        mostrar_estado(sensor_agua, calentador, sensor_presion, valvula)

        #Modo mantenimiento si jarra llegó al tope
        if not tope_alcanzado:
            calentador.mantener()
            clear()
            mostrar_estado(sensor_agua, calentador, sensor_presion, valvula)
            print("La jarra ha alcanzado su capacidad máxima (3.25 kg).")
            print("Debes servir el café antes de continuar.\n")

        #Menú externo (paso: jarra llena) 
        if not menu_externo(sensor_agua, calentador, sensor_presion, valvula, sensor_jarra):
            return

        #Servir café, se hace un condicional para pedirle al usurio si servir el cafe o seguir
        op_servir = input_entero(
            "¿Desea servir el café?\n 1: Sí\n 2: No (dejar en jarra)\n> ", {1, 2}
        )
        if op_servir == 1:
            sensor_presion.servir_cafe()
            time.sleep(3)
        else:
            print("El café permanece en la jarra.")

        clear()
        mostrar_estado(sensor_agua, calentador, sensor_presion, valvula)

        #Menu externo (paso: final de ciclo)
        if not menu_externo(sensor_agua, calentador, sensor_presion, valvula, sensor_jarra):
            return

        #Mas café?
        op_mas = input_entero("¿Preparar más café?\n 1: Sí\n 0: No (apagar)\n> ", {0, 1})
        if op_mas == 0:
            _secuencia_apagado(calentador, valvula)
            return