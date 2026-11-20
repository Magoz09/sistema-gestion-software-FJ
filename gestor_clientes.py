"""
PARTE CLIENTE - SOFTWARE FJ (versión corregida, alineada con el archivo del líder)
Contiene: log, excepciones, Cliente (encapsulación) y GestorClientes (sobrecarga simulada).
Ejecutar:  python parte_cliente_corregida.py
"""

import logging
import re

# ============================================================
# 1. CONFIGURACIÓN DEL REGISTRO DE EVENTOS (LOG)
# ============================================================

ARCHIVO_LOG = "software_fj.log"

logging.basicConfig(
    filename=ARCHIVO_LOG,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)
log = logging.getLogger("SoftwareFJ")


# ============================================================
# 2. EXCEPCIONES PERSONALIZADAS
# ============================================================

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


# ============================================================
# 4. CLASE CLIENTE - ENCAPSULACIÓN
# ============================================================

class Cliente:
    def __init__(self, documento, nombre, telefono, correo):
        self.__documento = self._validar_texto(documento, "documento")
        self.__nombre = self._validar_nombre(nombre)
        self.__telefono = self._validar_telefono(telefono)
        self.__correo = self._validar_correo(correo)
        self.__reservas_activas = 0
        self.__activo = True

    @staticmethod
    def _validar_texto(valor, campo):
        if not isinstance(valor, str) or not valor.strip():
            raise DatosInvalidosError(f"El {campo} es obligatorio.")
        return valor.strip()

    @staticmethod
    def _validar_nombre(nombre):
        if not isinstance(nombre, str) or not nombre.strip():
            raise DatosInvalidosError("El nombre es obligatorio.")
        if not re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñÜü ]+", nombre.strip()):
            raise DatosInvalidosError("El nombre solo debe contener letras y espacios.")
        return nombre.strip()

    @staticmethod
    def _validar_telefono(telefono):
        telefono = Cliente._validar_texto(telefono, "teléfono")
        if not re.fullmatch(r"[0-9]{7,15}", telefono):
            raise DatosInvalidosError("El teléfono debe contener entre 7 y 15 dígitos.")
        return telefono

    @staticmethod
    def _validar_correo(correo):
        correo = Cliente._validar_texto(correo, "correo")
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", correo):
            raise DatosInvalidosError("El correo electrónico no tiene un formato válido.")
        return correo

    @property
    def documento(self):
        return self.__documento

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, nuevo_nombre):
        self.__nombre = self._validar_nombre(nuevo_nombre)

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, nuevo_telefono):
        self.__telefono = self._validar_telefono(nuevo_telefono)

    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, nuevo_correo):
        self.__correo = self._validar_correo(nuevo_correo)

    @property
    def reservas_activas(self):
        return self.__reservas_activas

    @property
    def activo(self):
        return self.__activo

    def desactivar(self):
        if self.__reservas_activas > 0:
            raise OperacionNoPermitidaError(
                "No se puede desactivar un cliente con reservas confirmadas."
            )
        self.__activo = False

    def activar(self):
        self.__activo = True

    def _agregar_reserva_confirmada(self):
        if not self.__activo:
            raise OperacionNoPermitidaError("El cliente está inactivo.")
        self.__reservas_activas += 1

    def _retirar_reserva_confirmada(self):
        if self.__reservas_activas > 0:
            self.__reservas_activas -= 1

    def validar(self):
        # La validación se realiza en el constructor y en las propiedades.
        return True

    def __str__(self):
        estado = "Activo" if self.activo else "Inactivo"
        return (
            f"Documento: {self.documento} | Nombre: {self.nombre} | "
            f"Teléfono: {self.telefono} | Correo: {self.correo} | "
            f"Reservas confirmadas: {self.reservas_activas} | Estado: {estado}"
        )


# ============================================================
# 5. GESTOR DE CLIENTES - SOBRECARGA SIMULADA
# ============================================================

