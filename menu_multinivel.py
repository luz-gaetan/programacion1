"""
-----------------------------------------------------------------------------------------------
Título: Desarrollo inmobiliario
Fecha: 27/05/2025
Autor: Grupo 7 (Joaquina Dias, María Luz Gaetan, Nicolas Mendez, Valentina Clemente, Brendan Russell)

Descripción:

Pendientes:
-----------------------------------------------------------------------------------------------
"""
"""mejorar el resumen anual de propiedades por cantidad y pesos y el informe"""

#----------------------------------------------------------------------------------------------
# MÓDULOS
#----------------------------------------------------------------------------------------------
from datetime import datetime
import re
#----------------------------------------------------------------------------------------------
# FUNCIONES
#----------------------------------------------------------------------------------------------
def generar_fecha_hora():  #Genera y retorna fecha y hora actual en 'YYYY.MM.DD HH:MM:SS para registrar momentos exactos
    ahora = datetime.now()
    return ahora.strftime("%Y.%m.%d %H:%M:%S")

def valor_alquiler():
    while True:
        try:
            entrada = input("ingrese el valor del alquiler: ") #solicita valor y permite cancelar con-1
            if entrada == "-1":
                print("operacion cancelada.")
                return -1
            valor = int(entrada)
            if valor > 0:
                return valor
            else:
                print("El valor debe ser un numero entero positivo")
        except ValueError: 
            print("entrada invalida, tenes q ingresar un numero entero positivo.") #asefura que la entrada sea entera positiva

def alta_propietario(propietarios):
    try:
        print("\n--- alta de propietario ---") #da de alta un nuevo propietario si el codigo no existe
        codigo = input("ingrese el codigo del propietario: ")
        if codigo in propietarios:
            print("el propietario ya existe.")
            return propietarios
    
        nombre = input("ingrese nombre completo: ")
        dni = input("ingrese el dni: ")
        telefono = input("ingrese el telefono: ")
        
        while True:
            email = input("ingrese el email: ")
            if validar_email(email):
                break
            else:
                print("Email inválido")
                    
        propietarios[codigo] = {
            "id": codigo,
            "nombre": nombre,
            "dni": dni,
            "telefono": telefono,
            "email": email,
            "activo": True
        }
        print("propietario agregado correctamente.") #mensaje de confirmacion
    except Exception as e:
        print(f"Error al agregar propietario: {e}")
    return propietarios

def modificar_propietario(propietarios): #para modificar datos de un propetario
    try:
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
            print("propietario modificado.")
        else:
            print("propietario no encontrado o inactivo.") #si el propietario no es activo, no hay campos a reeplazar
    except Exception as e:
        print(f"Error al modificar propietario: {e}") 
    return propietarios

def baja_propietario(propietarios): #dar de baja a propietarios activos (sin eliminarlos, simplemente cambia el estado)
    codigo = input("ingrese codigo del propietario a eliminar: ")
    if codigo in propietarios and propietarios[codigo]["activo"]: #si se encuentra el codigo ingresado, se reemplaza el valor del codigo (activo = False)
        propietarios[codigo]["activo"] = False #damos de baja 
        print("propietario desactivado.")
    else:
        print("propietario no encontrado o ya inactivo.") #si ya esta inactivo, no hay nada que dar de baja
    return propietarios

def listar_propietarios(propietarios): #mostrar los propietarios activos
    print("\nListado de propietarios activos:")
    for cod, datos in propietarios.items(): #recorre todos los propietarios
        if datos["activo"]: #imprime solo los que son activos
            print(f"codigo: {cod} | nombre: {datos['nombre']} | dni: {datos['dni']} | telefeono: {datos['telefono']}| email: {datos['email']}")

def alta_propiedad(propiedades): #dar de alta una nueva propiedad si no existe
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
        print("propiedad agregada.") #mensaje de confirmacion
    return propiedades

def modificar_propiedad(propiedades): #modificar datos de propiedad activa
    codigo = input("ingrese el codigo de la propiedad a modificar: ") 
    if codigo in propiedades and propiedades[codigo]["activo"]: #reemplaza dirección, propietario y valor 
        propiedades[codigo]["direccion"] = input("nueva dirección: ")
        propiedades[codigo]["propietario"] = input("nuevo codigo del propietario: ")
        propiedades[codigo]["valor"] = valor_alquiler()
        print("propiedad modificada.")
    else:
        print("propiedad no encontrada o inactiva.") #al no estar activa, no se pide una nueva solicitud de datos
    return propiedades

def baja_propiedad(propiedades): #da de baja una propiedad (sin eliminarla)
    codigo = input("ingrese el codigo de la propiedad a eliminar: ").lower()
    codigo_encontrado = None
    for key in propiedades:
        if key.lower() == codigo:
            codigo_encontrado = key
            break
    if codigo_encontrado and propiedades[codigo_encontrado]["activo"]: 
        propiedades[codigo_encontrado]["activo"] = False
        print("propiedad desactivada.")
    else:
        print("propiedad no encontrada o ya inactiva")
    return propiedades

