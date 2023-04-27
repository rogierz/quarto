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

    @property
    def available_actions(self):
        available_actions = []
        for piece in self.available_pieces:
            for position in self.available_position:
                available_actions.append([piece, position])

        if len(self.available_pieces) == 0:
            available_actions.append([None, self.available_position[0]])
            return available_actions
        return available_actions

    def reset_all(self):
        self.reset()
        self.__init__()

    def set_players(self, players: tuple):
        super().set_players(players)
        players[0].set_moving_index(index=0)
        players[1].set_moving_index(index=1)
