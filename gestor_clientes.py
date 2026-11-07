class Cliente:
    def __init__(self, documento, nombre, telefono, correo):
        self.documento = documento
        self.nombre = nombre
        self.telefono = telefono
        self.correo = correo
        self.reservas = 0
        self.activo = True

    def agregar_reserva(self, cantidad=1):
        self.reservas += cantidad

    def __str__(self):
        return f"{self.documento} - {self.nombre}"

class GestorClientes:
    def __init__(self):
        self.clientes = {}

    def agregar(self, cliente):
        if cliente.documento in self.clientes:
            print(f"FALLÓ: documento {cliente.documento} ya existe")
            return False
        if not cliente.documento or not cliente.nombre:
            print("FALLÓ: datos incompletos")
            return False
        self.clientes[cliente.documento] = cliente
        return True

    def registrar(self, nombre=None, documento=None, telefono=None, correo=None, **kwargs):
        if kwargs:
            print(f"FALLÓ: argumento desconocido {list(kwargs.keys())}")
            return False
        if not nombre or not documento or not telefono or not correo:
            print(f"FALLÓ: falta un parámetro para registrar {documento}")
            return False
        cliente = Cliente(documento, nombre, telefono, correo)
        return self.agregar(cliente)
    def actualizar(self, *args, **kwargs):
        if len(args) != 1 or "documento" in kwargs:
            print("FALLÓ: documento duplicado o faltante en actualizar")
            return False
        documento = args[0]
        cliente = self.clientes.get(documento)
        if not cliente:
            print(f"FALLÓ: cliente {documento} no existe")
            return False
        permitidos = {"nombre", "telefono", "correo", "activo"}
        desconocidos = set(kwargs.keys()) - permitidos
        if desconocidos:
            print(f"FALLÓ: argumento desconocido {list(desconocidos)}")
            return False
        for clave, valor in kwargs.items():
            setattr(cliente, clave, valor)
        return True

    def buscar(self, documento):
        return self.clientes.get(documento)

    def eliminar(self, documento):
        cliente = self.clientes.get(documento)
        if not cliente:
            print(f"FALLÓ: cliente {documento} no existe")
            return False
        if cliente.reservas > 0:
            print(f"FALLÓ: cliente {documento} tiene reservas")
            return False
        del self.clientes[documento]
        return True

    def listar(self):
        return list(self.clientes.values())