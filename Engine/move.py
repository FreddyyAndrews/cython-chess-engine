class Move:

    starting_sqaure: int = None
    end_square: int = None

    def __init__(self, starting_square: int, end_sqaure: int) -> None:
        self.starting_sqaure = starting_square
        self.end_square = end_sqaure
