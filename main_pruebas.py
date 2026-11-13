# main_pruebas.py
# Pruebas iniciales de integración del sistema Software FJ.
# Ejecutar: python main_pruebas.py

from sistema import Sistema
from logger import log, ARCHIVO_LOG


def titulo(texto):
    print("\n" + "=" * 58)
    print(texto)
    print("=" * 58)


def ejecutar_prueba(numero, descripcion, operacion, esperado=True):
    titulo(f"PRUEBA {numero}: {descripcion}")
    try:
        obtenido = operacion()
        if obtenido == esperado:
            print("Resultado: CORRECTO")
            log.info("Prueba %s (%s): correcta", numero, descripcion)
        else:
            print("Resultado: DIFERENTE A LO ESPERADO")
            print("Obtenido:", obtenido, "| Esperado:", esperado)
            log.warning("Prueba %s (%s): resultado inesperado", numero, descripcion)
    except Exception as error:
        print("Excepción controlada:", error)
        log.exception("Excepción durante prueba %s (%s)", numero, descripcion)


def main():
    log.info("========== INICIO DE PRUEBAS SOFTWARE FJ ==========")
    sistema = Sistema()

    ejecutar_prueba(1, "Registrar primer cliente",
        lambda: sistema.registrar_cliente(
            nombre="Sergio Yasno", documento="1075123456",
            telefono="3101234567", correo="sergio@mail.com"))

    ejecutar_prueba(2, "Registrar segundo cliente",
        lambda: sistema.registrar_cliente(
            nombre="Maria Gomez", documento="52123456",
            telefono="3209876543", correo="maria@mail.com"))

    ejecutar_prueba(3, "Registro sin nombre",
        lambda: sistema.registrar_cliente(
            documento="79123456", telefono="3001112233",
            correo="pedro@mail.com"), esperado=False)

    ejecutar_prueba(4, "Registro sin teléfono",
        lambda: sistema.registrar_cliente(
            nombre="Luis Mora", documento="91123456",
            correo="luis@mail.com"), esperado=False)

    ejecutar_prueba(5, "Documento duplicado",
        lambda: sistema.registrar_cliente(
            nombre="Otro Sergio", documento="1075123456",
            telefono="3151112233", correo="otro@mail.com"),
        esperado=False)

    ejecutar_prueba(6, "Buscar cliente existente",
        lambda: sistema.buscar_cliente("1075123456") is not None)

    ejecutar_prueba(7, "Buscar cliente inexistente",
        lambda: sistema.buscar_cliente("00000000") is None)

    ejecutar_prueba(8, "Actualizar teléfono",
        lambda: sistema.actualizar_cliente(
            "1075123456", telefono="3112223344"))

    ejecutar_prueba(9, "Intentar cambiar el documento",
        lambda: sistema.actualizar_cliente(
            "1075123456", documento="999999"), esperado=False)

    ejecutar_prueba(10, "Actualizar cliente inexistente",
        lambda: sistema.actualizar_cliente(
            "00000000", telefono="3005556677"), esperado=False)

    ejecutar_prueba(11, "Eliminar cliente sin reservas",
        lambda: sistema.eliminar_cliente("52123456"))

    def eliminar_con_reserva():
        cliente = sistema.buscar_cliente("1075123456")
        if cliente is None:
            return False
        cliente.agregar_reserva(1)
        return sistema.eliminar_cliente("1075123456")

    ejecutar_prueba(12, "Intentar eliminar cliente con reservas",
        eliminar_con_reserva, esperado=False)

    titulo("RESUMEN FINAL")
    sistema.mostrar_resumen()

    titulo("CLIENTES REGISTRADOS")
    for cliente in sistema.listar_clientes():
        print(cliente)

    log.info("========== FIN DE PRUEBAS SOFTWARE FJ ==========")
    print("\nFinalizaron las pruebas iniciales.")
    print("Archivo de eventos y errores:", ARCHIVO_LOG)


if __name__ == "__main__":
    main()
