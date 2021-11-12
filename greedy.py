import random
from typing import List, Tuple
from copy import deepcopy

# declaramos la representacion del modelo
cost = []
ganancia = []


class ValueNotFoundError(Exception):
    pass


class BackpackSolver:

    def __init__(self, cost: List[int], gain: List[int], maximum_weight: int, elements_qty: int):
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
        self.actual_weight = 0
        self.actual_gain = 0
        self.solution = [0 for _ in range(elements_qty)]
        self.elements_qty = elements_qty

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

    def evaluate(self, index: int) -> float:
        return self.gain[index] / self.cost[index]

    def shortsighted_function(self) -> bool:
        """"
        Funcion miope, retorna tupla[bool, int] la cual bool indica si ya no puede seguir añadiendo
        y int el peso actual con la nueva construccion de solucion, solo añade algo nuevo a la solucion si es
        factible.
        """
        best_evaluated = (-1, -1)
        for index in range(self.elements_qty):
            if self.solution[index] != 1:
                evaluation = self.evaluate(index)
                if (
                    evaluation > best_evaluated[1]
                    and self.actual_weight + self.cost[index] <= self.maximum_weight
                ):
                    best_evaluated = (index, evaluation)
        if best_evaluated[0] == -1:
            return True
        else:
            self.solution[best_evaluated[0]] = 1
            self.actual_gain +=  self.gain[best_evaluated[0]]
            self.actual_weight += self.cost[best_evaluated[0]]
            return False

    def solve(self) -> Tuple[List[int], int]:
        """
        Resuelve de manera greedy el problema de la mochila
        Representacion: [0, 1, 0..., 1, 0] lista binaria que representa
        si objeto i es llevado o no.
        :returns lista de bits con la solucion
        """
        finish = False
        while not finish:
            print(self.solution, self.actual_weight, self.actual_gain)
            finish = self.shortsighted_function()
        return self.solution, self.actual_gain


class RandomBackPackGreedySolver(BackPackGreedySolver):

    def choose_start_point(self) -> None:
        """"
        Escoge un punto de partida aleatorio.
        Si este punto de partida genera una construccion no factible
        reintenta hasta quedarse sin opciones, si no las hay arroja ValueNotFoundError
        """
        random_start = random.randrange(0, len(self.cost))
        tries = len(self.cost)
        while tries:
            if self.cost[random_start] <= self.maximum_weight:
                self.solution[random_start] = 1
                self.actual_gain += self.gain[random_start]
                self.actual_weight += self.cost[random_start]
                return
            else:
                tries -= 1
        return

    def solve(self) -> Tuple[List[int], int]:
        self.choose_start_point()
        return super(RandomBackPackGreedySolver, self).solve()
