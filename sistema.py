# sistema.py
# Punto 5: integración inicial de Software FJ.
# Coordina las operaciones usando los módulos existentes del proyecto.

from gestor_clientes import GestorClientes
from logger import log


class Sistema:
    def __init__(self):
        self.gestor_clientes = GestorClientes()

        # Integración provisional: se conectarán las clases reales
        # cuando se conozcan las interfaces de servicios.py y reservas.py.
        self.servicios = []
        self.reservas = []

        log.info("Sistema Software FJ iniciado")

    def registrar_cliente(self, **datos):
        try:
            resultado = self.gestor_clientes.registrar(**datos)

            if resultado:
                log.info("Cliente registrado correctamente")
            else:
                log.warning("No se pudo registrar el cliente")

            return resultado

        except Exception:
            log.exception("Error al registrar cliente")
            raise

    def buscar_cliente(self, documento):
        cliente = self.gestor_clientes.buscar(documento)

        if cliente is None:
            log.warning("Cliente no encontrado: %s", documento)

        return cliente

    def actualizar_cliente(self, documento_actual, **datos):
        # documento_actual identifica al cliente que se va a actualizar.
        # Los demás campos se envían al gestor de clientes.
        resultado = self.gestor_clientes.actualizar(
            documento_actual, **datos
        )

        if resultado:
            log.info("Cliente %s actualizado", documento_actual)
        else:
            log.warning(
                "No se pudo actualizar el cliente %s",
                documento_actual
            )

        return resultado

    def eliminar_cliente(self, documento):
        resultado = self.gestor_clientes.eliminar(documento)

        if resultado:
            log.info("Cliente %s eliminado", documento)
        else:
            log.warning("No se pudo eliminar el cliente %s", documento)

        return resultado

    def listar_clientes(self):
        return self.gestor_clientes.listar()

    # Métodos provisionales hasta conocer la interfaz de servicios.py.
    def agregar_servicio(self, servicio):
        if servicio is None:
            raise ValueError("El servicio no puede estar vacío")

        self.servicios.append(servicio)
        log.info("Objeto de servicio agregado")
        return True

    def listar_servicios(self):
        return list(self.servicios)

    # Métodos provisionales hasta conocer la interfaz de reservas.py.
    def agregar_reserva(self, reserva):
        if reserva is None:
            raise ValueError("La reserva no puede estar vacía")

        self.reservas.append(reserva)
        log.info("Objeto de reserva agregado")
        return True

    def listar_reservas(self):
        return list(self.reservas)

    def mostrar_resumen(self):
        print("\n========== SOFTWARE FJ ==========")
        print("Clientes:", len(self.listar_clientes()))
        print("Servicios cargados:", len(self.listar_servicios()))
        print("Reservas cargadas:", len(self.listar_reservas()))
        print("=================================")
