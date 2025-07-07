"""
-----------------------------------------------------------------------------------------------
Título: Desarrollo inmobiliario
Fecha: 27/05/2025
Autor: Grupo 7 (Nicolas Mendez, Valentina Clemente)
----------------------------------------------------------------------------------------------------
Título: Sistema de Gestión Inmobiliaria
Autores: Grupo 7 - Joaquina Dias, María Luz Gaetan, Nicolas Mendez, Valentina Clemente, Brendan Russell
Fecha: 27/05/2025
Materia: Programación I

Descripción general:
--------------------
Este sistema fue desarrollado para administrar la gestión de propietarios, propiedades y comisiones 
dentro del rubro inmobiliario. Está pensado para una inmobiliaria que necesita registrar operaciones 
de alquiler y venta, calcular automáticamente comisiones, y generar reportes anuales.

El programa se basa en estructuras de datos simples (diccionarios y listas) y un menú interactivo 
por consola que permite realizar las principales tareas administrativas.

Características principales:
----------------------------
1. Gestión de propietarios:
   - Alta, modificación, baja (lógica) y listado de propietarios activos.
   - Asociación multivaluada de propiedades por propietario.

2. Gestión de propiedades:
   - Alta, modificación, baja (lógica) y listado de propiedades activas.
   - Registro de tipo, superficie, valor y propietario.
   - Asociación de múltiples comisiones por propiedad (campo multivaluado).

3. Gestión de comisiones:
   - Cálculo automático del 10% sobre el valor de la propiedad según operación (venta o alquiler).
   - Registro histórico organizado por fecha.
   - Almacenamiento multivaluado por fecha.

4. Informes:
   - Comisiones del mes actual.
   - Resumen anual por propiedad: total en pesos y cantidad de operaciones.
   - Sección destinada a un informe adicional definido por el equipo (a implementar).

Estructuras de datos utilizadas:
-------------------------------
- `propietarios`: diccionario que usa el DNI como clave. Cada propietario puede tener múltiples propiedades.
- `propiedades`: diccionario que usa un código de propiedad como clave. Cada propiedad puede tener múltiples comisiones.
- `comisiones`: diccionario con fechas como claves. Cada fecha tiene una lista de comisiones registradas ese día.

Campos multivaluados:
---------------------
- `propietarios['dni']['propiedades']`: lista de códigos de propiedades que posee.
- `propiedades['codigo']['comisiones']`: lista de montos de comisiones registradas.
- `comisiones['fecha']`: lista de transacciones registradas ese día.

Tecnologías utilizadas:
------------------------
- Python estándar.
- Módulo `datetime` para fechas.
- Módulo `re` para validación de emails.

Observaciones finales:
-----------------------
El programa está pensado con menú por consola y puede ser mejorado fácilmente para integrarse 
en una interfaz gráfica en el futuro. Cumple con las consignas de trabajo del segundo cuatrimestre, 
incluyendo el uso de datos multivaluados y diseño estructurado sin programación orientada a objetos.
"""
#----------------------------------------------------------------------------------------------
# MÓDULOS
#----------------------------------------------------------------------------------------------
from datetime import datetime
import re
import json

#----------------------------------------------------------------------------------------------
# FUNCIONES
#----------------------------------------------------------------------------------------------
#Funciones para Json---------------------------------------------------------------------------
def leer_json(nombre_archivo):
    try:
        with open(nombre_archivo, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def escribir_json(nombre_archivo, datos):
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)


