from src.Settings import *
from src.interface.Color import *
from src.interface.Board import *
from src.interface.Pawn import *
from src.player.Human import *
from src.action.PawnMove import *
from src.action.FencePlacing import *
from src.Path import *

import random


class Game:
    DefaultColorForPlayer = [
        Color.BLACK,
        Color.BLUE,
        Color.RED,
        Color.ORANGE
    ]

    DefaultNameForPlayer = [
        "1",
        "2",
        "3",
        "4"
    ]

    def __init__(self, players, cols=9, rows=9, totalFenceCount=20,
                 squareSize=40, innerSize=None):
        if innerSize is None:
            innerSize = int(squareSize / 8)
        self.totalFenceCount = totalFenceCount
        # TODO = CREAR INSTANCIA DE AREA
        board = Board(self, cols, rows, squareSize, innerSize)

        playerCount = min(int(len(players) / 2) * 2, 4)
        self.players = []

        for num_player in range(playerCount):

            # TODO = Seteamos a los jugaodres en caso no tengan nombre
            if players[num_player].name is None:
                players[num_player].name = Game.DefaultNameForPlayer[num_player]
            if players[num_player].color is None:
                players[num_player].color = Game.DefaultColorForPlayer[
                    num_player]

            # TODO = Inicializamos jugador
            players[num_player].pawn = Pawn(board, players[num_player])

            # TODO = Definimos inicio de posiciones
            players[num_player].startPosition = board.startPosition(num_player)
            players[num_player].endPositions = board.endPositions(num_player)
            self.players.append(players[num_player])
        self.board = board

    def start(self, roundCount=1):

        roundNumberZeroFill = len(str(roundCount))
        # For each round
        for roundNumber in range(1, roundCount + 1):
            # Reset board stored valid pawn moves & fence placings, and redraw empty grid
            self.board.initStoredValidActions()
            self.board.draw()
            print("ROUND #%s: " % str(roundNumber).zfill(roundNumberZeroFill),
                  end="")
            playerCount = len(self.players)
            # Share fences between players
            playerFenceCount = int(self.totalFenceCount / playerCount)
            self.board.fences, self.board.pawns = [], []
            # For each player
            for i in range(playerCount):
                player = self.players[i]
                # Place player pawn at start position and add fences to player stock
                player.pawn.place(player.startPosition)
                for j in range(playerFenceCount):
                    player.fences.append(Fence(self.board, player))
            # Define randomly first player (coin toss)
            currentPlayerIndex = random.randrange(playerCount)
            finished = False
            while not finished:
                player = self.players[currentPlayerIndex]
                # The player chooses its action (manually for human players or automatically for bots)
                action = player.play(self.board)
                if isinstance(action, PawnMove):
                    player.movePawn(action.toCoord)
                    # Check if the pawn has reach one of the player targets
                    if player.hasWon():
                        finished = True
                        print("Player %s won" % player.name)
                        player.score += 1
                elif isinstance(action, FencePlacing):
                    player.placeFence(action.coord, action.direction)
                elif isinstance(action, Quit):
                    finished = True
                    print("Player %s quitted" % player.name)
                currentPlayerIndex = (currentPlayerIndex + 1) % playerCount
                if INTERFACE:
                    time.sleep(TEMPO_SEC)
        print()
        # self.board.drawOnConsole()
        # Display final scores
        print("FINAL SCORES: ")
        bestPlayer = self.players[0]
        for player in self.players:
            print("- %s: %d" % (str(player), player.score))
            if player.score > bestPlayer.score:
                bestPlayer = player
        print("Player %s won with %d victories!" % (
            bestPlayer.name, bestPlayer.score))

    def end(self):
        if INTERFACE:
            self.board.window.close()
