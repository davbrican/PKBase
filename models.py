from _typeshed import Self


class Pokemon():
    id = ""
    nombre = ""
    tipos = []
    salud = 0
    ataque = 0
    defensa = 0
    ataque_especial = 0
    defensa_especial = 0
    total = 0

    def __init__(self, id, nombre, tipos, salud, ataque, defensa, ataque_especial, defensa_especial, total):
        super().__init__(id, nombre, tipos, salud, ataque, defensa, ataque_especial, defensa_especial, total)
        self.id = id
        self.nombre = nombre
        self.tipos = tipos
        self.salud = salud
        self.ataque = ataque
        self.defensa = defensa
        self.ataque_especial = ataque_especial
        self.defensa_especial = defensa_especial
        self.total = total

    def __str__(self) -> str:
        return self.id + " - " + self.nombre + " T: " + self.tipos + "\n Ataque: " + self.ataque + "\n Defensa: " + self.defensa+ "\n Ataque Especial: " + self.ataque_especial+ "\n Defensa Especial: " + self.defensa_especial + "\n\n Total: " + self.total