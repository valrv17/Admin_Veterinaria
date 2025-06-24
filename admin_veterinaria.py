import sqlite3
import os

# --- Configuración de la Base de Datos ---

DB_NAME = "veterinaria.db"

def crear_base_datos():
    """
    Crea o se conecta a la base de datos SQLite y retorna la conexión y el cursor.
    Si el archivo de la DB existe, lo elimina para empezar limpio.
    """
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
        print(f"Base de datos anterior eliminada: {DB_NAME}")

    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    print(f"Base de datos creada/conectada: {DB_NAME}")
    return conexion, cursor

def crear_tablas(cursor):
    """
    Crea las tablas 'Dueños', 'Mascotas' y 'Consultas' en la base de datos.
    """
    # Tabla Dueños
    sql_crear_duenos = """
    CREATE TABLE IF NOT EXISTS Dueños (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        telefono TEXT,
        direccion TEXT
    );
    """
    cursor.execute(sql_crear_duenos)
    print("Tabla 'Dueños' creada exitosamente.")

    # Tabla Mascotas
    sql_crear_mascotas = """
    CREATE TABLE IF NOT EXISTS Mascotas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        especie TEXT,
        raza TEXT,
        edad INTEGER,
        id_dueño INTEGER,
        FOREIGN KEY (id_dueño) REFERENCES Dueños(id) ON DELETE CASCADE
    );
    """
    cursor.execute(sql_crear_mascotas)
    print("Tabla 'Mascotas' creada exitosamente.")

    # Tabla Consultas
    sql_crear_consultas = """
    CREATE TABLE IF NOT EXISTS Consultas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TEXT NOT NULL, -- Formato YYYY-MM-DD HH:MM:SS
        motivo TEXT NOT NULL,
        diagnostico TEXT,
        id_mascota INTEGER,
        FOREIGN KEY (id_mascota) REFERENCES Mascotas(id) ON DELETE CASCADE
    );
    """
    cursor.execute(sql_crear_consultas)
    print("Tabla 'Consultas' creada exitosamente.")

# --- Funciones de Inserción ---

def insertar_dueño(cursor, conexion, nombre, telefono, direccion):
    """Inserta un nuevo dueño en la tabla 'Dueños'."""
    sql = "INSERT INTO Dueños (nombre, telefono, direccion) VALUES (?, ?, ?)"
    try:
        cursor.execute(sql, (nombre, telefono, direccion))
        conexion.commit()
        print(f"Dueño '{nombre}' agregado. ID: {cursor.lastrowid}")
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Error al insertar dueño: {e}")
        return None

def insertar_mascota(cursor, conexion, nombre, especie, raza, edad, id_dueño):
    """Inserta una nueva mascota en la tabla 'Mascotas'."""
    sql = "INSERT INTO Mascotas (nombre, especie, raza, edad, id_dueño) VALUES (?, ?, ?, ?, ?)"
    try:
        cursor.execute(sql, (nombre, especie, raza, edad, id_dueño))
        conexion.commit()
        print(f"Mascota '{nombre}' agregada. ID: {cursor.lastrowid}")
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Error al insertar mascota: {e}")
        return None

def insertar_consulta(cursor, conexion, fecha, motivo, diagnostico, id_mascota):
    """Inserta una nueva consulta en la tabla 'Consultas'."""
    sql = "INSERT INTO Consultas (fecha, motivo, diagnostico, id_mascota) VALUES (?, ?, ?, ?)"
    try:
        cursor.execute(sql, (fecha, motivo, diagnostico, id_mascota))
        conexion.commit()
        print(f"Consulta para mascota ID {id_mascota} agregada. ID: {cursor.lastrowid}")
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Error al insertar consulta: {e}")
        return None

# --- Funciones de Consulta (Mostrar Datos) ---

def mostrar_dueños(cursor):
    """Muestra todos los dueños en la base de datos."""
    print("\n--- LISTADO DE DUEÑOS ---")
    cursor.execute("SELECT id, nombre, telefono, direccion FROM Dueños")
    dueños = cursor.fetchall()
    if dueños:
        for d in dueños:
            print(f"ID: {d[0]}, Nombre: {d[1]}, Teléfono: {d[2] or 'N/A'}, Dirección: {d[3] or 'N/A'}")
    else:
        print("No hay dueños registrados.")
    return dueños

