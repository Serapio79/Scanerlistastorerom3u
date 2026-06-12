import os
import sys
import time
import random
import string
import math

# =========================
# COLORES PASTEL
# =========================
class ColoresDrako:
    PRINCIPAL = "\033[38;5;147m"
    SECUNDARIO = "\033[38;5;181m"
    EXITO = "\033[38;5;151m"
    ALERTA = "\033[38;5;217m"
    TEXTO = "\033[38;5;250m"
    RESET = "\033[0m"


# =========================
# CONFIG
# =========================
RUTA_BASE = "/sdcard/combo/"
SIMBOLOS = "@#!*"
TAMANO_MAXIMO_ARCHIVO = 50 * 1024 * 1024  # 50 MB en bytes

CARACTERES = {
    "1": string.digits,
    "2": string.digits + SIMBOLOS,
    "3": string.ascii_lowercase,
    "4": string.ascii_uppercase,
    "5": string.ascii_letters,
    "6": string.ascii_lowercase + string.digits,
    "7": string.ascii_uppercase + string.digits,
    "8": string.ascii_letters + string.digits,
    "9": string.ascii_letters + string.digits + SIMBOLOS,
}


# =========================
# UTILIDADES
# =========================
def clearConsole():
    os.system("cls" if os.name == "nt" else "clear")


def imprimir_titulo(texto):
    for char in texto:
        sys.stdout.write(
            f"{ColoresDrako.PRINCIPAL}{char}{ColoresDrako.RESET}"
        )
        sys.stdout.flush()
        time.sleep(0.003)
    print()


def linea():
    print(
        f"{ColoresDrako.PRINCIPAL}"
        f"─────────────────────────────"
        f"{ColoresDrako.RESET}"
    )


def obtener_nombre():
    n = 1
    while True:
        ruta = f"{RUTA_BASE}Drako_combo_{str(n).zfill(3)}.txt"
        if not os.path.exists(ruta):
            return ruta
        n += 1


def obtener_nombre_parte(base_ruta, parte):
    """Genera nombre para archivo parte N"""
    dir_name = os.path.dirname(base_ruta)
    base_name = os.path.basename(base_ruta)
    name, ext = os.path.splitext(base_name)
    return f"{dir_name}/{name}_parte{str(parte).zfill(3)}{ext}"


def generar_unico(minimo, maximo, chars, usados):
    while True:
        largo = random.randint(minimo, maximo)
        valor = ''.join(random.choices(chars, k=largo))
        if valor not in usados:
            usados.add(valor)
            return valor


def barra_progreso(actual, total, ancho=10):
    """Dibuja una barra de progreso"""
    if total == 0:
        return "[██████████] 100%"
    porcentaje = actual / total
    lleno = int(ancho * porcentaje)
    vacio = ancho - lleno
    barra = "█" * lleno + "░" * vacio
    return f"[{barra}] {int(porcentaje * 100)}%"


def formatear_numero(n):
    """Formatea numeros grandes con separadores"""
    return f"{n:,}".replace(",", ".")


def calcular_tamano_estimado(cantidad, longitud_promedio):
    """Estima tamano en bytes de un archivo de combos"""
    # usuario:password\n = longitud_promedio*2 + 2
    return cantidad * (longitud_promedio * 2 + 2)


# =========================
# MENUS
# =========================
def menu_principal():
    while True:
        linea()

        print(
            f"{ColoresDrako.TEXTO}["
            f"{ColoresDrako.PRINCIPAL} 1 "
            f"{ColoresDrako.TEXTO}] "
            f"{ColoresDrako.SECUNDARIO}➟ "
            f"{ColoresDrako.TEXTO}Usuario unico"
        )

        print(
            f"{ColoresDrako.TEXTO}["
            f"{ColoresDrako.PRINCIPAL} 2 "
            f"{ColoresDrako.TEXTO}] "
            f"{ColoresDrako.SECUNDARIO}➟ "
            f"{ColoresDrako.TEXTO}Usuario y contraseña"
        )

        linea()

        opcion = input(
            f"{ColoresDrako.EXITO}"
            f"Selecciona opcion (1-2): "
            f"{ColoresDrako.RESET}"
        ).strip()

        if opcion in ("1", "2"):
            return opcion

        print(
            f"{ColoresDrako.ALERTA}"
            f"[!] Opcion invalida. Ingresa 1 o 2."
            f"{ColoresDrako.RESET}"
        )


