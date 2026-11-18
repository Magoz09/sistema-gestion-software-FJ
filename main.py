from abc import ABC, abstractmethod
import logging
import re

# 1 CONFIGURACION DEL REGISTRO DE EVENTOS (LOGS)

ARCHIVO_LOG = "software_fj.log"

logging.basicConfig(
    filename = ARCHIVO_log,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8")

log = logging.getLogger("SoftwareFJ")

# 2 EXCEPCIONES PERSONALIZADAS

class SoftwareFJError(Exception):
     """Excepción base del sistema."""

class DatosInvalidosError(SoftwareFJError):
    """Se utiliza cuando los datos ingresados no son válidos."""


class ServicioNoDisponibleError(SoftwareFJError):
    """Se utiliza cuando un servicio no está disponible."""


class ReservaError(SoftwareFJError):
    """Se utiliza cuando ocurre un problema con una reserva."""


class OperacionNoPermitidaError(SoftwareFJError):
    """Se utiliza cuando una operación no está permitida."""

  # 3 CLASE ABSTRACTA ENTIDAD

class Entidad(ABC):

    def __init__(self, identificador):
        if not identificador:
            raise DatosInvalidosError(
                "El identificador es obligatorio."
            )

        self.identificador = identificador

    @abstractmethod
    def validar(self):
        pass