def mostrar_mascotas(cursor, id_dueño=None):
    """Muestra todas las mascotas, opcionalmente filtradas por id_dueño."""
    print("\n--- LISTADO DE MASCOTAS ---")
    if id_dueño:
        sql = "SELECT m.id, m.nombre, m.especie, m.raza, m.edad, d.nombre FROM Mascotas m JOIN Dueños d ON m.id_dueño = d.id WHERE m.id_dueño = ?"
        cursor.execute(sql, (id_dueño,))
    else:
        sql = "SELECT m.id, m.nombre, m.especie, m.raza, m.edad, d.nombre FROM Mascotas m JOIN Dueños d ON m.id_dueño = d.id"
        cursor.execute(sql)
    mascotas = cursor.fetchall()
    if mascotas:
        for m in mascotas:
            print(f"ID: {m[0]}, Nombre: {m[1]}, Especie: {m[2]}, Raza: {m[3] or 'N/A'}, Edad: {m[4] or 'N/A'} años, Dueño: {m[5]}")
    else:
        print("No hay mascotas registradas." if not id_dueño else f"No hay mascotas para el Dueño ID {id_dueño}.")
    return mascotas

def mostrar_consultas(cursor, id_mascota=None):
    """Muestra todas las consultas, opcionalmente filtradas por id_mascota."""
    print("\n--- LISTADO DE CONSULTAS ---")
    if id_mascota:
        sql = "SELECT c.id, c.fecha, c.motivo, c.diagnostico, m.nombre FROM Consultas c JOIN Mascotas m ON c.id_mascota = m.id WHERE c.id_mascota = ?"
        cursor.execute(sql, (id_mascota,))
    else:
        sql = "SELECT c.id, c.fecha, c.motivo, c.diagnostico, m.nombre FROM Consultas c JOIN Mascotas m ON c.id_mascota = m.id"
        cursor.execute(sql)
    consultas = cursor.fetchall()
    if consultas:
        for c in consultas:
            print(f"ID: {c[0]}, Fecha: {c[1]}, Mascota: {c[4]}, Motivo: {c[2]}, Diagnóstico: {c[3] or 'N/A'}")
    else:
        print("No hay consultas registradas." if not id_mascota else f"No hay consultas para la Mascota ID {id_mascota}.")
    return consultas

# --- Funciones de Actualización ---

def actualizar_dueño(cursor, conexion, id_dueño, nombre=None, telefono=None, direccion=None):
    """Actualiza los datos de un dueño existente."""
    sets = []
    params = []
    if nombre is not None:
        sets.append("nombre = ?")
        params.append(nombre)
    if telefono is not None:
        sets.append("telefono = ?")
        params.append(telefono)
    if direccion is not None:
        sets.append("direccion = ?")
        params.append(direccion)

    if not sets:
        print("No hay campos para actualizar.")
        return False

    sql = f"UPDATE Dueños SET {', '.join(sets)} WHERE id = ?"
    params.append(id_dueño)
    try:
        cursor.execute(sql, tuple(params))
        conexion.commit()
        if cursor.rowcount > 0:
            print(f"Dueño ID {id_dueño} actualizado exitosamente.")
            return True
        else:
            print(f"No se encontró el Dueño ID {id_dueño}.")
            return False
    except sqlite3.Error as e:
        print(f"Error al actualizar dueño: {e}")
        return False

def actualizar_mascota(cursor, conexion, id_mascota, nombre=None, especie=None, raza=None, edad=None, id_dueño=None):
    """Actualiza los datos de una mascota existente."""
    sets = []
    params = []
    if nombre is not None:
        sets.append("nombre = ?")
        params.append(nombre)
    if especie is not None:
        sets.append("especie = ?")
        params.append(especie)
    if raza is not None:
        sets.append("raza = ?")
        params.append(raza)
    if edad is not None:
        sets.append("edad = ?")
        params.append(edad)
    if id_dueño is not None:
        sets.append("id_dueño = ?")
        params.append(id_dueño)

    if not sets:
        print("No hay campos para actualizar.")
        return False

    sql = f"UPDATE Mascotas SET {', '.join(sets)} WHERE id = ?"
    params.append(id_mascota)
    try:
        cursor.execute(sql, tuple(params))
        conexion.commit()
        if cursor.rowcount > 0:
            print(f"Mascota ID {id_mascota} actualizada exitosamente.")
            return True
        else:
            print(f"No se encontró la Mascota ID {id_mascota}.")
            return False
    except sqlite3.Error as e:
        print(f"Error al actualizar mascota: {e}")
        return False

