
class Poteau:
    """Représente un poteau pour le Funibot"""

    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f"Poteau (x={self.x}; y={self.y}; z={self.z})"