# 🔐 Evaluador de Contraseñas

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![Dependencias](https://img.shields.io/badge/dependencias-ninguna-brightgreen)
![Interfaz](https://img.shields.io/badge/interfaz-consola%20%2B%20tkinter-lightgrey)

Herramienta en Python que **evalúa la fortaleza de una contraseña**, calcula su **entropía**, estima **cuánto tardaría en ser descifrada** en distintos escenarios de ataque y **genera contraseñas seguras** de forma aleatoria. Incluye una versión de consola y una interfaz gráfica con tkinter.

Proyecto educativo de ciberseguridad: sirve para entender por qué algunas contraseñas resisten más que otras y qué influye en ello (longitud, variedad de caracteres y velocidad del atacante).

---

## ✨ Características

- **Verificación de reglas:** longitud mínima, minúsculas, mayúsculas, números, caracteres especiales y detección de contraseñas muy comunes. Cada problema viene con su recomendación.
- **Cálculo de entropía** en bits y clasificación en cinco niveles: Muy Débil, Débil, Media, Fuerte y Muy Fuerte.
- **Estimación del tiempo de crackeo** en tres escenarios:
  | Escenario | Velocidad |
  |---|---|
  | Ataque en línea | 100 intentos/s |
  | Offline, hash rápido (GPU) | 10 000 millones de intentos/s |
  | Offline, PBKDF2 con 600 000 iteraciones | ~10 000 intentos/s |
- **Generador seguro** con el módulo `secrets` (aleatoriedad apta para criptografía), que solo devuelve contraseñas que cumplen todas las reglas.
- **Interfaz gráfica** con evaluación en tiempo real, barra de entropía por colores, generador y botón de copiar.
- **Sin dependencias externas:** solo usa la biblioteca estándar de Python.

---

## 📁 Estructura del proyecto

```
.
├── main.py        # Lógica del programa + interfaz de consola
├── interfaz.py    # Interfaz gráfica (tkinter), reutiliza las funciones de main.py
└── README.md
```

---

## Programa de Evaluación de Contraseñas

Programa en Python que evalúa la seguridad de contraseñas mediante el uso de variables, estructuras condicionales y lógica de programación, integrando criterios básicos de ciberseguridad para concientizar sobre el uso de credenciales robustas y afianzar los fundamentos del desarrollo de software.

## 🖥️ Uso

### Versión de consola

```bash
python main.py
```

Menú de opciones:

```
Opciones:
1. Evaluar una contraseña
2. Generar una contraseña
3. Salir
```

Ejemplo de evaluación con `Abc123!x`:

```
Clasificación de la contraseña: Media
Entropía: 52.44 bits

La contraseña cumple con todos los criterios de seguridad.

Tiempos estimados para crackear la contraseña:
- Ataque en línea (100 intentos/s): 1931.56 mil años
- Offline, hash rápido (GPU, 10 mil millones/s): 7.05 días
- Offline, PBKDF2 con 600 000 iteraciones (~10 mil/s): 19.32 mil años
```

### Versión gráfica

```bash
python interfaz.py
```

- Escribe la contraseña y el resultado se actualiza al instante.
- Marca "Mostrar contraseña" para ver lo que escribes.
- Usa el generador para crear una contraseña, copiarla o enviarla al campo de evaluación.
- El menú **Entropía → Ver escala de entropía** muestra los rangos de clasificación.

> Captura de pantalla: agrega aquí una imagen de la interfaz, por ejemplo `![Interfaz](docs/captura.png)`.

---

## 🧠 ¿Cómo funciona?

### Entropía

La entropía estima cuántas combinaciones tendría que probar un atacante:

```
H = L × log2(N)
```

donde `L` es la longitud de la contraseña y `N` el tamaño del conjunto de caracteres usados:

| Grupo presente | Aporta al conjunto |
|---|---|
| Minúsculas | 26 |
| Mayúsculas | 26 |
| Dígitos | 10 |
| Símbolos | 32 |

Por ejemplo, `Abc123!x` usa los cuatro grupos (N = 94) y tiene 8 caracteres: `8 × log2(94) ≈ 52.44 bits`.

### Clasificación

| Entropía | Nivel |
|---|---|
| < 28 bits | Muy Débil |
| 28 a 35 bits | Débil |
| 36 a 59 bits | Media |
| 60 a 127 bits | Fuerte |
| ≥ 128 bits | Muy Fuerte |

### Tiempo de crackeo

Se calcula el peor caso, probando todas las combinaciones (`2^entropía`), dividido entre los intentos por segundo de cada escenario. El mismo password puede resistir años contra un ataque en línea y caer en días si la base de datos se filtra con hashes rápidos; por eso se muestran los tres escenarios.

---

## 📚 Funciones principales (`main.py`)

| Función | Descripción |
|---|---|
| `verificar_contrasena(contrasena)` | Devuelve una lista de `(problema, recomendación)`; vacía si cumple todas las reglas. |
| `calcular_entropia(contrasena)` | Entropía en bits. |
| `clasificar_entropia(bits)` | Nivel de fortaleza como texto. |
| `cracking_time(entropia)` | Tiempos estimados en años por escenario. |
| `mostrar_tiempos_crackeo(entropia)` | Imprime los tiempos en formato legible. |
| `generar_contrasena_sugerida(longitud)` | Contraseña aleatoria que cumple todas las reglas. |

## ⚠️ Limitaciones

- La entropía asume que los caracteres se eligieron **al azar**. Claves predecibles como `Password1!` obtienen una puntuación alta aunque sean débiles.
- La lista de contraseñas comunes es pequeña (demostrativa).
- Los tiempos de crackeo son **estimaciones teóricas** de fuerza bruta, no una garantía de seguridad.
- La contraseña evaluada no se almacena ni se envía a ningún sitio: todo se procesa localmente.

## 🛠️ Mejoras futuras

- [ ] Cargar una lista externa de contraseñas filtradas.
- [ ] Detectar patrones: secuencias (`1234`, `abcd`), repeticiones y teclados (`qwerty`).
- [ ] Validar la longitud mínima dentro de `generar_contrasena_sugerida`.
- [ ] Proteger `cracking_time` contra desbordamiento con entropías muy altas.
- [ ] Tema oscuro en la interfaz gráfica.
- [ ] Pruebas unitarias con `unittest` o `pytest`.

## 👤 Autor

Kevin Valente  
GitHub: [@tu-usuario](https://github.com/KevinV676)
