#El proyecto consiste en desarrollar un programa interactivo en Python que permita al usuario evaluar
#el nivel de seguridad de su contraseña de forma sencilla y directa. El sistema analizará la clave e
#indicará si es Fuerte, Media o Débil según criterios preestablecidos, proporcionando
#recomendaciones claras para mejorarla. Cuenta con un menú accesible e intuitivo, ideal para
#estudiantes que se inician en la programación.


#-----------Librerías-----------#
from random import random
import secrets
import string
import math
#-------------Constantes----------------
LONGITUD_MINIMA = 8
LONGITUD_SUGERIDA = 16

#-----------Funciones-----------#

#------------Función para verificar la contraseña-----------#
def verificar_contrasena(contrasena):
    """Devuelve una lista de tuplas (problema, recomendación).
    Si la lista está vacía, la contraseña cumple todas las reglas."""
    problemas = []

    if contrasena.lower() in ["123456", "password", "qwerty", "abc123", "letmein"]:
        problemas.append((
            "Es una contraseña muy común o conocida.",
            "Elige otra que no aparezca en listas filtradas; añadir un número "
            "o símbolo al final no la hace segura."
        ))
    if len(contrasena) < LONGITUD_MINIMA:
        problemas.append((
            "Es demasiado corta.",
            f"Debe tener al menos {LONGITUD_MINIMA} caracteres."
        ))
    if not any(c.islower() for c in contrasena):
        problemas.append((
            "No contiene letras minúsculas.",
            "Agrega al menos una letra minúscula."
        ))
    if not any(c.isupper() for c in contrasena):
        problemas.append((
            "No contiene letras mayúsculas.",
            "Agrega al menos una letra mayúscula."
        ))
    if not any(c.isdigit() for c in contrasena):
        problemas.append((
            "No contiene números.",
            "Agrega al menos un número."
        ))
    if not any(c in string.punctuation for c in contrasena):
        problemas.append((
            "No contiene caracteres especiales.",
            "Agrega al menos un carácter especial (por ejemplo: !, @, #)."
        ))

    return problemas

#------------Entropia de la contraseña-----------#
def calcular_entropia(contrasena):
    """Calcula la entropía de la contraseña en bits."""
    pool = 0
    if any(c.islower() for c in contrasena):
        pool += 26
    if any(c.isupper() for c in contrasena):
        pool += 26
    if any(c.isdigit() for c in contrasena):
        pool += 10
    if any(c in string.punctuation for c in contrasena):
        pool += len(string.punctuation)

    if pool == 0:
        return 0.0

    return len(contrasena) * math.log2(pool)

def clasificar_entropia(bits):
    if bits < 28:
        return "Muy Débil"
    elif bits < 36:
        return "Débil"  
    elif bits < 60:
        return "Media"
    elif bits < 128:
        return "Fuerte"
    return "Muy Fuerte"

#------------Tiempo de crackeo estimado-----------#
SECONDS_PER_YEAR = 60 * 60 * 24 * 365.25
ESCENARIOS_ATAQUE = (
    ("Ataque en línea (100 intentos/s)", 1e2),
    ("Offline, hash rápido (GPU, 10 mil millones/s)", 1e10),
    ("Offline, PBKDF2 con 600 000 iteraciones (~10 mil/s)", 1e4),
)

def cracking_time(entropia):
    """Calcula el tiempo estimado para crackear la contraseña en años."""
    if entropia == 0:
        return "Inmediato"
    
    total_combinaciones = 2 ** entropia
    resultados = []
    for descripcion, intentos_por_segundo in ESCENARIOS_ATAQUE:
        tiempo_segundos = total_combinaciones / intentos_por_segundo
        tiempo_años = tiempo_segundos / SECONDS_PER_YEAR
        resultados.append((descripcion, tiempo_años))
    return resultados

def mostrar_tiempos_crackeo(entropia):
    """Muestra los tiempos estimados para crackear la contraseña."""
    resultados = cracking_time(entropia)
    print("\nTiempos estimados para crackear la contraseña:")
    for descripcion, tiempo_años in resultados:
        if tiempo_años < 1e-6:
            tiempo_str = "Inmediato"
        elif tiempo_años < 1:
            tiempo_str = f"{tiempo_años * 365:.2f} días"
        elif tiempo_años < 10:
            tiempo_str = f"{tiempo_años:.2f} años"
        elif tiempo_años < 1000:
            tiempo_str = f"{tiempo_años:.2f} años"
        else:
            tiempo_str = f"{tiempo_años / 1000:.2f} mil años"
        print(f"- {descripcion}: {tiempo_str}")

#------------generador de contraseñas-----------#
def generar_contrasena_sugerida(longitud=LONGITUD_SUGERIDA):
    alfabeto = string.ascii_letters + string.digits + string.punctuation
    while True:
        candidata = "".join(secrets.choice(alfabeto) for _ in range(longitud))
        if not verificar_contrasena(candidata):
            return candidata
#------------Función para mostrar la contraseña generada-----------#
def mostrar_contrasena_generada():
    """Genera y muestra una contraseña aleatoria al usuario."""
    longitud = input(f"Introduce la longitud deseada para la contraseña (mínimo {LONGITUD_MINIMA}): ")
    try:
        longitud = int(longitud)
        contrasena = generar_contrasena_sugerida(longitud)
        print(f"Contraseña generada: {contrasena}")
    except ValueError:
        print("Por favor, introduce un número válido.")

#------------menu de opciones-----------#
def mostrar_menu():
    """Muestra el menú de opciones al usuario."""
    print("\nOpciones:")
    print("1. Evaluar una contraseña")
    print("2. Generar una contraseña")
    print("3. Salir")

#------------Función principal-----------#
def main():
    """Función principal del programa."""
    print("Bienvenido al Evaluador de Contraseñas")
    while True:
        mostrar_menu()
        opcion = input("Selecciona una opción (1-3): ")
        if opcion == "1":
            contrasena = input("Introduce la contraseña a evaluar: ")
            problemas = verificar_contrasena(contrasena)
            entropia = calcular_entropia(contrasena)
            clasificacion = clasificar_entropia(entropia)

            print(f"\nClasificación de la contraseña: {clasificacion}")
            print(f"Entropía: {entropia:.2f} bits")

            if problemas:
                print("\nProblemas encontrados:")
                for problema, recomendacion in problemas:
                    print(f"- {problema} Recomendación: {recomendacion}")
            else:
                print("La contraseña cumple con todos los criterios de seguridad.")

            mostrar_tiempos_crackeo(entropia)

        elif opcion == "2":
            mostrar_contrasena_generada()
        elif opcion == "3":
            print("Gracias por usar el Evaluador de Contraseñas. ¡Hasta luego!")
            break
        else:
            print("Opción no válida. Por favor, selecciona 1, 2 o 3.")
if __name__ == "__main__":
    main()




