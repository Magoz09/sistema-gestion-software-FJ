"""
main.py
Simulación del módulo de CLIENTES de Software FJ.
Ejecuta operaciones válidas e inválidas y demuestra que el programa nunca se detiene.

Ejecutar:  python main.py
"""

from gestor_clientes import GestorClientes
from logger import ARCHIVO_LOG, log


def titulo(texto: str) -> None:
    """Imprime un encabezado para separar las operaciones."""
    print(f"\n=== {texto} ===")


def main() -> None:
    log.info("========== INICIO DE SIMULACIÓN: MÓDULO CLIENTES ==========")
    gestor = GestorClientes()

    # 1. Registro válido
    titulo("1. Registro válido")
    c1 = gestor.registrar(nombre="Sergio Yasno", documento="1075123456",
                          correo="sergio@mail.com", telefono="3101234567")
    print(c1 if c1 else "FALLÓ")

    # 2. Registro válido
    titulo("2. Registro válido")
    c2 = gestor.registrar(nombre="María Gómez", documento="52123456",
                          correo="maria.gomez@mail.com", telefono="3209876543")
    print(c2 if c2 else "FALLÓ")

    # 3. Correo inválido
    titulo("3. Registro inválido: correo sin formato")
    print(gestor.registrar(nombre="Pedro Ruiz", documento="79123456",
                           correo="pedro-correo-malo", telefono="3001112233") or "FALLÓ (registrado en log)")

    # 4. Nombre con números
    titulo("4. Registro inválido: nombre con números")
    print(gestor.registrar(nombre="Ana123", documento="80123456",
                           correo="ana@mail.com", telefono="3001112233") or "FALLÓ (registrado en log)")

    # 5. Parámetro faltante
    titulo("5. Registro inválido: falta el teléfono")
    print(gestor.registrar(nombre="Luis Mora", documento="91123456",
                           correo="luis@mail.com") or "FALLÓ (registrado en log)")

    # 6. Documento duplicado
    titulo("6. Registro inválido: documento duplicado")
    print(gestor.registrar(nombre="Otro Sergio", documento="1075123456",
                           correo="otro@mail.com", telefono="3151112233") or "FALLÓ (registrado en log)")

    # 7. Parámetro desconocido (TypeError encadenado)
    titulo("7. Registro inválido: argumento desconocido (excepción encadenada)")
    print(gestor.registrar(nombre="Carla Díaz", documento="63123456", correo="carla@mail.com",
                           telefono="3171112233", edad=30) or "FALLÓ (registrado en log)")

    # 8. Actualización válida
    titulo("8. Actualización válida de teléfono")
    print("OK" if gestor.actualizar("1075123456", telefono="3112223344") else "FALLÓ")

    # 9. Actualización no permitida
    titulo("9. Actualización no permitida: cambiar documento")
    print("OK" if gestor.actualizar("1075123456", documento="999999") else "FALLÓ (registrado en log)")

    # 10. Búsqueda de cliente inexistente
    titulo("10. Búsqueda de cliente inexistente")
    try:
        gestor.buscar("00000000")
    except Exception as e:  # noqa: BLE001 - demostración
        print(f"Capturado: {e}")
        log.error("Búsqueda fallida: %s", e)

    # 11. Eliminación válida
    titulo("11. Eliminación de cliente sin reservas")
    print("OK" if gestor.eliminar("52123456") else "FALLÓ")

    # 12. Eliminación con reservas (no permitida)
    titulo("12. Eliminación no permitida: cliente con reservas")
    cliente = gestor.buscar("1075123456")
    if cliente:
        cliente.agregar_reserva(1)
    print("OK" if gestor.eliminar("1075123456") else "FALLÓ (registrado en log)")

    titulo("Clientes finales en memoria")
    for c in gestor.listar():
        print(c)

    log.info("========== FIN DE SIMULACIÓN: el programa siguió estable ==========")
    print(f"\nProceso terminado sin interrupciones. Revisa el log en:\n{ARCHIVO_LOG}")


if __name__ == "__main__":
    main()