def actualizar_consulta(cursor, conexion, id_consulta, fecha=None, motivo=None, diagnostico=None, id_mascota=None):
    """Actualiza los datos de una consulta existente."""
    sets = []
    params = []
    if fecha is not None:
        sets.append("fecha = ?")
        params.append(fecha)
    if motivo is not None:
        sets.append("motivo = ?")
        params.append(motivo)
    if diagnostico is not None:
        sets.append("diagnostico = ?")
        params.append(diagnostico)
    if id_mascota is not None:
        sets.append("id_mascota = ?")
        params.append(id_mascota)

    if not sets:
        print("No hay campos para actualizar.")
        return False

    sql = f"UPDATE Consultas SET {', '.join(sets)} WHERE id = ?"
    params.append(id_consulta)
    try:
        cursor.execute(sql, tuple(params))
        conexion.commit()
        if cursor.rowcount > 0:
            print(f"Consulta ID {id_consulta} actualizada exitosamente.")
            return True
        else:
            print(f"No se encontró la Consulta ID {id_consulta}.")
            return False
    except sqlite3.Error as e:
        print(f"Error al actualizar consulta: {e}")
        return False

# --- Funciones de Eliminación ---

def eliminar_registro(cursor, conexion, tabla, id_registro):
    """Función genérica para eliminar un registro de cualquier tabla."""
    sql = f"DELETE FROM {tabla} WHERE id = ?"
    try:
        cursor.execute(sql, (id_registro,))
        conexion.commit()
        if cursor.rowcount > 0:
            print(f"Registro ID {id_registro} eliminado de la tabla '{tabla}' exitosamente.")
            return True
        else:
            print(f"No se encontró el registro ID {id_registro} en la tabla '{tabla}'.")
            return False
    except sqlite3.Error as e:
        print(f"Error al eliminar registro de {tabla}: {e}")
        return False

# --- Funciones de Datos de Ejemplo (Opcional) ---

def insertar_datos_iniciales(cursor, conexion):
    """Inserta datos de ejemplo en las tablas."""
    print("\n--- Insertando datos de ejemplo ---")
    id_dueño1 = insertar_dueño(cursor, conexion, "Juan Pérez", "3101234567", "Calle Falsa 123")
    id_dueño2 = insertar_dueño(cursor, conexion, "María García", "3209876543", "Carrera Siempre Viva 742")

    if id_dueño1 and id_dueño2:
        id_mascota1 = insertar_mascota(cursor, conexion, "Fido", "Perro", "Labrador", 5, id_dueño1)
        id_mascota2 = insertar_mascota(cursor, conexion, "Luna", "Gato", "Siamés", 2, id_dueño1)
        id_mascota3 = insertar_mascota(cursor, conexion, "Coco", "Pájaro", "Periquito", 1, id_dueño2)

        if id_mascota1:
            insertar_consulta(cursor, conexion, "2025-06-05 10:00:00", "Chequeo Anual", "Todo en orden.", id_mascota1)
            insertar_consulta(cursor, conexion, "2025-06-08 14:30:00", "Vacunación", "Vacuna de refuerzo aplicada.", id_mascota1)
        if id_mascota2:
            insertar_consulta(cursor, conexion, "2025-06-07 11:00:00", "Problema respiratorio", "Bronquitis leve, tratamiento con antibióticos.", id_mascota2)

    print("Datos de ejemplo insertados.")

# --- Función Principal y Menú Interactivo ---

def mostrar_menu():
    """Muestra el menú principal de opciones."""
    print("\n\n--- MENÚ DE VETERINARIA ---")
    print("1. Insertar nuevo registro")
    print("2. Consultar y mostrar registros")
    print("3. Actualizar registro existente")
    print("4. Eliminar registro")
    print("5. Salir")

