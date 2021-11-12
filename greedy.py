import random
from typing import List, Tuple
from copy import deepcopy

# declaramos la representacion del modelo
cost = []
ganancia = []


class ValueNotFoundError(Exception):
    pass


class BackpackSolver:

    def __init__(self, cost: List[int], gain: List[int], maximum_weight: int):
        """
        inicializador de solver
        :param cost: hace un paso por valor de la lista usando deepcopy, lista
        de costos
        :param gain: hace un paso por valor de la lista usando deepcopy,
        lista de ganancias respectivas al costo
        :param maximum_weight: peso maximo soportado por la mochila
        """
        self.cost = deepcopy(cost)
        self.gain = deepcopy(gain)
        self.maximum_weight = maximum_weight

    def solve(self) -> List[int]:
        raise NotImplementedError


class BackPackGreedySolver(BackpackSolver):
    """
    Solver Greedy del problema de la mochila
    se representa la mochila como una lista binario [1, 0, 1].
    Se inicializa esta lista con todos sus valores en 0, lo que equivale a no llevar nada
    en la mochila.

    El solver solo construira buscando soluciones factibles, es decir, si no puede entrar nada mas
    no entrara nada mas en la mochila
    """

    def choose_start_point(self) -> int:
        """
        Abstrae punto de partida a una funcion, en este caso
        retorna el primer valor factible como punto de partida.
        Si no encuentra nada manda un error.
        """
        for index, value in enumerate(self.cost):
            if value <= self.maximum_weight:
                return index
        raise ValueNotFoundError

    def evaluate(self, index: int) -> float:
        return self.gain[index] / self.cost[index]

    def shortsighted_function(self, solution: List[int], actual_weight: int, actual_gain: int) -> Tuple[bool, int, int]:
        """"
        Funcion miope, retorna tupla[bool, int] la cual bool indica si ya no puede seguir añadiendo
        y int el peso actual con la nueva construccion de solucion, solo añade algo nuevo a la solucion si es
        factible.
        """
        best_evaluated = (-1, -1)
        for index in range(len(solution)):
            if solution[index] != 1:
                evaluation = self.evaluate(index)
                if (
                    evaluation > best_evaluated[1]
                    and actual_weight + self.cost[index] <= self.maximum_weight
                ):
                    best_evaluated = (index, evaluation)
        if best_evaluated[0] == -1:
            return True, actual_weight, actual_gain
        else:
            solution[best_evaluated[0]] = 1
            return False, actual_weight + self.cost[best_evaluated[0]], actual_gain + self.gain[best_evaluated[0]]

    def solve(self) -> Tuple[List[int], int]:
        """
        Resuelve de manera greedy el problema de la mochila
        Representacion: [0, 1, 0..., 1, 0] lista binaria que representa
        si objeto i es llevado o no.
        :returns lista de bits con la solucion
        """
        # la solucion no ha sido iniciada, se debe construir por ende -1 representa que no se ha decidido.
        solution = [0 for _ in range(len(self.cost))]
        actual_weight = 0
        summed_gain = 0
        finish = False
        try:
            solution[self.choose_start_point()] = 1
            actual_weight += self.cost[self.choose_start_point()]
            summed_gain += self.gain[self.choose_start_point()]
        except ValueNotFoundError:
            finish = True
        while not finish:
            print(solution, actual_weight, summed_gain)
            finish, actual_weight, summed_gain = self.shortsighted_function(solution, actual_weight, summed_gain)
        return solution, summed_gain


class RandomBackPackGreedySolver(BackPackGreedySolver):

    def choose_start_point(self) -> int:
        """"
        Escoge un punto de partida aleatorio.
        Si este punto de partida genera una construccion no factible
        reintenta hasta quedarse sin opciones, si no las hay arroja ValueNotFoundError
        """
        random_start = random.randrange(0, len(self.cost))
        tries = len(self.cost)
        while tries:
            if self.cost[random_start] <= self.maximum_weight:
                return random_start
            else:
                tries -= 1
        raise ValueNotFoundError
