from quarto import quarto

class Quarto(quarto.Quarto):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.available_position = [(i, j) for i in range(4) for j in range(4)]
        self.available_pieces = [i for i in range(16)]
    
    def select(self, pieceIndex: int) -> bool:
        selected = super().select(pieceIndex)
        if selected:
            self.available_pieces.remove(pieceIndex)
        return selected
    
    def place(self, x: int, y: int) -> bool:
        placed = super().place(x, y)
        if placed:
            self.available_position.remove((x, y))
        return placed