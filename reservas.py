7. CLASE RESERVA Y GESTOR DE RESERVAS
# ============================================================

class Reserva(Entidad):
    IVA = 0.19
    DESCUENTO = 0.10

    def __init__(self, identificador, cliente, servicio, estado="Pendiente"):
        super().__init__(identificador)
        self.cliente = cliente
        self.servicio = servicio
        self.estado = estado
        self.costo_total = 0.0
        self.validar()

    def validar(self):
        if not isinstance(self.cliente, Cliente):
            raise DatosInvalidosError("Debe seleccionar un cliente válido.")
        if not self.cliente.activo:
            raise ReservaError("El cliente no está activo.")
        if not isinstance(self.servicio, Servicio):
            raise DatosInvalidosError("Debe seleccionar un servicio válido.")
        if self.estado not in ("Pendiente", "Confirmada", "Cancelada"):
            raise DatosInvalidosError("El estado de la reserva no es válido.")

    def confirmar(self):
        if self.estado != "Pendiente":
            raise OperacionNoPermitidaError(
                f"No se puede confirmar una reserva en estado {self.estado}."
            )
        if not self.servicio.disponible:
            raise ServicioNoDisponibleError("El servicio no está disponible.")

        costo_base = self.servicio.calcular_costo()
        self.costo_total = round(
            costo_base * (1 - self.DESCUENTO) * (1 + self.IVA), 2
        )
        self.estado = "Confirmada"
        self.cliente._agregar_reserva_confirmada()
        self.servicio.cambiar_disponibilidad(False)
        log.info("Reserva %s confirmada. Total: $%.2f", self.identificador, self.costo_total)
        return self.costo_total

    def cancelar(self):
        if self.estado == "Cancelada":
            raise OperacionNoPermitidaError("La reserva ya está cancelada.")
        if self.estado == "Confirmada":
            self.cliente._retirar_reserva_confirmada()
            self.servicio.cambiar_disponibilidad(True)
        self.estado = "Cancelada"
        log.info("Reserva %s cancelada.", self.identificador)
        return True

    def __str__(self):
        return (
            f"{self.identificador} | Cliente: {self.cliente.nombre} "
            f"({self.cliente.documento}) | Servicio: "
            f"{self.servicio.describir_servicio()} | Estado: {self.estado} "
            f"| Total: ${self.costo_total:,.2f}"
        )


class GestorReservas:
    def __init__(self):
        self._reservas = {}

    def crear_reserva(self, identificador, cliente, servicio):
        if identificador in self._reservas:
            raise ReservaError("Ya existe una reserva con ese identificador.")
        reserva = Reserva(identificador, cliente, servicio)
        self._reservas[identificador] = reserva
        log.info("Reserva %s creada.", identificador)
        return reserva

    def buscar(self, identificador):
        return self._reservas.get(identificador)

    def listar(self):
        return list(self._reservas.values())
