from src.settings import *
from src.game import *
from src.player.human import *
from src.player.random_bot import *
from src.player.build_runbot import *

PARAMETERS_ERROR_RETURN_CODE = 1


def readArguments():
    players = []
    rounds = 1
    cols = 9
    rows = 9
    totalFenceCount = 20
    squareSize = 70

    playersConsts = ['Alumno-UPC:Human', 'LutimiBot:BuildAndRunBot',
                     'ElioBot:BuildAndRunBot', 'RichiBot:BuildAndRunBot']

    for playerData in playersConsts:
        playerName, playerType = playerData.split(":")
        if playerType not in globals():
            print("Jugador desconocido")
            sys.exit(PARAMETERS_ERROR_RETURN_CODE)
        players.append(globals()[playerType](playerName))
    return players, rounds, cols, rows, totalFenceCount, squareSize


def main():
    win = GraphWin("Quoridor - Complejidad Algoritmica", 500, 100)
    win.setBackground("white")

    text = 'Bienvenido a Quoridor, presione click para iniciar'
    testText = Text(Point(150, 15), text)
    testText.draw(win)

    text = 'Recuerde: Hoy se enfrentará usted contra el mejor bot creado por nosotros'
    testText = Text(Point(215, 30), text)
    testText.draw(win)
    win.getMouse()

    players, rounds, cols, rows, totalFenceCount, squareSize = readArguments()

    # TODO = Inicializamos los componentes(creacion de jugadoresm columnas, tamaño, etc..)
    game = Game(players, cols, rows, totalFenceCount, squareSize)

    game.start(rounds)
    game.end()
    win.close()

    global TRACE
    for i in TRACE:
        print("%s: %s" % (i, TRACE[i]))


main()
