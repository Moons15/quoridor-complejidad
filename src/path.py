import math

from src.settings import *
from src.action.pawn_move import *


class Path:
    """
        Aquí definiremos los algoritmos utilizados en las funciones
    """

    def __init__(self, moves):
        self.moves = moves

    def length(self):
        return len(self.moves)

    def startCoord(self):
        return self.moves[0].fromCoord

    def endCoord(self):
        return self.moves[-1].toCoord

    def firstMove(self):
        return self.moves[0]

    # TODO = Función predeterminada en Python, enfoca al objeto de manera string

    def __str__(self):
        return "[%s] -> %s" % (str(self.startCoord()), " -> ".join(
            map(lambda move: str(move.toCoord), self.moves)))

    def ManhattanDistance(fromCoord, toCoord):
        return abs(toCoord.col - fromCoord.col) + abs(
            toCoord.row - fromCoord.row)

    def ManhattanDistanceMulti(fromCoord, toCoords):

        minManhattanDistance = math.inf  # 3.5
        for toCoord in toCoords:
            manhattanDistance = Path.ManhattanDistance(fromCoord, toCoord)
            if manhattanDistance < minManhattanDistance:
                minManhattanDistance = manhattanDistance
        return minManhattanDistance

    def BreadthFirstSearch(board, startCoord, endCoords, ignorePawns=False):
        """
        1ER ALGORITMO USADO === BFS

        Hecho por: Elio

        Es un algoritmo de búsqueda no informada utilizado para recorrer o buscar
        elementos en un grafo (usado frecuentemente sobre árboles).
        Intuitivamente, se comienza en la raíz (eligiendo algún nodo como
        elemento raíz en el caso de un grafo) y se exploran todos los vecinos
        de este nodo. A continuación para cada uno de los vecinos se exploran
        sus respectivos vecinos adyacentes, y así hasta que se recorra
        todo el árbol.
        """
        global TRACE
        TRACE["Path.BreadthFirstSearch"] += 1

        print("Esta utilizando BFS en este movimiento")
        root = PawnMove(None, startCoord)

        previousMoves = {startCoord: root}
        nextMoves = [root]
        validPawnMoves = board.storedValidPawnMovesIgnoringPawns if ignorePawns else board.storedValidPawnMoves
        while nextMoves:
            move = nextMoves.pop(0)
            for endCoord in endCoords:
                if move.toCoord == endCoord:
                    pathMoves = [move]
                    while move.fromCoord is not None:
                        move = previousMoves[move.fromCoord]
                        pathMoves.append(move)
                    pathMoves.reverse()
                    return Path(pathMoves[1:])
            validMoves = validPawnMoves[move.toCoord]
            sorted(validMoves,
                   key=lambda validMove: Path.ManhattanDistanceMulti(
                       validMove.toCoord, endCoords))
            for validMove in validMoves:
                if validMove.toCoord not in previousMoves:
                    previousMoves[validMove.toCoord] = validMove
                    nextMoves.append(validMove)
        return None

    def Dijkstra(board, startCoord, endCoords, moveScore=lambda move, step: 1,
                 ignorePawns=False):
        """
        3ER ALGORITMO USADO === Dijkstra

        Hecho por Richard

        El algoritmo de Dijkstra, también llamado algoritmo de caminos mínimos,
        es un algoritmo para la determinación del camino más corto, dado un
        vértice origen, hacia el resto de los vértices en un grafo que tiene
        pesos en cada arista. La idea subyacente en este algoritmo consiste en
        ir explorando todos los caminos más cortos que parten del vértice
        origen y que llevan a todos los demás vértices; cuando se obtiene el
        camino más corto desde el vértice origen hasta el resto de los vértices
         que componen el grafo, el algoritmo se detiene.
        """
        global TRACE
        TRACE["Path.Dijkstra"] += 1
        print("Esta utilizando Dijkstra en este movimiento")

        root = PawnMove(None, startCoord)

        previousMoves = {startCoord: (0, root)}
        nextMoves = [(0, 0, root)]
        validPawnMoves = board.storedValidPawnMovesIgnoringPawns \
            if ignorePawns else board.storedValidPawnMoves
        while nextMoves:
            sorted(nextMoves,
                   key=lambda nextMove: nextMove[1])
            (step, score, move) = nextMoves.pop(0)
            for endCoord in endCoords:
                if move.toCoord == endCoord:
                    pathMoves = [move]
                    while move.fromCoord is not None:
                        move = previousMoves[move.fromCoord][1]
                        pathMoves.append(move)
                    pathMoves.reverse()
                    return Path(pathMoves[1:])
            validMoves = validPawnMoves[move.toCoord]
            sorted(validMoves,
                   key=lambda validMove: Path.ManhattanDistanceMulti(
                       validMove.toCoord, endCoords))
            for validMove in validMoves:
                validMoveScore = score + moveScore(validMove, step + 1)
                if validMove.toCoord not in previousMoves:
                    previousMoves[validMove.toCoord] = (
                        validMoveScore, validMove)
                    nextMoves.append((step + 1, validMoveScore, validMove))
                if validMoveScore < previousMoves[validMove.toCoord][0]:
                    previousMoves[validMove.toCoord] = (
                        validMoveScore, validMove)
        return None

    def DepthFirstSearch(self, visited, graph, node):
        """
        3ER ALGORITMO USADO === DFS

        Hecho por Luis Ticona

        Una Búsqueda en profundidad (Depth First Search) es un algoritmo de
        búsqueda no informada utilizado para recorrer todos los nodos de un
        grafo o árbol (teoría de grafos) de manera ordenada, pero no uniforme.
        """

        global TRACE
        TRACE["Path.DepthFirstSearch"] += 1

        if node not in visited:
            print(node)
            visited.add(node)
            for neighbour in graph[node]:
                self.DepthFirstSearch(visited, graph, neighbour)

        def dfs_paths(graph, start, goal):
            stack = [(start, [start])]
            while stack:
                (vertex, path) = stack.pop()
                for next in graph[vertex] - set(path):
                    if next == goal:
                        yield path + [next]
                    else:
                        stack.append((next, path + [next]))

        return None