def listar_propiedades(propiedades): #lista propiedades
    print("\nlistado de propiedades activas:")
    for cod, datos in propiedades.items(): #recorre las propiedades dentro del diccionario
        if datos["activo"]: #verifica si activo=True e imprime los activos
            print(f"codigo: {cod} | direccion: {datos['direccion']} | propietario: {datos['propietario']} | alquiler: ${datos['valor']}")

def registrar_comision(propiedades, comisiones): #registra comisión del 10% del valor de una propiedad activa.
    cod_prop = input("ingrese codigo de la propiedad: ")
    if cod_prop in propiedades and propiedades[cod_prop]["activo"]:
        valor = propiedades[cod_prop]["valor"]
        monto = valor * 0.10 #calculo del 10% del valor
        fecha = generar_fecha_hora() #registra fecha y hora usando la funcion
        comisiones.append({ #agrega los datos a "comisiones"
            "fecha": fecha,
            "propiedad": cod_prop,
            "monto": monto
        })
        print(f"comision registrada: ${monto:.2f} ({fecha})")
    else:
        print("propiedad no encontrada o inactiva.")
    return comisiones

def comisiones_del_mes(comisiones): #mostrar comisiones en el mes y año actuales
    print("\ncomisiones del mes en curso:")
    hoy = datetime.now()
    for c in comisiones: #compara la fecha de cada comisión con la fecha actual
        fecha = datetime.strptime(c["fecha"], "%Y.%m.%d %H:%M:%S")
        if fecha.month == hoy.month and fecha.year == hoy.year: #si coinciden, se imprimen
            print(f"{c['fecha']} | propiedad: {c['propiedad']} | comision: ${c['monto']:.2f}")
            

def resumen_anual_comisiones_valor(comisiones): #Muestra todas las comisiones x propiedad durante el año actual
    print("\nresumen anual de comisiones por propiedad (pesos):")
    año_actual = datetime.now().year  #se establece el año actual
    totales = {} #inicializamos diccionario para ir sumando los montos de comisiones

    for c in comisiones: #recorremos comisiones
        fecha = datetime.strptime(c["fecha"], "%Y.%m.%d %H:%M:%S") # convertimos cadena en formato datetime
        if fecha.year == año_actual: #comparamos el año con el establecido
            prop = c["propiedad"]
            totales[prop] = totales.get(prop, 0) + c["monto"] #se suma el monto de la comisión al acumulado total de la propiedad

    if totales:
        for prop, monto in totales.items():
            print(f"propiedad: {prop} | total comisiones: ${monto:.2f}")
    else:
        print("no hay comisiones registradas en el año actual.")