def mostrar_menu_insertar():
    """Muestra el submenú para insertar registros."""
    print("\n--- INSERTAR NUEVO REGISTRO ---")
    print("1. Insertar Dueño")
    print("2. Insertar Mascota")
    print("3. Insertar Consulta")
    print("4. Volver al menú principal")

def mostrar_menu_consultar():
    """Muestra el submenú para consultar registros."""
    print("\n--- CONSULTAR Y MOSTRAR REGISTROS ---")
    print("1. Mostrar todos los Dueños")
    print("2. Mostrar todas las Mascotas")
    print("3. Mostrar todas las Consultas")
    print("4. Mostrar Mascotas por Dueño ID")
    print("5. Mostrar Consultas por Mascota ID")
    print("6. Volver al menú principal")

def mostrar_menu_actualizar():
    """Muestra el submenú para actualizar registros."""
    print("\n--- ACTUALIZAR REGISTRO EXISTENTE ---")
    print("1. Actualizar Dueño")
    print("2. Actualizar Mascota")
    print("3. Actualizar Consulta")
    print("4. Volver al menú principal")

def mostrar_menu_eliminar():
    """Muestra el submenú para eliminar registros."""
    print("\n--- ELIMINAR REGISTRO ---")
    print("1. Eliminar Dueño")
    print("2. Eliminar Mascota")
    print("3. Eliminar Consulta")
    print("4. Volver al menú principal")

