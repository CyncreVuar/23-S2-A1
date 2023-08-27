import abc

from data_structures.referential_array import ArrayR
from data_structures.stack_adt import ArrayStack
from data_structures.array_sorted_list import ArraySortedList
from data_structures.sorted_list_adt import ListItem

class Stats(abc.ABC):

    @abc.abstractmethod
    def get_attack(self):
        pass

    @abc.abstractmethod
    def get_defense(self):
        pass

    @abc.abstractmethod
    def get_speed(self):
        pass

    @abc.abstractmethod
    def get_max_hp(self):
        pass

#Anything otherwise is O(1)
class SimpleStats(Stats):
    """ everything unless stated otherwise is o(1)
        best and worst case o(1)"""

    def __init__(self, attack, defense, speed, max_hp) -> None:
        
        # TODO: Implement
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.max_hp = max_hp

    def get_attack(self):
        return self.attack

    def get_defense(self):
        return self.defense

    def get_speed(self):
        return self.speed

    def get_max_hp(self):
        return self.max_hp

class ComplexStats(Stats):

    def __init__(
        self,
        attack_formula: ArrayR[str],
        defense_formula: ArrayR[str],
        speed_formula: ArrayR[str],
        max_hp_formula: ArrayR[str],
    ) -> None:
        # TODO: Implement
        self.attack_formula = attack_formula
        self.defense_formula = defense_formula
        self. speed_formula = speed_formula
        self.max_hp_formula = max_hp_formula
        pass

    def get_attack(self, level: int):
        """ everything unless stated otherwise is o(1)
        best and worst case o(1)"""
        calc_stack = ArrayStack(20)
        for elem in self.attack_formula:
            if elem == "+":
                calc_stack.push(float(calc_stack.pop()) + float(calc_stack.pop()))
            elif elem == "/":
                op2 = float(calc_stack.pop())
                op1 = float(calc_stack.pop())
                calc_stack.push(op1 / op2)
            elif elem == "-":
                op2 = float(calc_stack.pop())
                op1 = float(calc_stack.pop())
                calc_stack.push(op1 - op2)
            elif elem == "*":
                calc_stack.push(float(calc_stack.pop()) * float(calc_stack.pop()))
            elif elem == "level":
                calc_stack.push(float(level))
            elif elem == "power":
                op2 = float(calc_stack.pop())
                op1 = float(calc_stack.pop())
                calc_stack.push(op1 ** op2)
            elif elem == "sqrt":
                calc_stack.push(float(calc_stack.pop())** (1/2))
            elif elem == "middle":
                median_list = ArraySortedList(3)
                op3 = float(calc_stack.pop())
                op2 = float(calc_stack.pop())
                op1 = float(calc_stack.pop())
                median_list.add(ListItem(op3, op3))
                median_list.add(ListItem(op2, op2))
                median_list.add(ListItem(op1, op1))
                calc_stack.push(median_list.delete_at_index(1).value)
            else:
                calc_stack.push(elem)
        return int(calc_stack.pop())

    def get_defense(self, level: int):
        """ everything unless stated otherwise is o(1)
        best and worst case o(1)"""
        calc_stack = ArrayStack(20)
        for elem in self.defense_formula:
            if elem == "+":
                calc_stack.push(float(calc_stack.pop()) + float(calc_stack.pop()))
            elif elem == "/":
                op2 = float(calc_stack.pop())
                op1 = float(calc_stack.pop())
                calc_stack.push(op1 / op2)
            elif elem == "-":
                op2 = float(calc_stack.pop())
                op1 = float(calc_stack.pop())
                calc_stack.push(op1 - op2)
            elif elem == "*":
                calc_stack.push(float(calc_stack.pop()) * float(calc_stack.pop()))
            elif elem == "level":
                calc_stack.push(float(level))
            elif elem == "power":
                op2 = float(calc_stack.pop())
                op1 = float(calc_stack.pop())
                calc_stack.push(op1 ** op2)
            elif elem == "sqrt":
                calc_stack.push(float(calc_stack.pop())** (1/2))
            elif elem == "middle":
                median_list = ArraySortedList(3)
                op3 = float(calc_stack.pop())
                op2 = float(calc_stack.pop())
                op1 = float(calc_stack.pop())
                median_list.add(ListItem(op3, op3))
                median_list.add(ListItem(op2, op2))
                median_list.add(ListItem(op1, op1))
                calc_stack.push(median_list.delete_at_index(1).value)
            else:
                calc_stack.push(elem)
        return int(calc_stack.pop())

    def get_speed(self, level: int):
        """ everything unless stated otherwise is o(1)
        best and worst case o(1)"""
        calc_stack = ArrayStack(20)
        for elem in self.speed_formula:
            if elem == "+":
                calc_stack.push(float(calc_stack.pop()) + float(calc_stack.pop()))
            elif elem == "/":
                op2 = float(calc_stack.pop())
                op1 = float(calc_stack.pop())
                calc_stack.push(op1 / op2)
            elif elem == "-":
                op2 = float(calc_stack.pop())
                op1 = float(calc_stack.pop())
                calc_stack.push(op1 - op2)
            elif elem == "*":
                calc_stack.push(float(calc_stack.pop()) * float(calc_stack.pop()))
            elif elem == "level":
                calc_stack.push(float(level))
            elif elem == "power":
                op2 = float(calc_stack.pop())
                op1 = float(calc_stack.pop())
                calc_stack.push(op1 ** op2)
            elif elem == "sqrt":
                calc_stack.push(float(calc_stack.pop())** (1/2))
            elif elem == "middle":
                median_list = ArraySortedList(3)
                op3 = float(calc_stack.pop())
                op2 = float(calc_stack.pop())
                op1 = float(calc_stack.pop())
                median_list.add(ListItem(op3, op3))
                median_list.add(ListItem(op2, op2))
                median_list.add(ListItem(op1, op1))
                calc_stack.push(median_list.delete_at_index(1).value)
            else:
                calc_stack.push(elem)
        return int(calc_stack.pop())

    def get_max_hp(self, level: int):
        """ everything unless stated otherwise is o(1)
        best and worst case o(1)"""
        calc_stack = ArrayStack(20)
        for elem in self.max_hp_formula:
            if elem == "+":
                calc_stack.push(float(calc_stack.pop()) + float(calc_stack.pop()))
            elif elem == "/":
                op2 = float(calc_stack.pop())
                op1 = float(calc_stack.pop())
                calc_stack.push(op1 / op2)
            elif elem == "-":
                op2 = float(calc_stack.pop())
                op1 = float(calc_stack.pop())
                calc_stack.push(op1 - op2)
            elif elem == "*":
                calc_stack.push(float(calc_stack.pop()) * float(calc_stack.pop()))
            elif elem == "level":
                calc_stack.push(float(level))
            elif elem == "power":
                op2 = float(calc_stack.pop())
                op1 = float(calc_stack.pop())
                calc_stack.push(op1 ** op2)
            elif elem == "sqrt":
                calc_stack.push(float(calc_stack.pop())** (1/2))
            elif elem == "middle":
                median_list = ArraySortedList(3)
                op3 = float(calc_stack.pop())
                op2 = float(calc_stack.pop())
                op1 = float(calc_stack.pop())
                median_list.add(ListItem(op3, op3))
                median_list.add(ListItem(op2, op2))
                median_list.add(ListItem(op1, op1))
                calc_stack.push(median_list.delete_at_index(1).value)
            else:
                calc_stack.push(elem)
        return int(calc_stack.pop())

