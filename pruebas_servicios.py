from servicios import (
    ReservaSalas,
    AlquilerEquipos,
    ConsultoriaEspecializada
)

# Creamos un objeto para cada servicio

sala = ReservaSalas("S001", 3, 50000)

equipo = AlquilerEquipos("E001", "Computador", 2, 30000)

consultoria = ConsultoriaEspecializada("C001", "Sistemas", 4, 40000)

# Mostramos la descripcion y el costo de cada servicio

servicios = [sala, equipo, consultoria]

for servicio in servicios:
    print(servicio.describir_servicio())
    print("Costo del servicio: $", servicio.calcular_costo())
    print("------------------------------")