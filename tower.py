from __future__ import annotations

from random_gen import RandomGen
from team import MonsterTeam
from battle import Battle

from elements import Element

from data_structures.queue_adt import CircularQueue
from data_structures.stack_adt import ArrayStack
from data_structures.referential_array import ArrayR
from data_structures.sorted_list_adt import ListItem

class BattleTower:

    MIN_LIVES = 2
    MAX_LIVES = 10

    def __init__(self, battle: Battle|None=None) -> None:
        self.battle = battle or Battle(verbosity=0)
        


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
        
            
        preteam = ArrayStack(6)
        
        preteam.push(self.enemy_team_out.retrieve_from_team().get_element()) #grab all elements from preteam
        #removes anything from team 2 and player


        for element in Element:








    def sort_by_lives(self):
        # 1054 ONLY
        raise NotImplementedError

def tournament_balanced(tournament_array: ArrayR[str]):
    # 1054 ONLY
    raise NotImplementedError

if __name__ == "__main__":

    RandomGen.set_seed(129371)

    bt = BattleTower(Battle(verbosity=3))
    bt.set_my_team(MonsterTeam(MonsterTeam.TeamMode.BACK, MonsterTeam.SelectionMode.RANDOM))
    bt.generate_teams(3)

    bt.next_battle()