def main():
    """Función principal que ejecuta la aplicación de la veterinaria."""
    conexion, cursor = crear_base_datos()
    crear_tablas(cursor)
    insertar_datos_iniciales(cursor, conexion) # Para tener algunos datos al inicio

    while True:
        mostrar_menu()
        opcion_principal = input("Seleccione una opción: ")

        if opcion_principal == '1': # Insertar
            while True:
                mostrar_menu_insertar()
                opcion_insertar = input("Seleccione una opción de inserción: ")
                if opcion_insertar == '1':
                    nombre = input("Nombre del Dueño: ")
                    telefono = input("Teléfono del Dueño (opcional): ")
                    direccion = input("Dirección del Dueño (opcional): ")
                    insertar_dueño(cursor, conexion, nombre, telefono if telefono else None, direccion if direccion else None)
                elif opcion_insertar == '2':
                    nombre = input("Nombre de la Mascota: ")
                    especie = input("Especie de la Mascota: ")
                    raza = input("Raza de la Mascota (opcional): ")
                    try:
                        edad = int(input("Edad de la Mascota (años, opcional): ") or 0)
                    except ValueError:
                        print("Edad no válida. Se usará 0.")
                        edad = 0
                    id_dueño = input("ID del Dueño de la Mascota: ")
                    if id_dueño.isdigit():
                        insertar_mascota(cursor, conexion, nombre, especie, raza if raza else None, edad, int(id_dueño))
                    else:
                        print("ID de Dueño no válido.")
                elif opcion_insertar == '3':
                    fecha = input("Fecha de la Consulta (YYYY-MM-DD HH:MM:SS, ej: 2025-06-10 15:00:00): ")
                    motivo = input("Motivo de la Consulta: ")
                    diagnostico = input("Diagnóstico de la Consulta (opcional): ")
                    id_mascota = input("ID de la Mascota de la Consulta: ")
                    if id_mascota.isdigit():
                        insertar_consulta(cursor, conexion, fecha, motivo, diagnostico if diagnostico else None, int(id_mascota))
                    else:
                        print("ID de Mascota no válido.")
                elif opcion_insertar == '4':
                    break
                else:
                    print("Opción no válida.")

        elif opcion_principal == '2': # Consultar
            while True:
                mostrar_menu_consultar()
                opcion_consultar = input("Seleccione una opción de consulta: ")
                if opcion_consultar == '1':
                    mostrar_dueños(cursor)
                elif opcion_consultar == '2':
                    mostrar_mascotas(cursor)
                elif opcion_consultar == '3':
                    mostrar_consultas(cursor)
                elif opcion_consultar == '4':
                    id_d = input("Ingrese el ID del Dueño para ver sus mascotas: ")
                    if id_d.isdigit():
                        mostrar_mascotas(cursor, int(id_d))
                    else:
                        print("ID de Dueño no válido.")
                elif opcion_consultar == '5':
                    id_m = input("Ingrese el ID de la Mascota para ver sus consultas: ")
                    if id_m.isdigit():
                        mostrar_consultas(cursor, int(id_m))
                    else:
                        print("ID de Mascota no válido.")
                elif opcion_consultar == '6':
                    break
                else:
                    print("Opción no válida.")

        elif opcion_principal == '3': # Actualizar
            while True:
                mostrar_menu_actualizar()
                opcion_actualizar = input("Seleccione una opción de actualización: ")
                if opcion_actualizar == '1':
                    try:
                        id_d = int(input("ID del Dueño a actualizar: "))
                        nombre = input("Nuevo Nombre (dejar en blanco para no cambiar): ") or None
                        telefono = input("Nuevo Teléfono (dejar en blanco para no cambiar): ") or None
                        direccion = input("Nueva Dirección (dejar en blanco para no cambiar): ") or None
                        actualizar_dueño(cursor, conexion, id_d, nombre, telefono, direccion)
                    except ValueError:
                        print("ID de Dueño no válido.")
                elif opcion_actualizar == '2':
                    try:
                        id_m = int(input("ID de la Mascota a actualizar: "))
                        nombre = input("Nuevo Nombre (dejar en blanco para no cambiar): ") or None
                        especie = input("Nueva Especie (dejar en blanco para no cambiar): ") or None
                        raza = input("Nueva Raza (dejar en blanco para no cambiar): ") or None
                        edad_str = input("Nueva Edad (dejar en blanco para no cambiar): ")
                        edad = int(edad_str) if edad_str.isdigit() else None
                        id_dueño_str = input("Nuevo ID del Dueño (dejar en blanco para no cambiar): ")
                        id_dueño = int(id_dueño_str) if id_dueño_str.isdigit() else None
                        actualizar_mascota(cursor, conexion, id_m, nombre, especie, raza, edad, id_dueño)
                    except ValueError:
                        print("ID de Mascota o Edad/ID Dueño no válido.")
                elif opcion_actualizar == '3':
                    try:
                        id_c = int(input("ID de la Consulta a actualizar: "))
                        fecha = input("Nueva Fecha (YYYY-MM-DD HH:MM:SS, dejar en blanco para no cambiar): ") or None
                        motivo = input("Nuevo Motivo (dejar en blanco para no cambiar): ") or None
                        diagnostico = input("Nuevo Diagnóstico (dejar en blanco para no cambiar): ") or None
                        id_mascota_str = input("Nuevo ID de la Mascota (dejar en blanco para no cambiar): ")
                        id_mascota = int(id_mascota_str) if id_mascota_str.isdigit() else None
                        actualizar_consulta(cursor, conexion, id_c, fecha, motivo, diagnostico, id_mascota)
                    except ValueError:
                        print("ID de Consulta o ID Mascota no válido.")
                elif opcion_actualizar == '4':
                    break
                else:
                    print("Opción no válida.")

        elif opcion_principal == '4': # Eliminar
            while True:
                mostrar_menu_eliminar()
                opcion_eliminar = input("Seleccione una opción de eliminación: ")
                if opcion_eliminar == '1':
                    try:
                        id_d = int(input("ID del Dueño a eliminar: "))
                        eliminar_registro(cursor, conexion, "Dueños", id_d)
                    except ValueError:
                        print("ID de Dueño no válido.")
                elif opcion_eliminar == '2':
                    try:
                        id_m = int(input("ID de la Mascota a eliminar: "))
                        eliminar_registro(cursor, conexion, "Mascotas", id_m)
                    except ValueError:
                        print("ID de Mascota no válido.")
                elif opcion_eliminar == '3':
                    try:
                        id_c = int(input("ID de la Consulta a eliminar: "))
                        eliminar_registro(cursor, conexion, "Consultas", id_c)
                    except ValueError:
                        print("ID de Consulta no válido.")
                elif opcion_eliminar == '4':
                    break
                else:
                    print("Opción no válida.")

        elif opcion_principal == '5': # Salir
            break
        else:
            print("Opción principal no válida.")

    conexion.close()
    print("Conexión a la base de datos cerrada. ¡Hasta luego!")

if __name__ == "__main__":
    main()