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
        """everything unless stated otherwise is o(1)
        O(1) best case and worse case"""
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
        
        # if self.team_mode.name == "FRONT": 
        #     self.team = ArrayStack(self.TEAM_LIMIT)
        #     self.team_original = ArrayStack(self.TEAM_LIMIT)
        #     self.type = "FRONT"
        # elif self.team_mode.name == "BACK":     
        #     self.team = CircularQueue(self.TEAM_LIMIT)    
        #     self.team_original = CircularQueue(self.TEAM_LIMIT) 
        # elif self.team_mode.name == "OPTIMISE": 
        
        
    def __str__ (self):
        """everything unless stated otherwise is o(1)
        o(1) best case and worse case"""
        return (f"{self.team_mode.name} TEAM")
    def __len__ (self):

        return len(self.team)

    def add_to_team(self, monster: MonsterBase):
        """everything unless stated otherwise is o(1)
        O(1) Best case
         O(n) worst case"""
        if self.team_mode.name == "FRONT": 
            """everything unless stated otherwise is o(1)
            O(1) Best case worst case"""
            self.team.push(monster)


        elif self.team_mode.name == "BACK": 
            """everything unless stated otherwise is o(1)
            O(1) Best case worst case""" 
            self.team.append(monster)


        elif self.team_mode.name == "OPTIMISE": 
            """everything unless stated otherwise is o(1)
            Best case O(log(n)) Worst case O(n)""" 


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
                self.team.add(monster_and_key) #Best case O(log(n)) Worst case O(n)


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
                self.team.add(monster_and_key) #Best case O(log(n)) Worst case O(n)  



    def retrieve_from_team(self) -> MonsterBase:
        """everything unless stated otherwise is o(1)
        O(1) best case, O(N) worst case N is len(self)"""
        if self.team_mode.name == "FRONT": 
            """O(1)  Best case worst case"""
            return self.team.pop()
        

        elif self.team_mode.name == "BACK":
            """everything unless stated otherwise is o(1)
            O(1)  Best case worst case"""
            return self.team.serve()
        
        
        elif self.team_mode.name == "OPTIMISE":
            """everything unless stated otherwise is o(1)
            O(N) best case, O(N) worst case N is len(self)
            This always deletes the head"""
            return self.team.delete_at_index(0).value #Best case O(len(self)) worst case O(len(self))

    def special(self) -> None:
        """everything unless stated otherwise is o(1)
        Best Case O(n) Worst case O(n * Len(self)) """

        if self.team_mode.name == "FRONT": 
            """everything unless stated otherwise is o(1)
            O(N) Best and worst case"""
            buffer_queue = CircularQueue(3)
            for _ in range(min(3, len(self.team))): #O(1) best and worst case
                buffer_queue.append(self.team.pop()) #O(1)
            for _ in range(len(buffer_queue)): #O(n) 
                self.team.push(buffer_queue.serve())    # O(N)

        elif self.team_mode.name == "BACK":
            """everything unless stated otherwise is o(1)
            best and worst case O(N), N being len(self)"""
            front_half = len(self.team)//2
            back_half = len(self.team)-(len(self.team)//2)     
            buffer_queue = CircularQueue(front_half)
            buffer_stack = ArrayStack(back_half)
            for _ in range(front_half): #O(n)
                buffer_queue.append(self.team.serve())#O(1)
            for _ in range(back_half):     #O(N)
                buffer_stack.push(self.team.serve())#O(1)
            
            for _ in range(back_half): #O(N)
                self.team.append(buffer_stack.pop())#O(1)
            for _ in range(front_half):#O(N)
                self.team.append(buffer_queue.serve())#O(1)
            
        elif self.team_mode.name == "OPTIMISE": 
            """everything unless stated otherwise is o(1)
            Best case O(n^2)  Worst case O(n * n) = O(n^2) n being len(self)"""
            buffer_list = ArraySortedList(self.TEAM_LIMIT)
            team_length = len(self.team)
            for _ in range(team_length):    #O(N)
                monster_and_key = self.team.delete_at_index(0)   #Best case O(len(self)) worst case O(len(self))
                monster = monster_and_key.value
                key_reversed = monster_and_key.key * -1
                monster_and_reversed_key = ListItem(monster, key_reversed)
                buffer_list.add(monster_and_reversed_key)#Best case O(log(n)) Worst case O(n)  
            for _ in range(team_length):#O(N)
                self.team.add(buffer_list.delete_at_index(0))#Best case Worst case O(n)  
            if self.reversed == False:
                self.reversed = True
            elif self.reversed == True:
                self.reversed == False

    def regenerate_team(self) -> None:
        """ everything unless stated otherwise is o(1)
        N = len(self)
        best case
        O(N*1)
        
        Worst case
        O(N*N)
        
        
        """
        while len(self.team):               #empty out team. While loop runs len(self times)
            self.retrieve_from_team()       # o(1) best case o(n) Worst case


        if self.team_mode.name == "FRONT":
            """ everything unless stated otherwise is o(1)
            N = len(self)
            o(n+n) = o(n)"""
            buffer_stack_copy = ArrayStack(6)
            buffer_stack = ArrayStack(6)
            while len(self.team_original): #o(n)
                monster = self.team_original.pop() 
                monster_copy = type(monster)(simple_mode=monster.simple_mode, level=monster.level)
                buffer_stack_copy.push(monster_copy)
                buffer_stack.push(monster)

            while len(buffer_stack):  #o(n)
                monster_copy = buffer_stack_copy.pop()
                monster = buffer_stack.pop()
                self.add_to_team(monster_copy) #o(1)
                self.team_original.push(monster)
            
        elif self.team_mode.name == "BACK":
            """ everything unless stated otherwise is o(1)
            N = len(self)
            o(n+n) = o(n)"""
            buffer_queue = CircularQueue(6)
            while len(self.team_original):  #runs len(self) times   
                monster = self.team_original.serve()
                monster_copy = type(monster)(simple_mode=monster.simple_mode, level=monster.level)
                self.add_to_team(monster_copy)
                buffer_queue.append(monster)
            while len(buffer_queue): #o(n)
                self.team_original.append(buffer_queue.serve())
            


        elif self.team_mode.name == "OPTIMISE":
            """everything unless stated otherwise is o(1)
            N = len(self)
            Best case o(n^2))
            Worst case o(n^2)"""
            self.reversed = False
            buffer_slist = ArraySortedList(6)
            while len(self.team_original): #o(n)
                monster_and_key = self.team_original.delete_at_index(0)     #O(len(self)) worst case
                monster = monster_and_key.value
                monster_copy = type(monster)(simple_mode=monster.simple_mode, level=monster.level)
                self.add_to_team(monster_copy)
                buffer_slist.add(monster_and_key) #Best case O(log(n)) Worst case O(n)
            while len(buffer_slist): #o(n)
                self.team_original.add(buffer_slist.delete_at_index(0))     #O(len(self)) worst case


                


                
            

        

    def select_randomly(self):
        """everything unless stated otherwise is o(1)
        N = len(self)
        Best case = O(n*log(n))
        Worst case O(n^2)"""
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

                        if self.team_mode.name == "FRONT": 
                            """everything unless stated otherwise is o(1)
                            O(1) best and worst case"""
                            self.team_original.push(monsters[x]())

                        elif self.team_mode.name == "BACK":   
                            """everything unless stated otherwise is o(1)
                            O(1) best and worst case"""  
                            self.team_original.append(monsters[x]())

                        elif self.team_mode.name == "OPTIMISE": 
                            """everything unless stated otherwise is o(1)
                            Best case O(log(n)) Worst case O(n) """
                            if self.sort_method == MonsterTeam.SortMode.HP:
                                monster_and_key = ListItem(monsters[x](), monsters[x]().get_hp() * -1)
                            elif self.sort_method == MonsterTeam.SortMode.ATTACK:
                                monster_and_key = ListItem(monsters[x](), monsters[x]().get_attack() * -1)
                            elif self.sort_method == MonsterTeam.SortMode.DEFENSE:
                                monster_and_key = ListItem(monsters[x](), monsters[x]().get_defense() * -1)
                            elif self.sort_method == MonsterTeam.SortMode.SPEED:
                                monster_and_key = ListItem(monsters[x](), monsters[x]().get_speed() * -1)
                            elif self.sort_method == MonsterTeam.SortMode.LEVEL:
                                monster_and_key = ListItem(monsters[x](), monsters[x]().get_level() * -1)
                            self.team_original.add(monster_and_key)   #Best case O(log(n)) Worst case O(n) 
                        break
            else:
                raise ValueError("Spawning logic failed.")

    def select_manually(self):
        """everything unless stated otherwise is o(1)
        n = len(self)
        Best case o(n)
        Worst case o(n^2)"""
        check = False
        while check == False: # check and input assumed o(1)
            Team_size = input("How many monsters are there?")
            try: 
                Team_size = int(Team_size)
                if Team_size <= self.TEAM_LIMIT and Team_size > 0:
                    check = True
            except:
                print("Please enter an integer between 1 and 6")


        check = False
        for _ in range(Team_size): #O(n)
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
            while check == False: #o(1)
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
            
            self.add_to_team(monsters[monster_pick - 1]())#O(1) Best case O(n) worst case

            if self.team_mode.name == "FRONT": 
                self.team_original.push(monsters[monster_pick - 1]()) #o(1)
            elif self.team_mode.name == "BACK":     
                self.team_original.append(monsters[monster_pick - 1]()) #o(1)
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
                self.team_original.add(monster_and_key) #Best case O(log(n)) Worst case O(n)     


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
        """everything unless stated otherwise is o(1)
        n = len(self)
        Best case o(n)'
        Worst case o(n^2)"""
        if len(provided_monsters) > 6:
            raise ValueError()
        for i in range(len(provided_monsters)): #o(n)
            monster = provided_monsters.__getitem__(i)()
            if provided_monsters.__getitem__(i).can_be_spawned() == False:
                raise ValueError(provided_monsters.__getitem__(i), "cannot be spawned")

            monster_copy = provided_monsters.__getitem__(i)()
            self.add_to_team(monster)#O(1) Best case O(n) worst case
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
                self.team_original.add(monster_and_key) #Best case O(log(n)) Worst case O(n) 


    def choose_action(self, currently_out: MonsterBase, enemy: MonsterBase) -> Battle.Action:
        # This is just a placeholder function that doesn't matter much for testing.
        from battle import Battle
        if currently_out.get_speed() >= enemy.get_speed() or currently_out.get_hp() >= enemy.get_hp():
            return Battle.Action.ATTACK
        return Battle.Action.SWAP

if __name__ == "__main__":

    # team = MonsterTeam(
    #     team_mode=MonsterTeam.TeamMode.OPTIMISE,
    #     selection_mode=MonsterTeam.SelectionMode.PROVIDED,
    #     sort_key=MonsterTeam.SortMode.HP,
    #     provided_monsters=ArrayR.from_list([Flamikin, Aquariuma, Vineon, Thundrake, Thundrake, Thundrake])
    # )

    # print('*******')
    # print(team)

    # hi = team.retrieve_from_team()
    # hi.set_hp(2)
    # team.add_to_team(hi)

    # while len(team):
    #     print(team.retrieve_from_team())
    
    # team.regenerate_team()
    # print('\n')

    # team.special()

    # hi = team.retrieve_from_team()
    # hi.set_hp(2)
    # team.add_to_team(hi)

    # team.regenerate_team()
    
    # while len(team):
    #     print(team.retrieve_from_team())




    


    class WeakThundrake(Thundrake):
        def get_max_hp(self):
            return 5
    my_monsters = ArrayR(4)
    my_monsters[0] = Flamikin   # 6 HP
    my_monsters[1] = Aquariuma  # 8 HP
    my_monsters[2] = Rockodile  # 9 HP
    my_monsters[3] = WeakThundrake  # 5 HP
    team = MonsterTeam(
        team_mode=MonsterTeam.TeamMode.OPTIMISE,
        selection_mode=MonsterTeam.SelectionMode.PROVIDED,
        sort_key=MonsterTeam.SortMode.HP,
        provided_monsters=my_monsters,
    )
    # Rockodile, Aquariuma, Flamikin, Thundrake
    rockodile = team.retrieve_from_team()
    aquariuma = team.retrieve_from_team()
    flamikin = team.retrieve_from_team()
    print(rockodile, Rockodile)
    print(aquariuma, Aquariuma)
    print(flamikin, Flamikin)

    rockodile.set_hp(2)
    flamikin.set_hp(4)
    team.add_to_team(rockodile)
    team.add_to_team(aquariuma)
    team.add_to_team(flamikin)
    # Aquariuma, Thundrake, Flamikin, Rockodile

    team.special()
    # Rockodile, Flamikin, Thundrake, Aquariuma
    rockodile = team.retrieve_from_team()
    flamikin = team.retrieve_from_team()
    print(rockodile, Rockodile)
    print(flamikin, Flamikin)


    flamikin.set_hp(1)
    team.add_to_team(flamikin)
    team.add_to_team(rockodile)

    flamikin = team.retrieve_from_team()
    print(flamikin, Flamikin)

    team.regenerate_team()
    # Back to normal sort order and Rockodile, Aquariuma, Flamikin, Thundrake
    while len(team):
        print(team.retrieve_from_team())


    # rockodile = team.retrieve_from_team()
    # aquariuma = team.retrieve_from_team()
    # print(rockodile, Rockodile)
    # print(aquariuma, Aquariuma)
    # print(rockodile.get_hp(), 9)
    # print(aquariuma.get_hp(), 8)
    