def menu_tipo(nombre):
    nombres = [
        "Solo numeros",
        "Numeros y simbolos",
        "Letras min",
        "Letras mayus",
        "Letras min y may",
        "Letras min y num",
        "Letras may y num",
        "Letras min may num",
        "Todo mezclado"
    ]

    while True:
        linea()

        for i, txt in enumerate(nombres, 1):
            print(
                f"{ColoresDrako.TEXTO}[{ColoresDrako.PRINCIPAL}{i}{ColoresDrako.TEXTO}] "
                f"{ColoresDrako.SECUNDARIO}➟ {ColoresDrako.TEXTO}{txt}"
            )

        linea()

        opcion = input(
            f"{ColoresDrako.EXITO}Tipo para {nombre}: {ColoresDrako.RESET}"
        ).strip()

        if opcion in CARACTERES:
            return opcion

        print(
            f"{ColoresDrako.ALERTA}[!] Tipo invalido. Ingresa un numero del 1 al 9.{ColoresDrako.RESET}"
        )


def menu_modo_visualizacion():
    """Pregunta si quiere modo silencioso o verbose"""
    linea()
    print(
        f"{ColoresDrako.TEXTO}["
        f"{ColoresDrako.PRINCIPAL} 1 "
        f"{ColoresDrako.TEXTO}] "
        f"{ColoresDrako.SECUNDARIO}➟ "
        f"{ColoresDrako.TEXTO}Mostrar cada combo (verbose)"
    )
    print(
        f"{ColoresDrako.TEXTO}["
        f"{ColoresDrako.PRINCIPAL} 2 "
        f"{ColoresDrako.TEXTO}] "
        f"{ColoresDrako.SECUNDARIO}➟ "
        f"{ColoresDrako.TEXTO}Solo barra de progreso (silencioso)"
    )
    linea()

    while True:
        opcion = input(
            f"{ColoresDrako.EXITO}"
            f"Modo de visualizacion: "
            f"{ColoresDrako.RESET}"
        ).strip()

        if opcion == "1":
            return True   # verbose
        elif opcion == "2":
            return False  # silencioso

        print(
            f"{ColoresDrako.ALERTA}"
            f"[!] Opcion invalida. Ingresa 1 o 2."
            f"{ColoresDrako.RESET}"
        )


