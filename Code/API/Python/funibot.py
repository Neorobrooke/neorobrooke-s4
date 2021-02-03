
class Position:
    def __init__(self, x, y, z) -> None:
        self.x = x
        self.y = y
        self.z = z
    
    def __repr__(self) -> str:
        return f"({self.x};{self.y};{self.z}"

class Poteau:
    """Représente un pôle du Funibot"""
    def __init__(self, nom, position = Position(0,0,0)) -> None:
        self.nom = nom
        self.pos = position

    def __repr__(self) -> str:
        return f"Poteau[{self.nom}]{self.pos}"

class Funibot:
    """Représente le Funibot"""
    
    def __init__(self, port_serie , poteaux: dict[str, Poteau]) -> None:
        pass

