from __future__ import annotations

from random_gen import RandomGen
from team import MonsterTeam
from battle import Battle

from elements import Element

from data_structures.queue_adt import CircularQueue

from data_structures.referential_array import ArrayR
from data_structures.bset import BSet

class BattleTower:

    MIN_LIVES = 2
    MAX_LIVES = 10

    def __init__(self, battle: Battle|None=None) -> None:
        self.battle = battle or Battle(verbosity=0)
        self.elements_so_far = BSet()

        


    def set_my_team(self, team: MonsterTeam) -> None:
        # Generate the team lives here too.
        self.player_team = team
        self.lives = RandomGen.randint(self.MIN_LIVES, self.MAX_LIVES)


    def generate_teams(self, n: int) -> None:
        self.enemy_teams = CircularQueue(n)
        for _ in range(n):
            self.enemy_teams.append(((MonsterTeam(team_mode=MonsterTeam.TeamMode.BACK,selection_mode=MonsterTeam.SelectionMode.RANDOM)), RandomGen.randint(self.MIN_LIVES, self.MAX_LIVES)))

    def battles_remaining(self) -> bool:
        if self.enemy_teams.is_empty():
            return False
        else:
            if self.lives <= 0:
                return False
            return True
        

    def next_battle(self) -> tuple[Battle.Result, MonsterTeam, MonsterTeam, int, int]:
        b = Battle(1)

        enemy_team_and_lives = self.enemy_teams.serve()
        self.enemy_team_out = enemy_team_and_lives[0]
        enemy_team_out_lives = enemy_team_and_lives[1]
        print(len(self.player_team))
        self.enemy_team_out.regenerate_team()
        self.player_team.regenerate_team()
        print("Team 1 has", len(self.player_team),"monsters and", self.lives, "lives!")
        print("Team 2 has", len(self.enemy_team_out),"monsters and", enemy_team_out_lives, "lives!")
        result = b.battle(self.player_team, self.enemy_team_out)
        self.enemy_team_out.regenerate_team()
        self.player_team.regenerate_team()
        if result == Battle.Result.TEAM1:
            enemy_team_out_lives -= 1
        elif result == Battle.Result.TEAM2:
            self.lives -= 1

        elif result == Battle.Result.DRAW:
            self.lives -= 1
            enemy_team_out_lives -= 1

        

        if enemy_team_out_lives > 0:
            self.enemy_teams.append((self.enemy_team_out, enemy_team_out_lives))
        print (result)
 
        return [result, self.player_team, self.enemy_team_out, self.lives, enemy_team_out_lives]

    def out_of_meta(self) -> ArrayR[Element]:
        
        next_team = self.enemy_teams.peek()[0]
        preteam = BSet()
        player_team = BSet()
        next_team_elements = BSet()
        no_meta = ArrayR(0)
        out_of_meta_Bset = BSet()
        
        try:
            len(self.enemy_team_out)
        except:
            return no_meta
        
        while len(self.enemy_team_out):
            preteam.add(Element.from_string(self.enemy_team_out.retrieve_from_team().get_element()).value) #grab all elements from preteam
        while len(self.player_team):   
            player_team.add(Element.from_string(self.player_team.retrieve_from_team().get_element()).value) #grabs all elements from player team
        while len(next_team):
            next_team_elements.add(Element.from_string(next_team.retrieve_from_team().get_element()).value)
        

        self.elements_so_far = self.elements_so_far.union(player_team)
        self.elements_so_far = self.elements_so_far.union(preteam)
        #removes anything from team 2 and player
        out_of_meta_Bset = self.elements_so_far.difference(player_team)
        out_of_meta_Bset = out_of_meta_Bset.difference(next_team_elements)

        self.enemy_team_out.regenerate_team()
        self.player_team.regenerate_team()

        out_of_meta = ArrayR(len(out_of_meta_Bset))
        i = 0
        for element in Element:
            if out_of_meta_Bset.__contains__(element.value):
                out_of_meta.__setitem__(i,element)
                i +=1
        return out_of_meta









def sort_by_lives(self):
    # 1054 ONLY
    raise NotImplementedError

def tournament_balanced(tournament_array: ArrayR[str]):
    # 1054 ONLY
    raise NotImplementedError

if __name__ == "__main__":

    # RandomGen.set_seed(129371)

    # bt = BattleTower(Battle(verbosity=3))
    # bt.set_my_team(MonsterTeam(MonsterTeam.TeamMode.BACK, MonsterTeam.SelectionMode.RANDOM))
    # bt.generate_teams(3)

    # bt.next_battle()
    from helpers import Flamikin, Faeboa
    RandomGen.set_seed(123456789)
    bt = BattleTower(Battle(verbosity=0))
    bt.set_my_team(MonsterTeam(
        team_mode=MonsterTeam.TeamMode.BACK,
        selection_mode=MonsterTeam.SelectionMode.PROVIDED,
        provided_monsters=ArrayR.from_list([Faeboa])
    ))
    bt.generate_teams(3)
    # The following teams should have been generated:
    # 1 (7 lives): Strikeon, Faeboa, Shockserpent, Gustwing, Vineon, Pythondra
        # Fighting, Fairy, Electric, Flying, Grass, Dragon

    # 2 (5 lives): Iceviper, Thundrake, Groundviper, Iceviper, Metalhorn
        # Ice, Electric, Ground, Steel

    # 3 (3 lives): Strikeon
        # Fighting

    # When no games have been played, noone is outside of the meta.
    print(bt.out_of_meta().to_list())
    result, t1, t2, l1, l2 = bt.next_battle()
    # After the first game, Fighting, Flying, Grass and Dragon are no longer in the meta.
    # Electric & Fairy are still present in the battle between the two.

    print(bt.out_of_meta().to_list(), [Element.GRASS, Element.DRAGON, Element.FIGHTING, Element.FLYING])
    result, t1, t2, l1, l2 = bt.next_battle()
    # After the second game, Flying, Grass, Dragon, Ice, Electric, Ground, Steel are no longer present.
    print(bt.out_of_meta().to_list(), [Element.GRASS, Element.DRAGON, Element.ELECTRIC, Element.FLYING, Element.GROUND, Element.ICE, Element.STEEL])
    result, t1, t2, l1, l2 = bt.next_battle()
    # After the third game, We are just missing Ice, Ground and Steel.
    print(bt.out_of_meta().to_list(), [Element.GROUND, Element.ICE, Element.STEEL])
    result, t1, t2, l1, l2 = bt.next_battle()
    # After the fourth game, We are back to missing Grass, Dragon, Fighting and Flying
    print(bt.out_of_meta().to_list(), [Element.GRASS, Element.DRAGON, Element.FIGHTING, Element.FLYING])

