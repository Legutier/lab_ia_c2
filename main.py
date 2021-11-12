from typing import Type
from greedy import BackPackGreedySolver


def initialize_greedy_from_file(solver: Type[BackPackGreedySolver], filename: str) -> BackPackGreedySolver:
    file_ = open(filename)
    lines = file_.readlines()
    total_items, maximum_weight = lines.pop(0).strip().split(" ")
    gain_list = []
    weight_list = []
    for line in lines:
        gain, weight = line.strip().split(" ")
        gain_list.append(int(gain))
        weight_list.append(int(weight))
    return solver(cost=weight_list, gain=gain_list, maximum_weight=int(maximum_weight))


if __name__ == "__main__":
    solver = initialize_greedy_from_file(solver=BackPackGreedySolver, filename="backpack1")
    print(solver.solve())