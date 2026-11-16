from abc import abstractmethod

from main import Entidad, DatosInvalidosError


class Servicio(Entidad):
#este metodo es obligatorio para las clases hijas.
    @abstractmethod
#cada servicio tendra su propia manera de calcular el precio
    def calcular_costo(self):
        pass

    @abstractmethod
#cada servicio explicara que ofrece
    def describir_servicio(self):
        pass

    @abstractmethod
#cada servicio comprobara que sus datos sean correctos
    def validar(self):
        pass
    
#creamos la primera clase implementando un constructor para asi recibir el identificador, las horas y la tarifa que se hereda de servicio    
class ReservaSalas(Servicio):

#aqui iniciamos el metodo que empieza el objeto y llamamos la clase padre entidad
    def __init__(self, identificador, horas, tarifa_por_hora):
        super().__init__(identificador)
        self.horas = horas   # aqui guardamos las horas reservadas
        self.tarifa_por_hora = tarifa_por_hora  # aqui guardamos el precio por hora
        self.validar()

# se multiplica las horas segun la tarifa
    def calcular_costo(self):
        return self.horas * self.tarifa_por_hora

# nos regresara una descripcion de la reserva
    def describir_servicio(self):
        return f"Reserva de sala por {self.horas} horas."

# comprobamos que las horas y la tarifa sean mayores que cero
    def validar(self):
        if not isinstance(self.horas, (int, float)) or self.horas <= 0:
            raise DatosInvalidosError("Las horas deben ser mayores que cero.")

        if not isinstance(self.tarifa_por_hora, (int, float)) or self.tarifa_por_hora <= 0:
            raise DatosInvalidosError("La tarifa debe ser mayor que cero.")
        
# creamos la segunda clase para poder registrar el equipo que se alquila heredada de nuestra clase abstracta
class AlquilerEquipos(Servicio):

    def __init__(self, identificador, equipo, dias, tarifa_por_dia):
        super().__init__(identificador)
        self.equipo = equipo  # se guardara el nombre del equipo
        self.dias = dias    # se guardara la cantidad de dias alquilado
        self.tarifa_por_dia = tarifa_por_dia   # se guarda el precio por dia
        self.validar()

# se multiplica los dias por la tarifa diaria
    def calcular_costo(self):
        return self.dias * self.tarifa_por_dia

# mostrara el equipo que se alquilo y el tiempo
    def describir_servicio(self):
        return f"Alquiler de {self.equipo} por {self.dias} días."

# comprueba que la informacion del equipo, los dias y la tarifa esten bien
    def validar(self):
        if not isinstance(self.equipo, str) or not self.equipo.strip():
            raise DatosInvalidosError("Debe indicar el equipo que desea alquilar.")

        if not isinstance(self.dias, (int, float)) or self.dias <= 0:
            raise DatosInvalidosError("Los días deben ser mayores que cero.")

        if not isinstance(self.tarifa_por_dia, (int, float)) or self.tarifa_por_dia <= 0:
            raise DatosInvalidosError("La tarifa diaria debe ser mayor que cero.")
        
# creamos la tercera clase para la asesoria heredada de nuestra clase obstracta        
class ConsultoriaEspecializada(Servicio):

    def __init__(self, identificador, tema, horas, tarifa_por_hora):
        super().__init__(identificador)
        self.tema = tema   # se guardara el tema de la asesoria
        self.horas = horas    # indica cuanto tiempo dura
        self.tarifa_por_hora = tarifa_por_hora    # indica el valor por hora
        self.validar()

# multiplica las horas por la tarifa
    def calcular_costo(self):
        return self.horas * self.tarifa_por_hora

# explicara el tipo de consultoria
    def describir_servicio(self):
        return f"Consultoria especializada en {self.tema}, durante {self.horas} horas."

# comprobamos que los datos sean correctos
    def validar(self):
        if not isinstance(self.tema, str) or not self.tema.strip():
            raise DatosInvalidosError("Debe indicar el tema de la consultoría.")

        if not isinstance(self.horas, (int, float)) or self.horas <= 0:
            raise DatosInvalidosError("Las horas deben ser mayores que cero.")

        if not isinstance(self.tarifa_por_hora, (int, float)) or self.tarifa_por_hora <= 0:
            raise DatosInvalidosError("La tarifa por hora debe ser mayor que cero.")