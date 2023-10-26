from Engine.move import Move


class Castle(Move):

    wk_castle: bool = None
    wq_castle: bool = None
    bk_castle: bool = None
    bq_castle: bool = None

    def __init__(self, wk_castle: bool = False, wq_castle: bool = False, bk_castle: bool = False, bq_castle: bool = False) -> None:
        self.wk_castle = wk_castle
        self.wq_castle = wq_castle
        self.bk_castle = bk_castle
        self.bq_castle = bq_castle
