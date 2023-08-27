from __future__ import annotations
from enum import auto
from typing import Optional

from base_enum import BaseEnum
from team import MonsterTeam

#test imports
from helpers import Flamikin, Aquariuma, Vineon, Strikeon, Normake, Marititan, Leviatitan, Treetower, Infernoth
from data_structures.referential_array import ArrayR

class Battle:

    class Action(BaseEnum):
        ATTACK = auto()
        SWAP = auto()
        SPECIAL = auto()

    class Result(BaseEnum):
        TEAM1 = auto()
        TEAM2 = auto()
        DRAW = auto()

    def __init__(self, verbosity=0) -> None:
        """ everything unless stated otherwise is o(1)
        best and worst case o(1)"""
        self.verbosity = verbosity

    def process_turn(self) -> Optional[Battle.Result]:
        """
        Process a single turn of the battle. Should:
        * process actions chosen by each team
        * level and evolve monsters
        * remove fainted monsters and retrieve new ones.
        * return the battle result if completed.
        """
        """ everything unless stated otherwise is o(1)
        n = len(self)
        best case o(1) worst case o(n)"""
        print("Turn", self.turn_number)
        self.turn_number += 1
        battle_choice1 = self.team1.choose_action(self.out1, self.out2)
        battle_choice2 = self.team2.choose_action(self.out2, self.out1)


        if battle_choice1 == Battle.Action.SWAP:
            print("retreat", str(self.out1))
            self.team1.add_to_team(self.out1) #O(1) Best case O(n) worst case
            self.out1 = self.team1.retrieve_from_team() #O(1) best case, O(N) worst case N is len(self)
            print(str(self.out1), ", i choose you")
        if battle_choice1 == Battle.Action.SPECIAL:
            self.team1.add_to_team(self.out1) #O(1) Best case O(n) worst case
            self.team1.special() #Best Case O(n) Worst case O(n * Len(self)) 
            self.out1 = self.team1.retrieve_from_team()#O(1) best case, O(N) worst case N is len(self)

        if battle_choice2 == Battle.Action.SWAP:
            print("retreat", str(self.out2))
            self.team2.add_to_team(self.out2) #O(1) Best case O(n) worst case
            self.out2 = self.team2.retrieve_from_team() #O(1) best case, O(N) worst case N is len(self)
            print(str(self.out2), ", i choose you")
        if battle_choice2 == Battle.Action.SPECIAL:
            self.team2.add_to_team(self.out2) #O(1) Best case O(n) worst case
            self.team2.special()#Best Case O(n) Worst case O(n * Len(self))
            self.out2 = self.team2.retrieve_from_team() #O(1) best case, O(N) worst case N is len(self)

        if battle_choice1 == Battle.Action.ATTACK and battle_choice2 == Battle.Action.ATTACK:
            if self.out1.get_speed() > self.out2.get_speed():
                self.out1.attack(self.out2)
                if self.out2.alive():
                    self.out2.attack(self.out1)

            elif self.out1.get_speed() < self.out2.get_speed():
                self.out2.attack(self.out1)
                if self.out1.alive():
                    self.out1.attack(self.out2)
            else:
                self.out1.attack(self.out2)
                self.out2.attack(self.out1)

        else:
            if battle_choice1 == Battle.Action.ATTACK:
                self.out1.attack(self.out2)
            if battle_choice2 == Battle.Action.ATTACK:
                self.out2.attack(self.out1)
        if self.out1.alive() and self.out2.alive():
            print("NO ONE DIED!", str(self.out1), str(self.out2))
            self.out1.set_hp(self.out1.get_hp() - 1)
            self.out2.set_hp(self.out2.get_hp()- 1)
        if self.out1.alive() == False and self.out2.alive() == False:
            if len(self.team1) == 0 and len(self.team2) == 0:
                return Battle.Result.DRAW
            elif len(self.team1) == 0:
                return Battle.Result.TEAM2
            elif len(self.team2) == 0:
                Battle.Result.TEAM1
            else:
                self.out1 = self.team1.retrieve_from_team() #O(1) best case, O(N) worst case N is len(self)
                self.out2 = self.team2.retrieve_from_team() #O(1) best case, O(N) worst case N is len(self)

        if self.out1.alive() == False:
            if len(self.team1) == 0:
                return Battle.Result.TEAM2
            print(str(self.out1))
            self.out1 = self.team1.retrieve_from_team() #O(1) best case, O(N) worst case N is len(self)
            self.out2.level_up()
            if self.out2.ready_to_evolve():
                print(str(self.out2), "is ready to evolve")
                self.out2 = self.out2.evolve()
        if self.out2.alive() == False:
            if len(self.team2) == 0:
                return Battle.Result.TEAM1
            print(str(self.out2))
            self.out2 = self.team2.retrieve_from_team() #O(1) best case, O(N) worst case N is len(self)
            self.out1.level_up()
            if self.out1.ready_to_evolve():
                print(str(self.out1), "is ready to evolve")
                self.out1 = self.out1.evolve()
        print(str(self.out1), str(self.out2))

        




    def battle(self, team1: MonsterTeam, team2: MonsterTeam) -> Battle.Result:
        """everything unless stated otherwise is o(1)
        n = len(self)
        Best case o(1)
        worst case o(m*n)
        """
        if self.verbosity > 0:
            print(f"Team 1: {team1} vs. Team 2: {team2}")
        # Add any pregame logic here.
        self.turn_number = 0
        self.team1 = team1
        self.team2 = team2
        self.out1 = team1.retrieve_from_team() #O(1) best case, O(N) worst case N is len(self)
        self.out2 = team2.retrieve_from_team() #O(1) best case, O(N) worst case N is len(self)
        result = None
        while result is None: #best case o(1) worst case o(m) m being the hp of a monster
            result = self.process_turn() #best case o(1) worst case o(n)
        # Add any postgame logic here.
        return result

if __name__ == "__main__":
    # t1 = MonsterTeam(MonsterTeam.TeamMode.BACK, MonsterTeam.SelectionMode.RANDOM)
    # t2 = MonsterTeam(MonsterTeam.TeamMode.BACK, MonsterTeam.SelectionMode.RANDOM)
    # b = Battle(verbosity=1)
    # print(b.battle(t1, t2))

    b = Battle(verbosity=3)
    team1 = MonsterTeam(
        team_mode=MonsterTeam.TeamMode.BACK,
        selection_mode=MonsterTeam.SelectionMode.PROVIDED,
        provided_monsters=ArrayR.from_list([
            Flamikin,
            Aquariuma,
            Vineon,
            Strikeon,
        ])
    )
    team2 = MonsterTeam(
        team_mode=MonsterTeam.TeamMode.FRONT,
        selection_mode=MonsterTeam.SelectionMode.PROVIDED,
        provided_monsters=ArrayR.from_list([
            Flamikin,
            Aquariuma,
            Vineon,
            Strikeon,
        ])
    )
    # Make them always attack
    # team1.choose_action = lambda out, team: Battle.Action.ATTACK
    # team2.choose_action = lambda out, team: Battle.Action.ATTACK
    print(b.battle(team1,team2))