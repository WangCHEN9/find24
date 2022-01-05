from itertools import permutations, product
from typing import List, Tuple
import random


class findMath4Num:
    def __init__(self, numbers: List[int], target_num: int = 24) -> None:
        self.target_num = target_num
        self.numbers = numbers
        self.length = len(self.numbers)
        self.ops_list = self._get_ops()
        self.combos = self._get_combos()

    def _get_ops(self):
        return list(product("*/+-", repeat=self.length - 1))

    def _get_combos(self):
        return list(permutations(self.numbers, self.length))

    def _get_formula_4_num(self, ops: Tuple, combo: Tuple):
        formula_1 = (
            f"(({combo[0]}{ops[0]}{combo[1]}){ops[1]}{combo[2]}){ops[2]}{combo[3]}"
        )
        formula_2 = (
            f"({combo[0]}{ops[0]}{combo[1]}){ops[1]}({combo[2]}{ops[2]}{combo[3]})"
        )
        return [formula_1, formula_2]

    def _get_all_formula_4_num(self):
        formula_list = []
        for combo in self.combos:
            for ops in self.ops_list:
                formula_list.append(self._get_formula_4_num(ops=ops, combo=combo))
        return formula_list

    def _flat_list(self, input_list: List[List]):
        flat_list = [item for sublist in input_list for item in sublist]
        return flat_list

    def get_result(self):
        ok_results = []
        for formula in self._flat_list(self._get_all_formula_4_num()):
            try:
                if abs(eval(formula) - self.target_num) < 10e-16:
                    ok_results.append(formula)
            except ZeroDivisionError:
                continue
        if len(ok_results) == 0:
            return ok_results
        else:
            return random.choice(ok_results)


class findMath6Num:
    def __init__(self, numbers: List[int], target_num: int = 24) -> None:
        self.target_num = target_num
        self.numbers = numbers
        self.length = len(self.numbers)

    def _get_combos_2_num(self):
        return list(permutations(self.numbers, 2))

    def _get_2_num_result(self, numbers: List):
        ops = ["*", "+"]
        results = []
        for op in ops:
            result = eval(f"({numbers[0]}{op}{numbers[1]})")
            results.append(result)
        return results

    def get_result(self):
        ok_results = []
        two_numbers_lists = self._get_combos_2_num()
        for two_numbers in two_numbers_lists:
            remain_4_num = self.list_subtract(
                small_list=list(two_numbers), big_list=self.numbers
            )
            for to_subtract in self._get_2_num_result(two_numbers):
                target_for_4_num = self.target_num - to_subtract
                x = findMath4Num(remain_4_num, target_for_4_num)
                sub_results = x.get_result()
                if len(sub_results) > 0:
                    ok_results.append(f"{two_numbers} -> {to_subtract} + {sub_results}")
        return ok_results

    def list_subtract(self, small_list: List, big_list: List):
        return [i for i in big_list if not i in small_list or small_list.remove(i)]


if __name__ == "__main__":
    x = findMath6Num([13, 10, 4, 1, 6, 7], target_num=100)

    for res in x.get_result():
        print(res, end="\n")
