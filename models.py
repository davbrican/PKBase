class Pokemon():
    def __init__(self, id, nombre, tipos, salud, ataque, defensa, ataque_especial, defensa_especial, total):
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
        return self.id + " - " + self.nombre + "\nT: " + str(self.tipos) + "\n\nAtaque: " + str(self.ataque) + "\nDefensa: " + str(self.defensa)+ "\nAtaque Especial: " + str(self.ataque_especial)+ "\nDefensa Especial: " + str(self.defensa_especial) + "\n\nTotal: " + str(self.total)