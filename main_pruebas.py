# main_pruebas.py
# Pruebas iniciales de integración del sistema Software FJ.
# Ejecutar: python main_pruebas.py

def ejecutar_pruebas():
    print("\n========== PRUEBAS AUTOMÁTICAS ==========")
    sistema = Sistema()
    correctas = 0
    total = 0

    def comprobar(descripcion, funcion, esperado=True):
        nonlocal correctas, total
        total += 1
        try:
            resultado = funcion()
            if resultado == esperado:
                correctas += 1
                print(f"[CORRECTA] {descripcion}")
            else:
                print(f"[REVISAR] {descripcion} | Resultado: {resultado}")
        except Exception as error:
            print(f"[ERROR CONTROLADO] {descripcion} | {error}")

    comprobar(
        "Registro de cliente con argumentos nombrados",
        lambda: sistema.registrar_cliente(
            documento="1075123456", nombre="Sergio Yasno",
            telefono="3101234567", correo="sergio@mail.com"
        ).documento == "1075123456"
    )

    comprobar(
        "Registro de cliente mediante objeto (sobrecarga)",
        lambda: sistema.registrar_cliente(
            Cliente("52123456", "Maria Gomez", "3209876543", "maria@mail.com")
        ).documento == "52123456"
    )

    comprobar(
        "Registro duplicado rechazado",
        lambda: _probar_error(
            lambda: sistema.registrar_cliente(
                documento="1075123456", nombre="Otro Sergio",
                telefono="3151112233", correo="otro@mail.com"
            )
        )
    )

    comprobar(
        "Búsqueda de cliente existente",
        lambda: sistema.buscar_cliente("1075123456") is not None
    )

    comprobar(
        "Actualización de teléfono con argumentos nombrados",
        lambda: sistema.actualizar_cliente(
            "1075123456", telefono="3112223344"
        )
    )

    comprobar(
        "Actualización con campo y valor (sobrecarga)",
        lambda: sistema.actualizar_cliente(
            "1075123456", "correo", "sergio.nuevo@mail.com"
        )
    )

    comprobar(
        "Cambio de documento no permitido",
        lambda: _probar_error(
            lambda: sistema.actualizar_cliente(
                "1075123456", documento="999999"
            )
        )
    )

    comprobar(
        "Creación y confirmación de reserva",
        lambda: _probar_reserva(sistema)
    )

    comprobar(
        "Cliente con reserva confirmada no se puede eliminar",
        lambda: _probar_error(lambda: sistema.eliminar_cliente("1075123456"))
    )

    comprobar(
        "Cancelación de reserva libera al cliente y al servicio",
        lambda: _probar_cancelacion(sistema)
    )

    print("----------------------------------------")
    print(f"Resultado: {correctas} de {total} pruebas correctas.")
    print("Archivo de registro:", ARCHIVO_LOG)
    print("========================================")


def _probar_error(funcion):
    try:
        funcion()
    except SoftwareFJError:
        return True
    return False


def _probar_reserva(sistema):
    reserva = sistema.crear_reserva("R001", "1075123456", "S001")
    total = sistema.confirmar_reserva("R001")
    return reserva.estado == "Confirmada" and total > 0


def _probar_cancelacion(sistema):
    sistema.cancelar_reserva("R001")
    cliente = sistema.buscar_cliente("1075123456")
    servicio = sistema.servicios["S001"]
    return (
        sistema.gestor_reservas.buscar("R001").estado == "Cancelada"
        and cliente.reservas_activas == 0
        and servicio.disponible
    )