def leer_json(nombre_archivo):
    try:
        with open(nombre_archivo, mode="r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}

def escribir_json(nombre_archivo, diccionario):
    with open(nombre_archivo, mode="w", encoding="utf-8") as f:
        json.dump(diccionario, f, ensure_ascii=False, indent=4)


#Funcines Generales-------------------------------------
def generar_fecha_hora():  #Genera y retorna fecha y hora actual en 'YYYY.MM.DD HH:MM:SS para registrar momentos exactos
    ahora = datetime.now()
    return ahora.strftime("%Y.%m.%d %H:%M:%S")

def valor_alquiler():
   while True:
      entrada = input("ingrese el valor del alquiler: ") #solicita valor y permite cancelar con-1
      if entrada == "-1":
         print("operacion cancelada.")
         return -1
      elif entrada.isdigit(): 
         return int(entrada)
      else: 
         print("entrada invalida, tenes q ingresar un numero entero positivo.") #asefura que la entrada sea entera positiva

def alta_propietario(propietarios):
   propietarios = leer_json("propietarios.json")
   print("\n--- Agregar propietario ---") #agrega un nuevo propietario
   codigo = input("ingrese el codigo del propietario: ")
   if codigo in propietarios:
      print("el propietario ya existe.")
   else: #solicita datos personales y los almacena en el diccionario
      nombre = input("ingrese nombre completo: ")
      dni = input("ingrese el dni: ")
      telefono = input("ingrese el telefono: ")
      while True:          
         email = input("ingrese el email: ")
         if validar_email(email):
            break
         else:
            print("Email inválido.")
            
      propietarios[codigo] = {
         "id": codigo,
         "nombre": nombre,
         "dni": dni,
         "telefono": telefono,            
         "email": email,
         "activo": True
      }
      escribir_json("propietarios.json", propietarios)
      print("propietario agregado correctamente.") #mensaje de confirmacion
    

def modificar_propietario(propietarios): #para modificar datos de un propetario
    propietarios = leer_json("propietarios.json")
    codigo = input("ingrese codigo del propietario que qeres modificar: ")
    if codigo in propietarios and propietarios[codigo]["activo"]:
        propietarios[codigo]["nombre"] = input("nuevo nombre: ") #reemplaza los campos
        propietarios[codigo]["dni"] = input("nuevo DNI: ")
        propietarios[codigo]["telefono"] = input("nuevo telefono: ")

        while True:
                nuevo_email = input("nuevo email: ")
                if validar_email(nuevo_email):
                    propietarios[codigo]["email"] = nuevo_email
                    break
                else:
                    print("Email inválido. Intente nuevamente.")
        
        escribir_json("propietarios.json", propietarios)            
        print("propietario modificado.")
    else:
        print("propietario no encontrado o inactivo.") #si el propietario no es activo, no hay campos a reeplazar
    

def baja_propietario(propietarios): #dar de baja a propietarios activos (sin eliminarlos, simplemente cambia el estado)
    propietarios = leer_json("propietarios.json")
    codigo = input("ingrese codigo del propietario a eliminar: ")
    if codigo in propietarios and propietarios[codigo]["activo"]: #si se encuentra el codigo ingresado, se reemplaza el valor del codigo (activo = False)
        propietarios[codigo]["activo"] = False #damos de baja 
        escribir_json("propietarios.json", propietarios)
        print("propietario desactivado.")
    else:
        print("propietario no encontrado o ya inactivo.") #si ya esta inactivo, no hay nada que dar de baja


def listar_propietarios(propietarios): #mostrar los propietarios activos
    propietarios = leer_json("propietarios.json")
    print("\nListado de propietarios activos:")
    for cod, datos in propietarios.items(): #recorre todos los propietarios
        if datos["activo"]: #imprime solo los que son activos
            print(f"codigo: {cod} | nombre: {datos['nombre']} | dni: {datos['dni']} | telefeono: {datos['telefono']}| email: {datos['email']}")

def alta_propiedad(propiedades, propietarios): #dar de alta una nueva propiedad si no existe
   propiedades = leer_json("propiedades.json")
   codigo = input("ingrese codigo de la propiedad: ")
   if codigo in propiedades: #si el codigo ya existe, no hay nada que agregar
      print("la propiedad ya existe.") 
   else: #no existe el codigo, solicita datos
      direccion = input("ingrese dirección: ")
      propietario = input("codigo del propietario: ")
      valor = valor_alquiler()
      propiedades[codigo] = {
         "direccion": direccion,
         "propietario": propietario,
         "valor": valor,
         "activo": True
      }
      if propietario in propietarios:
         if "propiedades" not in propietarios[propietario]:
            propietarios[propietario]["propiedades"] = []
         propietarios[propietario]["propiedades"].append(codigo)
      propiedades[codigo]["comisiones"] = []
      escribir_json("propiedades.json", propiedades)
      print("propiedad agregada.") #mensaje de confirmacion


def modificar_propiedad(propiedades): #modificar datos de propiedad activa
    propiedades = leer_json("propiedades.json")
    codigo = input("ingrese el codigo de la propiedad a modificar: ") 
    if codigo in propiedades and propiedades[codigo]["activo"]: #reemplaza dirección, propietario y valor 
        propiedades[codigo]["direccion"] = input("nueva dirección: ")
        propiedades[codigo]["propietario"] = input("nuevo codigo del propietario: ")
        propiedades[codigo]["valor"] = valor_alquiler()
        escribir_json("propiedades.json", propiedades)
        print("propiedad modificada.")
    else:
        print("propiedad no encontrada o inactiva.") #al no estar activa, no se pide una nueva solicitud de datos


def baja_propiedad(propiedades): #da de baja una propiedad (sin eliminarla)
    propiedades = leer_json("propiedades.json")
    codigo = input("ingrese el codigo de la propiedad a eliminar: ").lower()
    codigo_encontrado = None
    for key in propiedades:
        if key.lower() == codigo:
            codigo_encontrado = key
            break
    if codigo_encontrado and propiedades[codigo_encontrado]["activo"]: 
        propiedades[codigo_encontrado]["activo"] = False
        escribir_json("propiedades.json", propiedades)
        print("propiedad desactivada.")
    else:
        print("propiedad no encontrada o ya inactiva")
   

def listar_propiedades(propiedades): #lista propiedades
    propiedades = leer_json("propiedades.json")
    print("\nlistado de propiedades activas:")
    for cod, datos in propiedades.items(): #recorre las propiedades dentro del diccionario
        if datos["activo"]: #verifica si activo=True e imprime los activos
            print(f"codigo: {cod} | direccion: {datos['direccion']} | propietario: {datos['propietario']} | alquiler: ${datos['valor']}")

def registrar_comision(propiedades, comisiones):
   cod_prop = input("Ingrese código de la propiedad: ")
   if cod_prop in propiedades and propiedades[cod_prop]["activo"]:
      valor = propiedades[cod_prop]["valor"]
      monto = valor * 0.10
      fecha_completa = generar_fecha_hora()
      fecha = fecha_completa.split()[0] 
      tipo_operacion = input("Tipo de operación (venta/alquiler): ").strip().lower()
      mes_anio = datetime.now().strftime("%b.%y").upper()
      dni_propietario = propiedades[cod_prop].get("dni", "DESCONOCIDO")

      nueva_comision = {
         "codigo_propiedad": cod_prop,
         "dni_propietario": dni_propietario,
         "monto": monto,
         "tipo_operacion": tipo_operacion,
         "mes_anio": mes_anio
      }
      if fecha not in comisiones:
         comisiones[fecha] = []
      comisiones[fecha].append(nueva_comision)
      
      if "comisiones" not in propiedades[cod_prop]:
         propiedades[cod_prop]["comisiones"] = []
         propiedades[cod_prop]["comisiones"].append(monto)
         escribir_json("comisiones.json", comisiones) 
         print(f"Comisión registrada: ${monto:.2f} ({fecha_completa})")
      else:
        print("Propiedad no encontrada o inactiva.")
  

def comisiones_del_mes(comisiones):
    comisiones = leer_json("comisiones.json")
    print("\ncomisiones del mes en curso:")
    hoy = datetime.now()
    for fecha_str, lista in comisiones.items():
        fecha = datetime.strptime(fecha_str, "%Y.%m.%d")
        if fecha.month == hoy.month and fecha.year == hoy.year:
            for c in lista:
                print(f"{fecha_str} | propiedad: {c['codigo_propiedad']} | comision: ${c['monto']:.2f}")

def resumen_anual_comisiones_valor(comisiones, propiedades):
   comisiones = leer_json("comisiones.json")
   print("\nResumen anual de comisiones por propiedad (pesos):")
   año_actual = datetime.now().year
   totales = {}
   for fecha_str, lista in comisiones.items():
      fecha = datetime.strptime(fecha_str, "%Y.%m.%d")
      if fecha.year == año_actual:
         for c in lista:
            prop = c["codigo_propiedad"]
            totales[prop] = totales.get(prop, 0) + c["monto"]
    for cod_prop, datos in propiedades.items():
        if datos["activo"]:
            lista_comisiones = datos.get("comisiones", [])
            for monto in lista_comisiones:
                totales[cod_prop] = totales.get(cod_prop, 0) + monto

    if totales:
        for prop, monto in totales.items():
            print(f"Propiedad: {prop} | Total comisiones: ${monto:.2f}")
    else:
        print("No hay comisiones registradas en el año actual.")


def resumen_anual_comisiones_cantidad(comisiones, propiedades):
   comisiones = leer_json("comisiones.json")
   print("\nResumen anual de comisiones por propiedad (cantidad):")
   año_actual = datetime.now().year
   conteo = {}
   for fecha_str, lista in comisiones.items():
      fecha = datetime.strptime(fecha_str, "%Y.%m.%d")
      if fecha.year == año_actual:
         for c in lista:
            prop = c["codigo_propiedad"]
            conteo[prop] = conteo.get(prop, 0) + 1
    
   for cod_prop, datos in propiedades.items():
      if datos["activo"]:
         lista_comisiones = datos.get("comisiones", [])
         conteo[cod_prop] = conteo.get(cod_prop, 0) + len(lista_comisiones)

    if conteo:
       for prop, cantidad in conteo.items():
          print(f"Propiedad: {prop} | Cantidad de comisiones: {cantidad}")
    else:
       print("No hay comisiones registradas en el año actual.")

def informe():
    print("informe a mejorar") #falta implementacion para engrega final

def validar_email(email):
    pat = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pat, email) is not None