# =========================
# GENERAR: USUARIO UNICO
# =========================
def generar_usuario_unico():
    linea()
    print(
        f"{ColoresDrako.TEXTO}"
        f"Modo de ingreso de usuarios:"
        f"{ColoresDrako.RESET}"
    )
    print(
        f"{ColoresDrako.TEXTO}["
        f"{ColoresDrako.PRINCIPAL} 1 "
        f"{ColoresDrako.TEXTO}] "
        f"{ColoresDrako.SECUNDARIO}➟ "
        f"{ColoresDrako.TEXTO}Ingresar usuarios manualmente"
    )
    print(
        f"{ColoresDrako.TEXTO}["
        f"{ColoresDrako.PRINCIPAL} 2 "
        f"{ColoresDrako.TEXTO}] "
        f"{ColoresDrako.SECUNDARIO}➟ "
        f"{ColoresDrako.TEXTO}Cargar desde archivo"
    )
    linea()

    while True:
        modo_usuarios = input(
            f"{ColoresDrako.EXITO}"
            f"Selecciona opcion (1-2): "
            f"{ColoresDrako.RESET}"
        ).strip()
        if modo_usuarios in ("1", "2"):
            break
        print(
            f"{ColoresDrako.ALERTA}"
            f"[!] Opcion invalida. Ingresa 1 o 2."
            f"{ColoresDrako.RESET}"
        )

    lista_usuarios = []

    if modo_usuarios == "1":
        print()
        print(
            f"{ColoresDrako.TEXTO}"
            f"Ingresa los usuarios separados por coma o espacio."
            f"{ColoresDrako.RESET}"
        )
        print(
            f"{ColoresDrako.TEXTO}"
            f"Ejemplo: usuario1, usuario2, usuario3"
            f"{ColoresDrako.RESET}"
        )
        entrada = input(
            f"{ColoresDrako.EXITO}"
            f"Usuarios: "
            f"{ColoresDrako.RESET}"
        )
        # Separar por coma, espacio, o salto de línea
        for separador in [',', ' ', ';', '\n']:
            if separador in entrada:
                lista_usuarios = [u.strip() for u in entrada.split(separador) if u.strip()]
                break
        if not lista_usuarios:
            lista_usuarios = [entrada.strip()]
    else:
        print()
        print(
            f"{ColoresDrako.TEXTO}"
            f"Archivos en {RUTA_BASE}:"
            f"{ColoresDrako.RESET}"
        )
        # Listar archivos .txt en RUTA_BASE
        try:
            archivos = [f for f in os.listdir(RUTA_BASE) if f.endswith('.txt')]
            if archivos:
                for i, arch in enumerate(archivos, 1):
                    print(
                        f"{ColoresDrako.TEXTO}[{ColoresDrako.PRINCIPAL}{i}{ColoresDrako.TEXTO}] "
                        f"{ColoresDrako.SECUNDARIO}➟ {ColoresDrako.TEXTO}{arch}"
                    )
            else:
                print(
                    f"{ColoresDrako.ALERTA}"
                    f"  No hay archivos .txt en la carpeta"
                    f"{ColoresDrako.RESET}"
                )
        except Exception:
            print(
                f"{ColoresDrako.ALERTA}"
                f"  No se pudo listar archivos"
                f"{ColoresDrako.RESET}"
            )

        ruta_input = input(
            f"{ColoresDrako.EXITO}"
            f"Numero o nombre del archivo: "
            f"{ColoresDrako.RESET}"
        ).strip()

        # Si ingreso un numero, seleccionar de la lista
        try:
            num_seleccion = int(ruta_input)
            if 1 <= num_seleccion <= len(archivos):
                ruta_archivo = os.path.join(RUTA_BASE, archivos[num_seleccion - 1])
            else:
                print(
                    f"{ColoresDrako.ALERTA}"
                    f"[!] Numero invalido. Debe ser entre 1 y {len(archivos)}."
                    f"{ColoresDrako.RESET}"
                )
                return None
        except ValueError:
            # No es numero, tratar como nombre de archivo
            if not ruta_input.startswith('/'):
                ruta_archivo = os.path.join(RUTA_BASE, ruta_input)
            else:
                ruta_archivo = ruta_input
        try:
            with open(ruta_archivo, "r", encoding="utf-8") as f:
                for linea_archivo in f:
                    usuario = linea_archivo.strip()
                    if usuario and ':' not in usuario:
                        lista_usuarios.append(usuario)
                    elif usuario and ':' in usuario:
                        # Si tiene formato usuario:password, solo tomar usuario
                        lista_usuarios.append(usuario.split(':')[0].strip())
            print(
                f"{ColoresDrako.EXITO}"
                f"Cargados {len(lista_usuarios)} usuarios."
                f"{ColoresDrako.RESET}"
            )
        except FileNotFoundError:
            print(
                f"{ColoresDrako.ALERTA}"
                f"[!] Archivo no encontrado: {ruta_archivo}"
                f"{ColoresDrako.RESET}"
            )
            return None
        except Exception as e:
            print(
                f"{ColoresDrako.ALERTA}"
                f"[!] Error al leer archivo: {e}"
                f"{ColoresDrako.RESET}"
            )
            return None

    if not lista_usuarios:
        print(
            f"{ColoresDrako.ALERTA}"
            f"[!] No se ingresaron usuarios."
            f"{ColoresDrako.RESET}"
        )
        return None

    # Eliminar duplicados manteniendo orden
    usuarios_unicos = []
    vistos = set()
    for u in lista_usuarios:
        if u not in vistos:
            vistos.add(u)
            usuarios_unicos.append(u)
    lista_usuarios = usuarios_unicos

    print()
    print(
        f"{ColoresDrako.EXITO}"
        f"Usuarios cargados: {len(lista_usuarios)}"
        f"{ColoresDrako.RESET}"
    )
    for i, u in enumerate(lista_usuarios[:5], 1):
        print(
            f"{ColoresDrako.TEXTO}"
            f"[{i}] {u}"
            f"{ColoresDrako.RESET}"
        )
    if len(lista_usuarios) > 5:
        print(
            f"{ColoresDrako.TEXTO}"
            f"... y {len(lista_usuarios) - 5} mas"
            f"{ColoresDrako.RESET}"
        )

    while True:
        try:
            cantidad_input = input(
                f"{ColoresDrako.EXITO}"
                f"\nCantidad de contraseñas (0 = todas las posibles) \n{ColoresDrako.PRINCIPAL}>> "
                f"{ColoresDrako.RESET}"
            ).strip()
            cantidad = int(cantidad_input)
            if cantidad >= 0:
                break
            print(
                f"{ColoresDrako.ALERTA}"
                f"[!] La cantidad no puede ser negativa."
                f"{ColoresDrako.RESET}"
            )
        except ValueError:
            print(
                f"{ColoresDrako.ALERTA}"
                f"[!] Ingresa un numero valido."
                f"{ColoresDrako.RESET}"
            )

    tipo_pass = menu_tipo("contraseña")

    while True:
        try:
            min_p = int(input(
                f"{ColoresDrako.TEXTO}"
                f"Longitud minima: "
                f"{ColoresDrako.RESET}"
            ))
            if min_p > 0:
                break
            print(
                f"{ColoresDrako.ALERTA}"
                f"[!] La longitud minima debe ser mayor a 0."
                f"{ColoresDrako.RESET}"
            )
        except ValueError:
            print(
                f"{ColoresDrako.ALERTA}"
                f"[!] Ingresa un numero valido."
                f"{ColoresDrako.RESET}"
            )

    while True:
        try:
            max_p = int(input(
                f"{ColoresDrako.TEXTO}"
                f"Longitud maxima: "
                f"{ColoresDrako.RESET}"
            ))
            if max_p >= min_p:
                break
            print(
                f"{ColoresDrako.ALERTA}"
                f"[!] La longitud maxima debe ser igual o mayor a la minima ({min_p})."
                f"{ColoresDrako.RESET}"
            )
        except ValueError:
            print(
                f"{ColoresDrako.ALERTA}"
                f"[!] Ingresa un numero valido."
                f"{ColoresDrako.RESET}"
            )

    verbose = menu_modo_visualizacion()

    ruta_base = obtener_nombre()
    chars = CARACTERES[tipo_pass]

    # Calcular combinaciones posibles
    total_combinaciones = 0
    for longitud in range(min_p, max_p + 1):
        total_combinaciones += len(chars) ** longitud

    cantidad_por_usuario = total_combinaciones if cantidad == 0 else cantidad
    cantidad_objetivo = len(lista_usuarios) * cantidad_por_usuario

    # Estimar tamano
    longitud_promedio = (min_p + max_p) // 2
    tamano_estimado = cantidad_objetivo * (longitud_promedio + len(max(lista_usuarios, key=len)) + 2)
    dividir = tamano_estimado > TAMANO_MAXIMO_ARCHIVO
    num_partes_estimado = math.ceil(tamano_estimado / TAMANO_MAXIMO_ARCHIVO) if dividir else 1

    print()
    linea()
    print(
        f"{ColoresDrako.TEXTO}"
        f"Resumen de generacion:"
        f"{ColoresDrako.RESET}"
    )
    print(
        f"{ColoresDrako.TEXTO}"
        f"Usuarios: {formatear_numero(len(lista_usuarios))}"
        f"{ColoresDrako.RESET}"
    )
    print(
        f"{ColoresDrako.TEXTO}"
        f"Passwords por usuario: {formatear_numero(cantidad_por_usuario)}"
        f"{ColoresDrako.RESET}"
    )
    print(
        f"{ColoresDrako.TEXTO}"
        f"Combos totales: {formatear_numero(cantidad_objetivo)}"
        f"{ColoresDrako.RESET}"
    )
    print(
        f"{ColoresDrako.TEXTO}"
        f"Tamano estimado: ~{formatear_numero(tamano_estimado)} bytes ({tamano_estimado / (1024*1024):.1f} MB)"
        f"{ColoresDrako.RESET}"
    )
    if dividir:
        print(
            f"{ColoresDrako.EXITO}"
            f"Se dividira en {num_partes_estimado} archivo(s) de ~50MB"
            f"{ColoresDrako.RESET}"
        )
    linea()
    print()

    print(
        f"{ColoresDrako.EXITO}"
        f"Generando y guardando..."
        f"{ColoresDrako.RESET}"
    )
    print()

    generados = 0
    parte_actual = 1
    tamano_actual = 0
    buffer_escritura = []
    TAMANO_BUFFER = 1000

    ruta_actual = obtener_nombre_parte(ruta_base, parte_actual)
    archivo = open(ruta_actual, "w", encoding="utf-8")
    archivos_creados = [ruta_actual]
    tiempo_inicio = time.time()
    ultima_barra = tiempo_inicio

    try:
        for usuario in lista_usuarios:
            usadas = set()
            for _ in range(cantidad_por_usuario):
                if len(usadas) >= total_combinaciones:
                    break

                password = generar_unico(min_p, max_p, chars, usadas)
                registro = f"{usuario}:{password}\n"
                registro_bytes = len(registro.encode('utf-8'))

                if dividir and tamano_actual + registro_bytes > TAMANO_MAXIMO_ARCHIVO:
                    if buffer_escritura:
                        archivo.write(''.join(buffer_escritura))
                        buffer_escritura = []
                    archivo.close()
                    parte_actual += 1
                    ruta_actual = obtener_nombre_parte(ruta_base, parte_actual)
                    archivo = open(ruta_actual, "w", encoding="utf-8")
                    archivos_creados.append(ruta_actual)
                    tamano_actual = 0

                buffer_escritura.append(registro)
                tamano_actual += registro_bytes
                generados += 1

                if len(buffer_escritura) >= TAMANO_BUFFER:
                    archivo.write(''.join(buffer_escritura))
                    buffer_escritura = []

                ahora = time.time()
                if generados % 500 == 0 or (ahora - ultima_barra >= 1.0) or generados == cantidad_objetivo:
                    if not verbose:
                        barra_texto = barra_progreso(generados, cantidad_objetivo)
                        tiempo_transcurrido = ahora - tiempo_inicio
                        cpm = int(generados / (tiempo_transcurrido / 60)) if tiempo_transcurrido > 0 else 0
                        texto_salida = (
                            ColoresDrako.EXITO + barra_texto + " | " +
                            formatear_numero(generados) + "/" + formatear_numero(cantidad_objetivo) + " | " +
                            "CPM: " + formatear_numero(cpm) + ColoresDrako.RESET
                        )
                        sys.stdout.write("\r" + texto_salida)
                        sys.stdout.flush()
                        ultima_barra = ahora
                    else:
                        if generados % 100 == 0:
                            print(
                                f"{ColoresDrako.TEXTO}"
                                f"{usuario}:{password}"
                                f"{ColoresDrako.RESET}"
                            )

    except KeyboardInterrupt:
        print()
        print(
            f"{ColoresDrako.ALERTA}"
            f"[!] Generacion interrumpida por el usuario."
            f"{ColoresDrako.RESET}"
        )
    finally:
        if buffer_escritura:
            archivo.write(''.join(buffer_escritura))
        archivo.close()

    if not verbose:
        print()

    tiempo_total = time.time() - tiempo_inicio
    cpm_final = int(generados / (tiempo_total / 60)) if tiempo_total > 0 else 0

    print()
    linea()
    print(
        f"{ColoresDrako.EXITO}"
        f"Combos generados: {formatear_numero(generados)}"
        f"{ColoresDrako.RESET}"
    )
    print(
        f"{ColoresDrako.TEXTO}"
        f"Tiempo: {tiempo_total:.2f}s | CPM: {formatear_numero(cpm_final)}"
        f"{ColoresDrako.RESET}"
    )
    if len(archivos_creados) == 1:
        print(
            f"{ColoresDrako.TEXTO}"
            f"Archivo: {archivos_creados[0]}"
            f"{ColoresDrako.RESET}"
        )
    else:
        print(
            f"{ColoresDrako.TEXTO}"
            f"Archivos ({len(archivos_creados)} partes):"
            f"{ColoresDrako.RESET}"
        )
        for arch in archivos_creados:
            print(
                f"{ColoresDrako.TEXTO}"
                f"    - {arch}"
                f"{ColoresDrako.RESET}"
            )

    return archivos_creados[0] if archivos_creados else ruta_base



