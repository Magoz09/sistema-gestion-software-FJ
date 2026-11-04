from abc import ABC, abstractmethod
import logging

# 1 CONFIGURACION DEL ARCHIVO DE LOGS

logging.basicConfig(
    filename="software_fj.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"

  # 2 EXCEPCIONES PERSONALIZADAS

  class SoftwareFJError(Exception):
    pass


class DatosInvalidosError(SoftwareFJError):
    pass


class ServicioNoDisponibleError(SoftwareFJError):
    pass


class ReservaError(SoftwareFJError):
    pass


class OperacionNoPermitidaError(SoftwareFJError):
    pass

  
