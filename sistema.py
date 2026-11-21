class Sistema:
    def __init__(self):
        self.gestor_clientes = GestorClientes()
        self.gestor_reservas = GestorReservas()
        self.servicios = {}
        self._cargar_servicios_iniciales()
        log.info("Sistema Software FJ iniciado.")

    def _cargar_servicios_iniciales(self):
        servicios_iniciales = [
            ReservaSalas("S001", 3, 50000),
            AlquilerEquipos("E001", "Computador", 2, 30000),
            ConsultoriaEspecializada("C001", "Sistemas", 4, 40000)
        ]
        for servicio in servicios_iniciales:
            self.servicios[servicio.identificador] = servicio

    def registrar_cliente(self, *args, **kwargs):
        return self.gestor_clientes.registrar(*args, **kwargs)

    def buscar_cliente(self, documento):
        return self.gestor_clientes.buscar(documento)

    def actualizar_cliente(self, documento, *args, **kwargs):
        return self.gestor_clientes.actualizar(documento, *args, **kwargs)

    def eliminar_cliente(self, documento):
        return self.gestor_clientes.eliminar(documento)

    def listar_clientes(self):
        return self.gestor_clientes.listar()

    def listar_servicios(self):
        return list(self.servicios.values())

    def crear_reserva(self, id_reserva, documento_cliente, id_servicio):
        cliente = self.buscar_cliente(documento_cliente)
        servicio = self.servicios.get(id_servicio)
        if cliente is None:
            raise DatosInvalidosError("No se encontró el cliente indicado.")
        if servicio is None:
            raise DatosInvalidosError("No se encontró el servicio indicado.")
        return self.gestor_reservas.crear_reserva(id_reserva, cliente, servicio)

    def confirmar_reserva(self, id_reserva):
        reserva = self.gestor_reservas.buscar(id_reserva)
        if reserva is None:
            raise ReservaError("No se encontró la reserva.")
        return reserva.confirmar()

    def cancelar_reserva(self, id_reserva):
        reserva = self.gestor_reservas.buscar(id_reserva)
        if reserva is None:
            raise ReservaError("No se encontró la reserva.")
        return reserva.cancelar()

    def listar_reservas(self):
        return self.gestor_reservas.listar()

    def mostrar_resumen(self):
        print("\n========== RESUMEN SOFTWARE FJ ==========")
        print("Clientes registrados:", len(self.listar_clientes()))
        print("Servicios disponibles:", len(self.listar_servicios()))
        print("Reservas registradas:", len(self.listar_reservas()))
        print("=========================================")