def resumen_anual_comisiones_cantidad(comisiones): #mostar total de comisiones registradas por propiedad durante el año actual
    print("\nresumen anual de comisiones por propiedad (cantidades):")
    año_actual = datetime.now().year #establecer año actual
    conteo = {} #inicializar diccionario para contar cantidad de comisiones por propiedad

    for c in comisiones: #recorre comisiones
        fecha = datetime.strptime(c["fecha"], "%Y.%m.%d %H:%M:%S") #convierte cadena al formato datetime (YYYY.MM.DD HH:MM:SS)
        if fecha.year == año_actual: #filtra comisiones del año actual
            prop = c["propiedad"]
            conteo[prop] = conteo.get(prop, 0) + 1 #cuenta comisiones por propiedad

    if conteo:
        for prop, cantidad in conteo.items():
            print(f"propiedad: {prop} | cantidad de comisiones: {cantidad}")
    else:
        print("no hay comisiones registradas en el año actual.")


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
    propietarios = {
        "30111222": {"nombre": "Juan Pérez", "dni": "30111222","telefono": "1155550001", "email": "juan@gmail.com", "activo": True},
        "30222333": {"nombre": "María Gómez", "dni": "30222333","telefono": "1155550002", "email": "maria@gmail.com", "activo": True},
        "30333444": {"nombre": "Carlos López", "dni": "30333444","telefono": "1155550003", "email": "carlos@gmail.com", "activo": True},
        "30444555": {"nombre": "Ana Torres", "dni": "30333444","telefono": "1155550004", "email": "ana@gmail.com", "activo": True},
        "30555666": {"nombre": "Laura Méndez", "dni": "30444555","telefono": "1155550005", "email": "laura@gmail.com", "activo": True},
        "30666777": {"nombre": "Pedro Rodríguez","dni": "30555666", "telefono": "1155550006", "email": "pedro@gmail.com", "activo": True},
        "30777888": {"nombre": "Lucía Fernández","dni": "30666777", "telefono": "1155550007", "email": "lucia@gmail.com", "activo": True},
        "30888999": {"nombre": "Diego Suárez", "dni": "30777888","telefono": "1155550008", "email": "diego@gmail.com", "activo": True},
        "30999000": {"nombre": "Marta Díaz","dni": "30999000", "telefono": "1155550009", "email": "marta@gmail.com", "activo": True},
        "31000111": {"nombre": "Jorge Silva","dni": "31000111", "telefono": "1155550010", "email": "jorge@gmail.com", "activo": True},
        }

    propiedades = {
        "P001": {"direccion": "Calle 123","propietario": "Juan Pérez", "tipo": "Departamento", "superficie": 75, "valor": 120000, "dni": "30111222","activo": True},
        "P002": {"direccion": "Av. 456","propietario": "María Gómez", "tipo": "Casa", "superficie": 150, "valor": 250000, "dni": "30222333","activo": True},
        "P003": {"direccion": "Diag. 789","propietario": "Carlos López", "tipo": "PH", "superficie": 90, "valor": 180000, "dni": "30333444","activo": True},
        "P004": {"direccion": "Las Heras 101","propietario": "Ana Torres", "tipo": "Casa", "superficie": 200, "valor": 310000, "dni": "30444555","activo": True},
        "P005": {"direccion": "San Martín 202","propietario": "Laura Méndez", "tipo": "Departamento", "superficie": 60, "valor": 95000, "dni": "30555666","activo": True},
        "P006": {"direccion": "Belgrano 303","propietario": "Pedro Rodríguez", "tipo": "PH", "superficie": 85, "valor": 150000, "dni": "30666777","activo": True},
        "P007": {"direccion": "Córdoba 404","propietario": "Lucía Fernández", "tipo": "Departamento", "superficie": 70, "valor": 110000, "dni": "30777888","activo": True},
        "P008": {"direccion": "Santa Fe 505","propietario": "Diego Suárez", "tipo": "Casa", "superficie": 180, "valor": 290000, "dni": "30888999","activo": True},
        "P009": {"direccion": "Rivadavia 606","propietario": "Marta Díaz", "tipo": "PH", "superficie": 95, "valor": 160000, "dni": "30999000","activo": True},
        "P010": {"direccion": "Mitre 707","propietario": "Jorge Silva", "tipo": "Departamento", "superficie": 55, "valor": 87000, "dni": "31000111","activo": True}
        }
    
    comisiones = [
        {"fecha": "2024.01.15 00:00:00", "codigo_propiedad": "P001", "monto": 3000, "tipo_operacion": "alquiler", "mes_anio": "ENE.24"},
        {"fecha": "2024.02.10 00:00:00", "codigo_propiedad": "P002", "monto": 12000, "tipo_operacion": "venta", "mes_anio": "FEB.24"},
        {"fecha": "2024.03.05 00:00:00", "codigo_propiedad": "P003", "monto": 5000, "tipo_operacion": "alquiler", "mes_anio": "MAR.24"},
        {"fecha": "2024.04.12 00:00:00", "codigo_propiedad": "P004", "monto": 15000, "tipo_operacion": "venta", "mes_anio": "ABR.24"},
        {"fecha": "2024.05.22 00:00:00", "codigo_propiedad": "P005", "monto": 3500, "tipo_operacion": "alquiler", "mes_anio": "MAY.24"},
        {"fecha": "2024.06.30 00:00:00", "codigo_propiedad": "P006", "monto": 10000, "tipo_operacion": "venta", "mes_anio": "JUN.24"},
        {"fecha": "2024.07.08 00:00:00", "codigo_propiedad": "P007", "monto": 4000, "tipo_operacion": "alquiler", "mes_anio": "JUL.24"},
        {"fecha": "2024.08.19 00:00:00", "codigo_propiedad": "P008", "monto": 13000, "tipo_operacion": "venta", "mes_anio": "AGO.24"},
        {"fecha": "2024.09.27 00:00:00", "codigo_propiedad": "P009", "monto": 4200, "tipo_operacion": "alquiler", "mes_anio": "SEP.24"},
        {"fecha": "2024.10.03 00:00:00", "codigo_propiedad": "P010", "monto": 9000, "tipo_operacion": "venta", "mes_anio": "OCT.24"},
    ]

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
                    propiedades = alta_propiedad(propiedades)
                    
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
                    resumen_anual_comisiones_cantidad(comisiones)
                
                elif opcionSubmenu == "3":   # Opción 3 del submenú
                    resumen_anual_comisiones_valor(comisiones)
                
                elif opcionSubmenu == "4":   # Opción 4 del submenú
                    informe()

                input("\nPresione ENTER para volver al menú.") # Pausa entre opciones
                print("\n\n")

        if opcionSubmenu != "0": # Pausa entre opciones. No la realiza si se vuelve de un submenú
            input("\nPresione ENTER para volver al menú.")
            print("\n\n")

# Punto de entrada al programa
main()