def generar_usuario_y_pass():
    while True:
        try:
            cantidad_input = input(
                f"{ColoresDrako.TEXTO}Cantidad de combos (0 = todas las posibles) \n{ColoresDrako.PRINCIPAL}>> "
                f"{ColoresDrako.RESET}"
            ).strip()
            cantidad = int(cantidad_input)
            if cantidad >= 0:
                break
            print(
                f"{ColoresDrako.ALERTA}"
                f"[!] La cantidad no puede ser negativa."
                f"{ColoresDrako.RESET}"
            )
        except ValueError:
            print(
                f"{ColoresDrako.ALERTA}"
                f"[!] Ingresa un numero valido."
                f"{ColoresDrako.RESET}"
            )

    print()
    print(f"{ColoresDrako.TEXTO}CONFIGURACION USUARIO")
    tipo_user = menu_tipo("usuario")

    while True:
        try:
            min_u = int(input(f"{ColoresDrako.TEXTO}Longitud minima usuario: "))
            if min_u > 0:
                break
            print(
                f"{ColoresDrako.ALERTA}"
                f"[!] La longitud minima debe ser mayor a 0."
                f"{ColoresDrako.RESET}"
            )
        except ValueError:
            print(
                f"{ColoresDrako.ALERTA}"
                f"[!] Ingresa un numero valido."
                f"{ColoresDrako.RESET}"
            )

    while True:
        try:
            max_u = int(input(f"{ColoresDrako.TEXTO}Longitud maxima usuario: "))
            if max_u >= min_u:
                break
            print(
                f"{ColoresDrako.ALERTA}"
                f"[!] La longitud maxima debe ser igual o mayor a la minima ({min_u})."
                f"{ColoresDrako.RESET}"
            )
        except ValueError:
            print(
                f"{ColoresDrako.ALERTA}"
                f"[!] Ingresa un numero valido."
                f"{ColoresDrako.RESET}"
            )

    print()
    print(f"{ColoresDrako.TEXTO}CONFIGURACION CONTRASENA")
    tipo_pass = menu_tipo("contraseña")

    while True:
        try:
            min_p = int(input(f"{ColoresDrako.TEXTO}Longitud minima contraseña: "))
            if min_p > 0:
                break
            print(
                f"{ColoresDrako.ALERTA}"
                f"[!] La longitud minima debe ser mayor a 0."
                f"{ColoresDrako.RESET}"
            )
        except ValueError:
            print(
                f"{ColoresDrako.ALERTA}"
                f"[!] Ingresa un numero valido."
                f"{ColoresDrako.RESET}"
            )

    while True:
        try:
            max_p = int(input(f"{ColoresDrako.TEXTO}Longitud maxima contraseña: "))
            if max_p >= min_p:
                break
            print(
                f"{ColoresDrako.ALERTA}"
                f"[!] La longitud maxima debe ser igual o mayor a la minima ({min_p})."
                f"{ColoresDrako.RESET}"
            )
        except ValueError:
            print(
                f"{ColoresDrako.ALERTA}"
                f"[!] Ingresa un numero valido."
                f"{ColoresDrako.RESET}"
            )

    verbose = menu_modo_visualizacion()

    ruta_base = obtener_nombre()

    chars_user = CARACTERES[tipo_user]
    chars_pass = CARACTERES[tipo_pass]

    # Generar TODOS los usuarios posibles
    print()
    print(
        f"{ColoresDrako.EXITO}"
        f"Generando lista de usuarios posibles..."
        f"{ColoresDrako.RESET}"
    )

    todos_usuarios = []
    usuarios_generados = 0
    usuarios_usados = set()
    total_combos_user = 0
    for longitud in range(min_u, max_u + 1):
        total_combos_user += len(chars_user) ** longitud

    # Generar todos los usuarios únicos
    while len(usuarios_usados) < total_combos_user:
        usuario = generar_unico(min_u, max_u, chars_user, usuarios_usados)
        todos_usuarios.append(usuario)
        usuarios_generados += 1
        if usuarios_generados % 10000 == 0:
            texto_prog = ColoresDrako.TEXTO + "Usuarios generados: " + formatear_numero(usuarios_generados) + "/" + formatear_numero(total_combos_user) + ColoresDrako.RESET
            sys.stdout.write("\r" + texto_prog)
            sys.stdout.flush()

    print()
    print(
        f"{ColoresDrako.EXITO}"
        f"Total usuarios: {formatear_numero(len(todos_usuarios))}"
        f"{ColoresDrako.RESET}"
    )

    # Generar TODAS las passwords posibles
    print(
        f"{ColoresDrako.EXITO}"
        f"Generando lista de passwords posibles..."
        f"{ColoresDrako.RESET}"
    )

    todas_passwords = []
    passwords_generadas = 0
    passwords_usadas = set()
    total_combos_pass = 0
    for longitud in range(min_p, max_p + 1):
        total_combos_pass += len(chars_pass) ** longitud

    # Generar todas las passwords únicas
    while len(passwords_usadas) < total_combos_pass:
        password = generar_unico(min_p, max_p, chars_pass, passwords_usadas)
        todas_passwords.append(password)
        passwords_generadas += 1
        if passwords_generadas % 10000 == 0:
            texto_prog = ColoresDrako.TEXTO + "Passwords generadas: " + formatear_numero(passwords_generadas) + "/" + formatear_numero(total_combos_pass) + ColoresDrako.RESET
            sys.stdout.write("\r" + texto_prog)
            sys.stdout.flush()

    print()
    print(
        f"{ColoresDrako.EXITO}"
        f"Total passwords: {formatear_numero(len(todas_passwords))}"
        f"{ColoresDrako.RESET}"
    )

    # Calcular total de combinaciones
    total_combinaciones = len(todos_usuarios) * len(todas_passwords)
    cantidad_objetivo = total_combinaciones if cantidad == 0 else min(cantidad, total_combinaciones)

    # Mezclar usuarios y passwords
    print(
        f"{ColoresDrako.EXITO}"
        f"Mezclando..."
        f"{ColoresDrako.RESET}"
    )
    random.shuffle(todos_usuarios)
    random.shuffle(todas_passwords)

    # Estimar tamano
    longitud_promedio = ((min_u + max_u) // 2) + ((min_p + max_p) // 2) + 1
    tamano_estimado = cantidad_objetivo * (longitud_promedio + 1)
    dividir = tamano_estimado > TAMANO_MAXIMO_ARCHIVO
    num_partes_estimado = math.ceil(tamano_estimado / TAMANO_MAXIMO_ARCHIVO) if dividir else 1

    print()
    linea()
    print(
        f"{ColoresDrako.TEXTO}"
        f"Resumen de generacion:"
        f"{ColoresDrako.RESET}"
    )
    print(
        f"{ColoresDrako.TEXTO}"
        f"Usuarios: {formatear_numero(len(todos_usuarios))}"
        f"{ColoresDrako.RESET}"
    )
    print(
        f"{ColoresDrako.TEXTO}"
        f"Passwords: {formatear_numero(len(todas_passwords))}"
        f"{ColoresDrako.RESET}"
    )
    print(
        f"{ColoresDrako.TEXTO}"
        f"Combinaciones totales: {formatear_numero(total_combinaciones)}"
        f"{ColoresDrako.RESET}"
    )
    print(
        f"{ColoresDrako.TEXTO}"
        f"Combos a generar: {formatear_numero(cantidad_objetivo)}"
        f"{ColoresDrako.RESET}"
    )
    print(
        f"{ColoresDrako.TEXTO}"
        f"Tamano estimado: ~{formatear_numero(tamano_estimado)} bytes ({tamano_estimado / (1024*1024):.1f} MB)"
        f"{ColoresDrako.RESET}"
    )
    if dividir:
        print(
            f"{ColoresDrako.EXITO}"
            f"Se dividira en {num_partes_estimado} archivo(s) de ~50MB"
            f"{ColoresDrako.RESET}"
        )
    linea()
    print()

    print(
        f"{ColoresDrako.EXITO}"
        f"Generando y guardando combos mezclados..."
        f"{ColoresDrako.RESET}"
    )
    print()

    generados = 0
    parte_actual = 1
    tamano_actual = 0
    buffer_escritura = []
    TAMANO_BUFFER = 1000

    ruta_actual = obtener_nombre_parte(ruta_base, parte_actual)
    archivo = open(ruta_actual, "w", encoding="utf-8")
    archivos_creados = [ruta_actual]
    tiempo_inicio = time.time()
    ultima_barra = tiempo_inicio

    # Generar combos mezclados: para cada usuario, recorrer passwords en orden aleatorio
    # Pero mezclando el orden de aparición
    try:
        # Crear índices mezclados para recorrer en orden aleatorio
        indices_usuarios = list(range(len(todos_usuarios)))
        indices_passwords = list(range(len(todas_passwords)))

        # Si la cantidad es menor que el total, seleccionar posiciones aleatorias
        if cantidad_objetivo < total_combinaciones:
            # Generar pares (usuario_idx, password_idx) aleatorios
            combos_generados = set()
            while generados < cantidad_objetivo:
                u_idx = random.choice(indices_usuarios)
                p_idx = random.choice(indices_passwords)
                par = (u_idx, p_idx)
                if par in combos_generados:
                    continue
                combos_generados.add(par)

                usuario = todos_usuarios[u_idx]
                password = todas_passwords[p_idx]
                registro = f"{usuario}:{password}\n"
                registro_bytes = len(registro.encode('utf-8'))

                if dividir and tamano_actual + registro_bytes > TAMANO_MAXIMO_ARCHIVO:
                    if buffer_escritura:
                        archivo.write(''.join(buffer_escritura))
                        buffer_escritura = []
                    archivo.close()
                    parte_actual += 1
                    ruta_actual = obtener_nombre_parte(ruta_base, parte_actual)
                    archivo = open(ruta_actual, "w", encoding="utf-8")
                    archivos_creados.append(ruta_actual)
                    tamano_actual = 0

                buffer_escritura.append(registro)
                tamano_actual += registro_bytes
                generados += 1

                if len(buffer_escritura) >= TAMANO_BUFFER:
                    archivo.write(''.join(buffer_escritura))
                    buffer_escritura = []

                ahora = time.time()
                if generados % 500 == 0 or (ahora - ultima_barra >= 1.0) or generados == cantidad_objetivo:
                    if not verbose:
                        barra_texto = barra_progreso(generados, cantidad_objetivo)
                        tiempo_transcurrido = ahora - tiempo_inicio
                        cpm = int(generados / (tiempo_transcurrido / 60)) if tiempo_transcurrido > 0 else 0
                        texto_salida = (
                            ColoresDrako.EXITO + barra_texto + " | " +
                            formatear_numero(generados) + "/" + formatear_numero(cantidad_objetivo) + " | " +
                            "CPM: " + formatear_numero(cpm) + ColoresDrako.RESET
                        )
                        sys.stdout.write("\r" + texto_salida)
                        sys.stdout.flush()
                        ultima_barra = ahora
                    else:
                        if generados % 100 == 0:
                            print(
                                f"{ColoresDrako.TEXTO}"
                                f"{usuario}:{password}"
                                f"{ColoresDrako.RESET}"
                            )
        else:
            # Generar TODAS las combinaciones en orden mezclado
            # Recorrer usuarios mezclados, y para cada uno, passwords mezcladas
            for u_idx in indices_usuarios:
                usuario = todos_usuarios[u_idx]
                for p_idx in indices_passwords:
                    password = todas_passwords[p_idx]
                    registro = f"{usuario}:{password}\n"
                    registro_bytes = len(registro.encode('utf-8'))

                    if dividir and tamano_actual + registro_bytes > TAMANO_MAXIMO_ARCHIVO:
                        if buffer_escritura:
                            archivo.write(''.join(buffer_escritura))
                            buffer_escritura = []
                        archivo.close()
                        parte_actual += 1
                        ruta_actual = obtener_nombre_parte(ruta_base, parte_actual)
                        archivo = open(ruta_actual, "w", encoding="utf-8")
                        archivos_creados.append(ruta_actual)
                        tamano_actual = 0

                    buffer_escritura.append(registro)
                    tamano_actual += registro_bytes
                    generados += 1

                    if len(buffer_escritura) >= TAMANO_BUFFER:
                        archivo.write(''.join(buffer_escritura))
                        buffer_escritura = []

                    ahora = time.time()
                    if generados % 500 == 0 or (ahora - ultima_barra >= 1.0):
                        if not verbose:
                            barra_texto = barra_progreso(generados, cantidad_objetivo)
                            tiempo_transcurrido = ahora - tiempo_inicio
                            cpm = int(generados / (tiempo_transcurrido / 60)) if tiempo_transcurrido > 0 else 0
                            texto_salida = (
                                ColoresDrako.EXITO + barra_texto + " | " +
                                formatear_numero(generados) + "/" + formatear_numero(cantidad_objetivo) + " | " +
                                "CPM: " + formatear_numero(cpm) + ColoresDrako.RESET
                            )
                            sys.stdout.write("\r" + texto_salida)
                            sys.stdout.flush()
                            ultima_barra = ahora
                        else:
                            if generados % 100 == 0:
                                print(
                                    f"{ColoresDrako.TEXTO}"
                                    f"{usuario}:{password}"
                                    f"{ColoresDrako.RESET}"
                                )

                if generados >= cantidad_objetivo:
                    break

    except KeyboardInterrupt:
        print()
        print(
            f"{ColoresDrako.ALERTA}"
            f"[!] Generacion interrumpida por el usuario."
            f"{ColoresDrako.RESET}"
        )
    finally:
        if buffer_escritura:
            archivo.write(''.join(buffer_escritura))
        archivo.close()

    if not verbose:
        print()

    tiempo_total = time.time() - tiempo_inicio
    cpm_final = int(generados / (tiempo_total / 60)) if tiempo_total > 0 else 0

    print()
    linea()
    print(
        f"{ColoresDrako.EXITO}"
        f"Combos generados: {formatear_numero(generados)}"
        f"{ColoresDrako.RESET}"
    )
    print(
        f"{ColoresDrako.TEXTO}"
        f"Tiempo: {tiempo_total:.2f}s | CPM: {formatear_numero(cpm_final)}"
        f"{ColoresDrako.RESET}"
    )
    if len(archivos_creados) == 1:
        print(
            f"{ColoresDrako.TEXTO}"
            f"Archivo: {archivos_creados[0]}"
            f"{ColoresDrako.RESET}"
        )
    else:
        print(
            f"{ColoresDrako.TEXTO}"
            f"Archivos ({len(archivos_creados)} partes):"
            f"{ColoresDrako.RESET}"
        )
        for arch in archivos_creados:
            print(
                f"{ColoresDrako.TEXTO}"
                f"    - {arch}"
                f"{ColoresDrako.RESET}"
            )

    return archivos_creados[0] if archivos_creados else ruta_base



def main():
    os.makedirs(RUTA_BASE, exist_ok=True)

    clearConsole()

    titulo = r"""
    _____            ____          _       
   |   __|___ ___   |    \ ___ ___| |_ ___ 
   |  |  | -_|   |  |  |  |  _| .'| '_| . |
   |_____|___|_|_|  |____/|_| |__,|_,_|___|
"""
    imprimir_titulo(titulo)

    while True:
        opcion = menu_principal()

        if opcion == "1":
            ruta = generar_usuario_unico()
        else:
            ruta = generar_usuario_y_pass()

        print()
        linea()

        print(
            f"{ColoresDrako.EXITO}"
            f"Finalizado"
            f"{ColoresDrako.RESET}"
        )

        print()

        seguir = input(
            f"{ColoresDrako.EXITO}"
            f"Seguir generando? (s/n): "
            f"{ColoresDrako.RESET}"
        ).lower()

        if seguir == "n":
            print(
                f"{ColoresDrako.SECUNDARIO}"
                f"Hasta luego que tengan un hermoso dia"
                f"{ColoresDrako.RESET}"
            )
            break


if __name__ == "__main__":
    main()
