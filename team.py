from __future__ import annotations
from enum import auto
from typing import Optional, TYPE_CHECKING

from base_enum import BaseEnum
from monster_base import MonsterBase
from random_gen import RandomGen
from helpers import get_all_monsters
from data_structures.stack_adt import ArrayStack
from data_structures.queue_adt import CircularQueue
from data_structures.array_sorted_list import ArraySortedList
from data_structures.referential_array import ArrayR


if TYPE_CHECKING:
    from battle import Battle

class MonsterTeam:

    class TeamMode(BaseEnum):

        FRONT = auto()
        BACK = auto()
        OPTIMISE = auto()

    class SelectionMode(BaseEnum):

        RANDOM = auto()
        MANUAL = auto()
        PROVIDED = auto()

    class SortMode(BaseEnum):

        HP = auto()
        ATTACK = auto()
        DEFENSE = auto()
        SPEED = auto()
        LEVEL = auto()

    TEAM_LIMIT = 6

    def __init__(self, team_mode: TeamMode, selection_mode, **kwargs) -> None:
        # Add any preinit logic here.
        self.team_mode = team_mode

        if self.team_mode.name == "FRONT": 
            self.team = ArrayStack(self.TEAM_LIMIT)
            self.team_original = ArrayStack(self.TEAM_LIMIT)
        elif self.team_mode.name == "BACK":     
            self.team = CircularQueue(self.TEAM_LIMIT)    
            self.team_original = CircularQueue(self.TEAM_LIMIT) 
        elif self.team_mode.name == "OPTIMISE": 
            self.team = ArraySortedList(self.TEAM_LIMIT)
            self.sort_method = kwargs['sort_mode']
            # if self.sort_method == MonsterTeam.SortMode.HP:
        self.team_original


        if selection_mode == self.SelectionMode.RANDOM:
            self.select_randomly(**kwargs)
        elif selection_mode == self.SelectionMode.MANUAL:
            self.select_manually(**kwargs)
        elif selection_mode == self.SelectionMode.PROVIDED:
            self.select_provided(**kwargs)
        else:
            raise ValueError(f"selection_mode {selection_mode} not supported.")

    def add_to_team(self, monster: MonsterBase):
        if self.team_mode.name == "FRONT": 
            self.team.push(monster)
        elif self.team_mode.name == "BACK":     
            self.team.append(monster)
        elif self.team_mode.name == "OPTIMISE": 
            print("ggez") 


    def retrieve_from_team(self) -> MonsterBase:
        if self.team_mode.name == "FRONT": 
            self.team.pop()
        elif self.team_mode.name == "BACK":     
            self.team.serve()
        elif self.team_mode.name == "OPTIMISE": 
            self.team.delete_at_index(0)

    def special(self) -> None:
        if self.team_mode.name == "FRONT": 
            buffer_queue = CircularQueue(3)
            for _ in range(min(MonsterTeam.TEAM_LIMIT/2, len(self.team))):
                buffer_queue.append(self.team.pop())
            for _ in range(len(buffer_queue)):
                self.team.push(buffer_queue.serve())
        elif self.team_mode.name == "BACK":
            front_half = len(self.team)//2
            back_half = len(self.team)-(len(self.team)//2)     
            buffer_queue = CircularQueue(front_half)
            buffer_stack = ArrayStack(back_half)
            for _ in range(front_half):
                buffer_queue.append(self.team.serve())
            for _ in range(back_half):     
                buffer_stack.push(self.team.serve())
            
            for _ in range(back_half):
                self.team.append(buffer_stack.pop())
            for _ in range(front_half):
                self.team.append(buffer_queue.serve())
            
        elif self.team_mode.name == "OPTIMISE": 
            print("ggez") 

    def regenerate_team(self) -> None:
        if self.team_mode.name == "FRONT": 
            print("front")
        elif self.team_mode.name == "BACK":     
            print("BACK")
        elif self.team_mode.name == "OPTIMISE": 
            print("ggez") 

    def select_randomly(self):
        team_size = RandomGen.randint(1, self.TEAM_LIMIT)
        monsters = get_all_monsters()
        n_spawnable = 0
        for x in range(len(monsters)):
            if monsters[x].can_be_spawned():
                n_spawnable += 1

        for _ in range(team_size):
            spawner_index = RandomGen.randint(0, n_spawnable-1)
            cur_index = -1
            for x in range(len(monsters)):
                if monsters[x].can_be_spawned():
                    cur_index += 1
                    if cur_index == spawner_index:
                        # Spawn this monster
                        self.add_to_team(monsters[x]())
                        break
            else:
                raise ValueError("Spawning logic failed.")

    def select_manually(self):
        check = False
        while check == False:
            Team_size = input("How many monsters are there?")
            try: 
                Team_size = int(Team_size)
                if Team_size <= 6 and Team_size > 0:
                    check = True
            except:
                print("Please enter an integer between 1 and 6")

        if self.team_mode.name == "FRONT": 
            buffer_stack = ArrayStack(Team_size)
            check = False
            for _ in range(Team_size):
                print("""MONSTERS Are:
                1: Flamikin [✔️]
                2: Infernoth [❌]
                3: Infernox [❌]
                4: Aquariuma [✔️]
                5: Marititan [❌]
                6: Leviatitan [❌]
                7: Vineon [✔️]
                8: Treetower [❌]
                9: Treemendous [❌]
                10: Rockodile [✔️]
                11: Stonemountain [❌]
                12: Gustwing [✔️]
                13: Stormeagle [❌]
                14: Frostbite [✔️]
                15: Blizzarus [❌]
                16: Thundrake [✔️]
                17: Thunderdrake [❌]
                18: Shadowcat [✔️]
                19: Nightpanther [❌]
                20: Mystifly [✔️]
                21: Telekite [❌]
                22: Metalhorn [✔️]
                23: Ironclad [❌]
                24: Normake [❌]
                25: Strikeon [✔️]
                26: Venomcoil [✔️]
                27: Pythondra [✔️]
                28: Constriclaw [✔️]
                29: Shockserpent [✔️]
                30: Driftsnake [✔️]
                31: Aquanake [✔️]
                32: Flameserpent [✔️]
                33: Leafadder [✔️]
                34: Iceviper [✔️]
                35: Rockpython [✔️]
                36: Soundcobra [✔️]
                37: Psychosnake [✔️]
                38: Groundviper [✔️]
                39: Faeboa [✔️]
                40: Bugrattler [✔️]
                41: Darkadder [✔️]""")
                while check == False:
                    monster = input("Which monster are you spawning?")
                

        elif self.team_mode.name == "BACK":     
            self.team.serve()
        elif self.team_mode.name == "OPTIMISE": 
            self.team.delete_at_index(0)
        """
        Prompt the user for input on selecting the team.
        Any invalid input should have the code prompt the user again.

        First input: Team size. Single integer
        For _ in range(team size):
            Next input: Prompt selection of a Monster class.
                * Should take a single input, asking for an integer.
                    This integer corresponds to an index (1-indexed) of the helpers method
                    get_all_monsters()
                * If invalid of monster is not spawnable, should ask again.

        Add these monsters to the team in the same order input was provided. Example interaction:

        How many monsters are there? 2
        MONSTERS Are:
        1: Flamikin [✔️]
        2: Infernoth [❌]
        3: Infernox [❌]
        4: Aquariuma [✔️]
        5: Marititan [❌]
        6: Leviatitan [❌]
        7: Vineon [✔️]
        8: Treetower [❌]
        9: Treemendous [❌]
        10: Rockodile [✔️]
        11: Stonemountain [❌]
        12: Gustwing [✔️]
        13: Stormeagle [❌]
        14: Frostbite [✔️]
        15: Blizzarus [❌]
        16: Thundrake [✔️]
        17: Thunderdrake [❌]
        18: Shadowcat [✔️]
        19: Nightpanther [❌]
        20: Mystifly [✔️]
        21: Telekite [❌]
        22: Metalhorn [✔️]
        23: Ironclad [❌]
        24: Normake [❌]
        25: Strikeon [✔️]
        26: Venomcoil [✔️]
        27: Pythondra [✔️]
        28: Constriclaw [✔️]
        29: Shockserpent [✔️]
        30: Driftsnake [✔️]
        31: Aquanake [✔️]
        32: Flameserpent [✔️]
        33: Leafadder [✔️]
        34: Iceviper [✔️]
        35: Rockpython [✔️]
        36: Soundcobra [✔️]
        37: Psychosnake [✔️]
        38: Groundviper [✔️]
        39: Faeboa [✔️]
        40: Bugrattler [✔️]
        41: Darkadder [✔️]
        Which monster are you spawning? 38
        MONSTERS Are:
        1: Flamikin [✔️]
        2: Infernoth [❌]
        3: Infernox [❌]
        4: Aquariuma [✔️]
        5: Marititan [❌]
        6: Leviatitan [❌]
        7: Vineon [✔️]
        8: Treetower [❌]
        9: Treemendous [❌]
        10: Rockodile [✔️]
        11: Stonemountain [❌]
        12: Gustwing [✔️]
        13: Stormeagle [❌]
        14: Frostbite [✔️]
        15: Blizzarus [❌]
        16: Thundrake [✔️]
        17: Thunderdrake [❌]
        18: Shadowcat [✔️]
        19: Nightpanther [❌]
        20: Mystifly [✔️]
        21: Telekite [❌]
        22: Metalhorn [✔️]
        23: Ironclad [❌]
        24: Normake [❌]
        25: Strikeon [✔️]
        26: Venomcoil [✔️]
        27: Pythondra [✔️]
        28: Constriclaw [✔️]
        29: Shockserpent [✔️]
        30: Driftsnake [✔️]
        31: Aquanake [✔️]
        32: Flameserpent [✔️]
        33: Leafadder [✔️]
        34: Iceviper [✔️]
        35: Rockpython [✔️]
        36: Soundcobra [✔️]
        37: Psychosnake [✔️]
        38: Groundviper [✔️]
        39: Faeboa [✔️]
        40: Bugrattler [✔️]
        41: Darkadder [✔️]
        Which monster are you spawning? 2
        This monster cannot be spawned.
        Which monster are you spawning? 1
        """
        raise NotImplementedError

    def select_provided(self, provided_monsters:Optional[ArrayR[type[MonsterBase]]]=None):
        """
        Generates a team based on a list of already provided monster classes.

        While the type hint imples the argument can be none, this method should never be called without the list.
        Monsters should be added to the team in the same order as the provided array.

        Example input:
        [Flamikin, Aquariuma, Gustwing] <- These are all classes.

        Example team if in TeamMode.FRONT:
        [Gustwing Instance, Aquariuma Instance, Flamikin Instance]
        """
        if self.team_mode.name == "FRONT": 
            self.team.pop()
        elif self.team_mode.name == "BACK":     
            self.team.serve()
        elif self.team_mode.name == "OPTIMISE": 
            self.team.delete_at_index(0)
        raise NotImplementedError

    def choose_action(self, currently_out: MonsterBase, enemy: MonsterBase) -> Battle.Action:
        # This is just a placeholder function that doesn't matter much for testing.
        from battle import Battle
        if currently_out.get_speed() >= enemy.get_speed() or currently_out.get_hp() >= enemy.get_hp():
            return Battle.Action.ATTACK
        return Battle.Action.SWAP

if __name__ == "__main__":
    team = MonsterTeam(
        team_mode=MonsterTeam.TeamMode.OPTIMISE,
        selection_mode=MonsterTeam.SelectionMode.RANDOM,
        sort_key=MonsterTeam.SortMode.HP,
    )
    print(team)
    while len(team):
        print(team.retrieve_from_team())
