class PrecomputedMoveData:

    def __init__(self):
        self.num_squares_to_edge = [[0 for _ in range(8)] for _ in range(64)]

        # Iterate through the board
        for file in range(8):
            for rank in range(8):
                # Find distance from edge and store in array
                numNorth = 7 - rank
                numSouth = rank
                numWest = file
                numEast = 7 - file
                squareIndex = rank * 8 + file
                moveData = [
                    numNorth, numSouth, numEast, numWest,
                    min(numNorth, numWest), min(numSouth, numEast),
                    min(numNorth, numEast), min(numSouth, numWest)
                ]
                self.num_squares_to_edge[squareIndex] = moveData