#----------------------------------------------------------------------------------------------
# CUERPO PRINCIPAL
#----------------------------------------------------------------------------------------------
def main():
    #-------------------------------------------------
    # Inicialización de variables
    #----------------------------------------------------------------------------------------------
    """
-----------------------------------------------------------------------------------------------
 ESTRUCTURAS DE DATOS Y TIPOS DE ENTIDADES
 -----------------------------------------------------------------------------------------------
 Diccionario de propietarios:
   Clave: DNI del propietario (str)
   Valor: Diccionario con los siguientes campos:
       - nombre (str)
       - dni (str)
       - telefono (str)
       - email (str)
       - activo (bool)
       - propiedades (list[str]) --> IDs de propiedades asociadas (opcional / multivaluado)

 Diccionario de propiedades:
   Clave: codigo de propiedad (str)
   Valor: Diccionario con los siguientes campos:
       - direccion (str)
       - propietario (str) --> nombre
       - dni (str) --> del propietario
       - tipo (str) --> "Departamento", "Casa", etc.
       - superficie (int)
       - valor (int) --> valor de alquiler/venta
       - activo (bool)
       - comisiones (list[float]) --> montos de comisiones (opcional / multivaluado)

 Diccionario de comisiones:
   Clave: fecha en formato "YYYY.MM.DD" (str)
   Valor: lista de diccionarios, cada uno con:
       - codigo_propiedad (str)
       - monto (float)
       - tipo_operacion (str): "alquiler" o "venta"
       - mes_anio (str): por ejemplo "JUL.24"
"""
    propietarios = {
    "30111222": {"nombre": "Juan Pérez", "dni": "30111222","telefono": "1155550001", "email": "juan@gmail.com", "activo": True, "propiedades": ["P001", "P003"]},
    "30222333": {"nombre": "María Gómez", "dni": "30222333","telefono": "1155550002", "email": "maria@gmail.com", "activo": True, "propiedades": ["P002"]},
    "30333444": {"nombre": "Carlos López", "dni": "30333444","telefono": "1155550003", "email": "carlos@gmail.com", "activo": True, "propiedades": ["P003"]},
    "30444555": {"nombre": "Ana Torres", "dni": "30444555","telefono": "1155550004", "email": "ana@gmail.com", "activo": True, "propiedades": ["P004"]},
    "30555666": {"nombre": "Laura Méndez", "dni": "30555666","telefono": "1155550005", "email": "laura@gmail.com", "activo": True, "propiedades": ["P005"]},
    "30666777": {"nombre": "Pedro Rodríguez","dni": "30666777", "telefono": "1155550006", "email": "pedro@gmail.com", "activo": True, "propiedades": ["P006"]},
    "30777888": {"nombre": "Lucía Fernández","dni": "30777888", "telefono": "1155550007", "email": "lucia@gmail.com", "activo": True, "propiedades": ["P007"]},
    "30888999": {"nombre": "Diego Suárez", "dni": "30888999","telefono": "1155550008", "email": "diego@gmail.com", "activo": True, "propiedades": ["P008"]},
    "30999000": {"nombre": "Marta Díaz","dni": "30999000", "telefono": "1155550009", "email": "marta@gmail.com", "activo": True, "propiedades": ["P009"]},
    "31000111": {"nombre": "Jorge Silva","dni": "31000111", "telefono": "1155550010", "email": "jorge@gmail.com", "activo": True, "propiedades": ["P010"]},
    }

    propiedades = {
    "P001": {"direccion": "Calle 123","propietario": "Juan Pérez", "tipo": "Departamento", "superficie": 75, "valor": 120000, "dni": "30111222","activo": True, "comisiones": [3000]},
    "P002": {"direccion": "Av. 456","propietario": "María Gómez", "tipo": "Casa", "superficie": 150, "valor": 250000, "dni": "30222333","activo": True, "comisiones": [12000]},
    "P003": {"direccion": "Diag. 789","propietario": "Carlos López", "tipo": "PH", "superficie": 90, "valor": 180000, "dni": "30333444","activo": True, "comisiones": [5000]},
    "P004": {"direccion": "Las Heras 101","propietario": "Ana Torres", "tipo": "Casa", "superficie": 200, "valor": 310000, "dni": "30444555","activo": True, "comisiones": [15000]},
    "P005": {"direccion": "San Martín 202","propietario": "Laura Méndez", "tipo": "Departamento", "superficie": 60, "valor": 95000, "dni": "30555666","activo": True, "comisiones": [3500]},
    "P006": {"direccion": "Belgrano 303","propietario": "Pedro Rodríguez", "tipo": "PH", "superficie": 85, "valor": 150000, "dni": "30666777","activo": True, "comisiones": [10000]},
    "P007": {"direccion": "Córdoba 404","propietario": "Lucía Fernández", "tipo": "Departamento", "superficie": 70, "valor": 110000, "dni": "30777888","activo": True, "comisiones": [4000]},
    "P008": {"direccion": "Santa Fe 505","propietario": "Diego Suárez", "tipo": "Casa", "superficie": 180, "valor": 290000, "dni": "30888999","activo": True, "comisiones": [13000]},
    "P009": {"direccion": "Rivadavia 606","propietario": "Marta Díaz", "tipo": "PH", "superficie": 95, "valor": 160000, "dni": "30999000","activo": True, "comisiones": [4200]},
    "P010": {"direccion": "Mitre 707","propietario": "Jorge Silva", "tipo": "Departamento", "superficie": 55, "valor": 87000, "dni": "31000111","activo": True, "comisiones": [9000]}
    }
    
    comisiones = {
        "2024.01.15": [
            {"codigo_propiedad": "P001", "monto": 3000, "tipo_operacion": "alquiler", "mes_anio": "ENE.24"}
        ],
        "2024.02.10": [
            {"codigo_propiedad": "P002", "monto": 12000, "tipo_operacion": "venta", "mes_anio": "FEB.24"}
        ],
        "2024.03.05": [
            {"codigo_propiedad": "P003", "monto": 5000, "tipo_operacion": "alquiler", "mes_anio": "MAR.24"}
        ],
        "2024.04.12": [
            {"codigo_propiedad": "P004", "monto": 15000, "tipo_operacion": "venta", "mes_anio": "ABR.24"}
        ],
        "2024.05.22": [
            {"codigo_propiedad": "P005", "monto": 3500, "tipo_operacion": "alquiler", "mes_anio": "MAY.24"}
        ],
        "2024.06.30": [
            {"codigo_propiedad": "P006", "monto": 10000, "tipo_operacion": "venta", "mes_anio": "JUN.24"}
        ],
        "2024.07.08": [
            {"codigo_propiedad": "P007", "monto": 4000, "tipo_operacion": "alquiler", "mes_anio": "JUL.24"}
        ],
        "2024.08.19": [
            {"codigo_propiedad": "P008", "monto": 13000, "tipo_operacion": "venta", "mes_anio": "AGO.24"}
        ],
        "2024.09.27": [
            {"codigo_propiedad": "P009", "monto": 4200, "tipo_operacion": "alquiler", "mes_anio": "SEP.24"}
        ],
        "2024.10.03": [
            {"codigo_propiedad": "P010", "monto": 9000, "tipo_operacion": "venta", "mes_anio": "OCT.24"}
        ]
    }
    #-------------------------------------------------
    # Bloque de menú
    #----------------------------------------------------------------------------------------------
    while True:
        while True:
            opciones = 4
            print()
            print("---------------------------")
            print("MENÚ PRINCIPAL")
            print("---------------------------")
            print("[1] Gestión de propietarios")
            print("[2] Gestión de propiedades")
            print("[3] Gestión de comisiones")
            print("[4] Informes")
            print("---------------------------")
            print("[0] Salir del programa")
            print("---------------------------")
            print()
            
            opcionSubmenu = ""
            opcionMenuPrincipal = input("Seleccione una opción: ")
            if opcionMenuPrincipal in [str(i) for i in range(0, opciones + 1)]: # Sólo continua si se elije una opcion de menú válida
                break
            else:
                input("Opción inválida. Presione ENTER para volver a seleccionar.")
        print()

        if opcionMenuPrincipal == "0": # Opción salir del programa
            exit() # También puede ser sys.exit() para lo cual hay que importar el módulo sys

        elif opcionMenuPrincipal == "1":   # Opción 1 del menú principal
            while True:
                while True:
                    opciones = 4
                    print()
                    print("---------------------------")
                    print("MENÚ PRINCIPAL > GESTIÓN DE PROPIETARIOS")
                    print("---------------------------")
                    print("[1] Ingresar propietario")
                    print("[2] Modificar propietario")
                    print("[3] Eliminar propietario")
                    print("[4] Listado de propietarios")
                    print("---------------------------")
                    print("[0] Volver al menú anterior")
                    print("---------------------------")
                    print()
                    
                    opcionSubmenu = input("Seleccione una opción: ")
                    if opcionSubmenu in [str(i) for i in range(0, opciones + 1)]: # Sólo continua si se elije una opcion de menú válida
                        break
                    else:
                        input("Opción inválida. Presione ENTER para volver a seleccionar.")
                print()

                if opcionSubmenu == "0": # Opción salir del submenú
                    break # No sale del programa, sino que vuelve al menú anterior
                
                elif opcionSubmenu == "1":   # Opción 1 del submenú
                    propietarios = alta_propietario(propietarios)
                    
                elif opcionSubmenu == "2":   # Opción 2 del submenú
                    propietarios = modificar_propietario(propietarios)
                
                elif opcionSubmenu == "3":   # Opción 3 del submenú
                    propietarios = baja_propietario(propietarios)
                
                elif opcionSubmenu == "4":   # Opción 4 del submenú
                    listar_propietarios(propietarios)

                input("\nPresione ENTER para volver al menú.") # Pausa entre opciones
                print("\n\n")


        elif opcionMenuPrincipal == "2":   # Opción 2 del menú principal
            while True:
                while True:
                    opciones = 4
                    print()
                    print("---------------------------")
                    print("MENÚ PRINCIPAL > GESTIÓN DE PROPIEDADES")
                    print("---------------------------")
                    print("[1] Ingresar propiedad")
                    print("[2] Modificar propiedad")
                    print("[3] Eliminar propiedad")
                    print("[4] Listado de propiedades")
                    print("---------------------------")
                    print("[0] Volver al menú anterior")
                    print("---------------------------")
                    print()
                    
                    opcionSubmenu = input("Seleccione una opción: ")
                    if opcionSubmenu in [str(i) for i in range(0, opciones + 1)]: # Sólo continua si se elije una opcion de menú válida
                        break
                    else:
                        input("Opción inválida. Presione ENTER para volver a seleccionar.")
                print()

                if opcionSubmenu == "0": # Opción salir del submenú
                    break # No sale del programa, sino que vuelve al menú anterior
                
                elif opcionSubmenu == "1":   # Opción 1 del submenú
                    print("ingrese a la propiedad")
                    propiedades = alta_propiedad(propiedades, propietarios)
                    
                elif opcionSubmenu == "2":   # Opción 2 del submenú
                    print("modifique la propiedad")
                    propiedades = modificar_propiedad(propiedades)
                
                elif opcionSubmenu == "3":   # Opción 3 del submenú
                    print("elimine la propiedad")
                    propiedades = baja_propiedad(propiedades)
                
                elif opcionSubmenu == "4":   # Opción 4 del submenú
                    print("listado de propiedades")
                    listar_propiedades(propiedades)

                input("\nPresione ENTER para volver al menú.") # Pausa entre opciones
                print("\n\n")
        
        elif opcionMenuPrincipal == "3":   # Opción 3 del menú principal
            while True:
                while True:
                    opciones = 1
                    print()
                    print("---------------------------")
                    print("MENÚ PRINCIPAL > GESTIÓN DE COMISIONES")
                    print("---------------------------")
                    print("[1] Registro de comisiones")
                    print("---------------------------")
                    print("[0] Volver al menú anterior")
                    print("---------------------------")
                    print()
                    
                    opcionSubmenu = input("Seleccione una opción: ")
                    if opcionSubmenu in [str(i) for i in range(0, opciones + 1)]: # Sólo continua si se elije una opcion de menú válida
                        break
                    else:
                        input("Opción inválida. Presione ENTER para volver a seleccionar.")
                print()

                if opcionSubmenu == "0": # Opción salir del submenú
                    break # No sale del programa, sino que vuelve al menú anterior
                
                elif opcionSubmenu == "1":   # Opción 1 del submenú
                    print("registro de comisiones")
                    comisiones = registrar_comision(propiedades, comisiones)

                input("\nPresione ENTER para volver al menú.") # Pausa entre opciones
                print("\n\n")
        
        elif opcionMenuPrincipal == "4":   # Opción 4 del menú principal
            while True:
                while True:
                    opciones = 4
                    print()
                    print("---------------------------")
                    print("MENÚ PRINCIPAL > INFORMES")
                    print("---------------------------")
                    print("[1] Comisiones del mes")
                    print("[2] Resumen anual de comisiones por propiedad (cantidades)")
                    print("[3] Resumen anual de comisiones por propiedad (pesos)")
                    print("[4] Informe ideado por el equipo")
                    print("---------------------------")
                    print("[0] Volver al menú anterior")
                    print("---------------------------")
                    print()
                    
                    opcionSubmenu = input("Seleccione una opción: ")
                    if opcionSubmenu in [str(i) for i in range(0, opciones + 1)]: # Sólo continua si se elije una opcion de menú válida
                        break
                    else:
                        input("Opción inválida. Presione ENTER para volver a seleccionar.")
                print()

                if opcionSubmenu == "0": # Opción salir del submenú
                    break # No sale del programa, sino que vuelve al menú anterior
                
                elif opcionSubmenu == "1":   # Opción 1 del submenú
                    comisiones_del_mes(comisiones)
                    
                elif opcionSubmenu == "2":   # Opción 2 del submenú
                    resumen_anual_comisiones_cantidad(comisiones, propiedades)
                
                elif opcionSubmenu == "3":   # Opción 3 del submenú
                    resumen_anual_comisiones_valor(comisiones, propiedades)
                
                elif opcionSubmenu == "4":   # Opción 4 del submenú
                    informe()

                input("\nPresione ENTER para volver al menú.") # Pausa entre opciones
                print("\n\n")

        if opcionSubmenu != "0": # Pausa entre opciones. No la realiza si se vuelve de un submenú
            input("\nPresione ENTER para volver al menú.")
            print("\n\n")
# Punto de entrada al programa
main()