class GestorClientes:
    def __init__(self):
        self._clientes = {}

    def registrar(self, *args, **kwargs):
        """
        Sobrecarga simulada:
        1) registrar(cliente)
        2) registrar(documento, nombre, telefono, correo)
        3) registrar(documento=..., nombre=..., telefono=..., correo=...)
        """
        try:
            if len(args) == 1 and isinstance(args[0], Cliente) and not kwargs:
                cliente = args[0]
            elif len(args) == 4 and not kwargs:
                cliente = Cliente(*args)
            elif not args:
                permitidos = {"documento", "nombre", "telefono", "correo"}
                desconocidos = set(kwargs) - permitidos
                if desconocidos:
                    raise DatosInvalidosError(
                        f"Argumentos desconocidos: {', '.join(desconocidos)}"
                    )
                faltantes = permitidos - set(kwargs)
                if faltantes:
                    raise DatosInvalidosError(
                        f"Faltan datos: {', '.join(sorted(faltantes))}"
                    )
                cliente = Cliente(
                    kwargs["documento"], kwargs["nombre"],
                    kwargs["telefono"], kwargs["correo"]
                )
            else:
                raise DatosInvalidosError(
                    "Forma de registro no válida. Use un objeto Cliente, "
                    "cuatro datos posicionales o los cuatro argumentos con nombre."
                )

            if cliente.documento in self._clientes:
                raise DatosInvalidosError(
                    f"El documento {cliente.documento} ya está registrado."
                )

            self._clientes[cliente.documento] = cliente
            log.info("Cliente registrado: %s", cliente.documento)
            return cliente

        except SoftwareFJError as error:
            log.warning("No se pudo registrar el cliente: %s", error)
            raise

    def actualizar(self, documento, *args, **kwargs):
        """
        Sobrecarga simulada:
        1) actualizar(documento, telefono="...")
        2) actualizar(documento, "telefono", "...")
        """
        cliente = self.buscar(documento)
        if cliente is None:
            raise DatosInvalidosError("El cliente no existe.")

        if len(args) == 2 and not kwargs:
            campo, valor = args
            kwargs = {campo: valor}
        elif args:
            raise DatosInvalidosError(
                "Use actualizar(documento, campo, valor) o "
                "actualizar(documento, campo=valor)."
            )

        permitidos = {"nombre", "telefono", "correo"}
        desconocidos = set(kwargs) - permitidos
        if desconocidos:
            raise OperacionNoPermitidaError(
                "No se permite modificar: " + ", ".join(desconocidos)
            )
        if not kwargs:
            raise DatosInvalidosError("Debe indicar al menos un dato para actualizar.")

        # Se validan los valores antes de aplicarlos.
        for campo, valor in kwargs.items():
            if campo == "nombre":
                cliente.nombre = valor
            elif campo == "telefono":
                cliente.telefono = valor
            elif campo == "correo":
                cliente.correo = valor

        log.info("Cliente actualizado: %s", documento)
        return True

    def buscar(self, documento):
        return self._clientes.get(str(documento).strip())

    def eliminar(self, documento):
        cliente = self.buscar(documento)
        if cliente is None:
            raise DatosInvalidosError("El cliente no existe.")
        if cliente.reservas_activas > 0:
            raise OperacionNoPermitidaError(
                "No se puede eliminar un cliente con reservas confirmadas."
            )
        del self._clientes[cliente.documento]
        log.info("Cliente eliminado: %s", documento)
        return True

    def listar(self):
        return list(self._clientes.values())



# ============================================================
# DEMOSTRACIÓN: operaciones válidas e inválidas (el programa nunca se detiene)
# ============================================================

def titulo(texto):
    print(f"\n=== {texto} ===")


def intentar(descripcion, funcion):
    """Ejecuta una operación; si falla con un error del sistema lo muestra y sigue."""
    titulo(descripcion)
    try:
        resultado = funcion()
        print("OK:", resultado)
    except SoftwareFJError as error:
        print("Error controlado:", error)
    except TypeError as error:  # p. ej. actualizar(documento=...) repite el argumento
        print("Error controlado (TypeError):", error)
        log.warning("TypeError controlado: %s", error)


if __name__ == "__main__":
    log.info("===== INICIO DEMO CLIENTES =====")
    gestor = GestorClientes()

    intentar("1. Registro válido (argumentos con nombre)", lambda: gestor.registrar(
        documento="1075123456", nombre="Sergio Yasno",
        telefono="3101234567", correo="sergio@mail.com"))
    intentar("2. Registro válido (objeto Cliente)", lambda: gestor.registrar(
        Cliente("52123456", "Maria Gomez", "3209876543", "maria@mail.com")))
    intentar("3. Correo inválido", lambda: gestor.registrar(
        documento="79123456", nombre="Pedro Ruiz",
        telefono="3001112233", correo="pedro-correo-malo"))
    intentar("4. Nombre con números", lambda: gestor.registrar(
        documento="80123456", nombre="Ana123",
        telefono="3001112233", correo="ana@mail.com"))
    intentar("5. Falta el teléfono", lambda: gestor.registrar(
        documento="91123456", nombre="Luis Mora", correo="luis@mail.com"))
    intentar("6. Documento duplicado", lambda: gestor.registrar(
        documento="1075123456", nombre="Otro Sergio",
        telefono="3151112233", correo="otro@mail.com"))
    intentar("7. Argumento desconocido", lambda: gestor.registrar(
        documento="63123456", nombre="Carla Diaz", telefono="3171112233",
        correo="carla@mail.com", edad=30))
    intentar("8. Actualización válida", lambda: gestor.actualizar(
        "1075123456", telefono="3112223344"))
    intentar("9. Actualización no permitida (documento)", lambda: gestor.actualizar(
        "1075123456", documento="999999"))
    intentar("10. Búsqueda de cliente inexistente", lambda: gestor.buscar("00000000"))
    intentar("11. Eliminación válida", lambda: gestor.eliminar("52123456"))

    def eliminar_con_reserva():
        cliente = gestor.buscar("1075123456")
        cliente._agregar_reserva_confirmada()
        return gestor.eliminar("1075123456")
    intentar("12. Eliminación no permitida (cliente con reservas)", eliminar_con_reserva)

    titulo("Clientes finales")
    for c in gestor.listar():
        print(c)
    log.info("===== FIN DEMO CLIENTES =====")
    print(f"\nProceso terminado sin interrupciones. Log en: {ARCHIVO_LOG}")
