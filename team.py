from __future__ import annotations
from enum import auto
from typing import Optional, TYPE_CHECKING

from helpers import Flamikin, Aquariuma, Vineon, Normake, Thundrake, Rockodile, Mystifly, Strikeon, Faeboa, Soundcobra

from base_enum import BaseEnum
from monster_base import MonsterBase
from random_gen import RandomGen
from helpers import get_all_monsters
from data_structures.stack_adt import ArrayStack
from data_structures.queue_adt import CircularQueue
from data_structures.array_sorted_list import ArraySortedList
from data_structures.array_sorted_list import ListItem
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
            self.type = "FRONT"
        elif self.team_mode.name == "BACK":     
            self.team = CircularQueue(self.TEAM_LIMIT)    
            self.team_original = CircularQueue(self.TEAM_LIMIT) 
        elif self.team_mode.name == "OPTIMISE": 
            self.team = ArraySortedList(self.TEAM_LIMIT)
            self.sort_method = kwargs['sort_key']
            # if self.sort_method == MonsterTeam.SortMode.HP:
            self.team_original = ArraySortedList(self.TEAM_LIMIT)
            self.reversed = False


        if selection_mode == self.SelectionMode.RANDOM:
            self.select_randomly()
        elif selection_mode == self.SelectionMode.MANUAL:
            self.select_manually()
        elif selection_mode == self.SelectionMode.PROVIDED:
            provided_monsters = kwargs['provided_monsters']
            self.select_provided(provided_monsters)
        else:
            raise ValueError(f"selection_mode {selection_mode} not supported.")
        
    def __len__ (self):

        return len(self.team)

    def add_to_team(self, monster: MonsterBase):
        if self.team_mode.name == "FRONT": 
            self.team.push(monster)
        elif self.team_mode.name == "BACK":     
            self.team.append(monster)
        elif self.team_mode.name == "OPTIMISE": 


            if self.reversed == False:
                if self.sort_method == MonsterTeam.SortMode.HP:
                    monster_and_key = ListItem(monster, monster.get_hp() * -1)
                elif self.sort_method == MonsterTeam.SortMode.ATTACK:
                    monster_and_key = ListItem(monster, monster.get_attack() * -1)
                elif self.sort_method == MonsterTeam.SortMode.DEFENSE:
                    monster_and_key = ListItem(monster, monster.get_defense() * -1)
                elif self.sort_method == MonsterTeam.SortMode.SPEED:
                    monster_and_key = ListItem(monster, monster.get_speed() * -1)
                elif self.sort_method == MonsterTeam.SortMode.LEVEL:
                    monster_and_key = ListItem(monster, monster.get_level() * -1)
                self.team.add(monster_and_key)


            elif self.reversed == True:
                if self.sort_method == MonsterTeam.SortMode.HP:
                    monster_and_key = ListItem(monster, monster.get_hp())
                elif self.sort_method == MonsterTeam.SortMode.ATTACK:
                    monster_and_key = ListItem(monster, monster.get_attack())
                elif self.sort_method == MonsterTeam.SortMode.DEFENSE:
                    monster_and_key = ListItem(monster, monster.get_defense())
                elif self.sort_method == MonsterTeam.SortMode.SPEED:
                    monster_and_key = ListItem(monster, monster.get_speed())
                elif self.sort_method == MonsterTeam.SortMode.LEVEL:
                    monster_and_key = ListItem(monster, monster.get_level())
                self.team.add(monster_and_key)



    def retrieve_from_team(self) -> MonsterBase:
        if self.team_mode.name == "FRONT": 
            return self.team.pop()
        elif self.team_mode.name == "BACK":     
            return self.team.serve()
        elif self.team_mode.name == "OPTIMISE": 
            return self.team.delete_at_index(0).value

    def special(self) -> None:
        if self.team_mode.name == "FRONT": 
            buffer_queue = CircularQueue(3)
            for _ in range(min(MonsterTeam.TEAM_LIMIT//2, len(self.team))):
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
            buffer_list = ArraySortedList(self.TEAM_LIMIT)
            team_length = len(self.team)
            for _ in range(team_length):
                monster_and_key = self.team.delete_at_index(0)
                monster = monster_and_key.value
                key_reversed = monster_and_key.key * -1
                monster_and_reversed_key = ListItem(monster, key_reversed)
                buffer_list.add(monster_and_reversed_key)
            for _ in range(team_length):
                self.team.add(buffer_list.delete_at_index(0))
            if self.reversed == False:
                self.reversed = True
            elif self.reversed == True:
                self.reversed == False

    def regenerate_team(self) -> None:
        self.team = self.team_original

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


        check = False
        for _ in range(Team_size):
            check = False
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
                monster_pick = input("Which monster are you spawning?")
                monsters = get_all_monsters()
                try: 
                    monster_pick = int(monster_pick)
                    if monster_pick <= 41 and monster_pick > 0 and monsters[monster_pick-1].can_be_spawned():

                        check = True
                    else:
                        print("This monster cannot be spawned.")
                except:
                    print("This monster cannot be spawned.")
            
            self.add_to_team(monsters[monster_pick - 1]())

            if self.team_mode.name == "FRONT": 
                self.team_original.push(monsters[monster_pick - 1]())
            elif self.team_mode.name == "BACK":     
                self.team_original.append(monsters[monster_pick - 1]())
            elif self.team_mode.name == "OPTIMISE": 
                if self.sort_method == MonsterTeam.SortMode.HP:
                    monster_and_key = ListItem(monsters[monster_pick - 1](), monsters[monster_pick - 1]().get_hp() * -1)
                elif self.sort_method == MonsterTeam.SortMode.ATTACK:
                    monster_and_key = ListItem(monsters[monster_pick - 1](), monsters[monster_pick - 1]().get_attack() * -1)
                elif self.sort_method == MonsterTeam.SortMode.DEFENSE:
                    monster_and_key = ListItem(monsters[monster_pick - 1](), monsters[monster_pick - 1]().get_defense() * -1)
                elif self.sort_method == MonsterTeam.SortMode.SPEED:
                    monster_and_key = ListItem(monsters[monster_pick - 1](), monsters[monster_pick - 1]().get_speed() * -1)
                elif self.sort_method == MonsterTeam.SortMode.LEVEL:
                    monster_and_key = ListItem(monsters[monster_pick - 1](), monsters[monster_pick - 1]().get_level() * -1)
                self.team_original.add(monster_and_key)    


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
        if len(provided_monsters) > 6:
            raise ValueError()
        for i in range(len(provided_monsters)):
            monster = provided_monsters.__getitem__(i)()
            if provided_monsters.__getitem__(i).can_be_spawned() == False:
                raise ValueError(provided_monsters.__getitem__(i), "cannot be spawned")

            monster_copy = provided_monsters.__getitem__(i)()
            self.add_to_team(monster)
            if self.team_mode.name == "FRONT": 
                self.team_original.push(monster_copy)
            elif self.team_mode.name == "BACK":     
                self.team_original.append(monster_copy)
            elif self.team_mode.name == "OPTIMISE": 
                if self.sort_method == MonsterTeam.SortMode.HP:
                    monster_and_key = ListItem(monster_copy, monster_copy.get_hp() * -1)
                elif self.sort_method == MonsterTeam.SortMode.ATTACK:
                    monster_and_key = ListItem(monster_copy, monster_copy.get_attack() * -1)
                elif self.sort_method == MonsterTeam.SortMode.DEFENSE:
                    monster_and_key = ListItem(monster_copy, monster_copy.get_defense() * -1)
                elif self.sort_method == MonsterTeam.SortMode.SPEED:
                    monster_and_key = ListItem(monster_copy, monster_copy.get_speed() * -1)
                elif self.sort_method == MonsterTeam.SortMode.LEVEL:
                    monster_and_key = ListItem(monster_copy, monster_copy.get_level() * -1)
                self.team_original.add(monster_and_key) 


    def choose_action(self, currently_out: MonsterBase, enemy: MonsterBase) -> Battle.Action:
        # This is just a placeholder function that doesn't matter much for testing.
        from battle import Battle
        if currently_out.get_speed() >= enemy.get_speed() or currently_out.get_hp() >= enemy.get_hp():
            return Battle.Action.ATTACK
        return Battle.Action.SWAP

if __name__ == "__main__":
    # team = MonsterTeam(
    #     team_mode=MonsterTeam.TeamMode.OPTIMISE,
    #     selection_mode=MonsterTeam.SelectionMode.RANDOM,
    #     sort_key=MonsterTeam.SortMode.HP,
    # )
    # print(team)
    # while len(team):
    #     print(team.retrieve_from_team())


    # my_monsters = ArrayR(4)
    # my_monsters[0] = Flamikin
    # my_monsters[1] = Aquariuma
    # my_monsters[2] = Vineon
    # my_monsters[3] = Thundrake
    # extra = Normake()
    # team = MonsterTeam(
    #     team_mode=MonsterTeam.TeamMode.BACK,
    #     selection_mode=MonsterTeam.SelectionMode.MANUAL,
    #     # provided_monsters=my_monsters
    # )
    # print(team.retrieve_from_team())
    # print(team.retrieve_from_team())
    # print(team.retrieve_from_team())
    # team.regenerate_team()
    # print(len(team))
    # print(team.retrieve_from_team())


    my_monsters = ArrayR(2)
    my_monsters[0] = Flamikin
    my_monsters[1] = Normake
    team = MonsterTeam(
        team_mode=MonsterTeam.TeamMode.OPTIMISE,
        selection_mode=MonsterTeam.SelectionMode.PROVIDED,
        sort_key=MonsterTeam.SortMode.HP,
        provided_monsters=my_monsters,
    )
    # Rockodile, Aquariuma, Flamikin, Thundrake




    print(team.retrieve_from_team())
    print(team.retrieve_from_team())





    






    # flamikin.set_hp(1)
    # team.add_to_team(flamikin)
    # team.add_to_team(rockodile)

    # flamikin = team.retrieve_from_team()
    # self.assertIsInstance(flamikin, Flamikin)

    # team.regenerate_team()

    # rockodile = team.retrieve_from_team()
    # aquariuma = team.retrieve_from_team()
    # self.assertIsInstance(rockodile, Rockodile)
    # self.assertIsInstance(aquariuma, Aquariuma)
    # self.assertEqual(rockodile.get_hp(), 9)
    # self.assertEqual(aquariuma.get_hp(), 8)
