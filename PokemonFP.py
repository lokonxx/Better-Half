# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 10:35:11 2019

Final Project II - Pocket Monsters

Authors@author: Kenneth Tang and Nathan Tran
@email: ketang@clarku.edu / natran@clarku.edu

"""
from playsound import playsound
import random

class Pokemon:
    
    def __init__(self, name, hp, thp, lvl, att, de, spAtt, spDe, sp, typ, moves):
        ''' initializes a type of pokemon with its stats and characteristics'''
        
        self.n = name        # name
        self.hp = hp         # current health
        self.thp = thp       # total health
        self.l = lvl         # level
        self.a = att         # attack
        self.d = de          # defense
        self.spa = spAtt     # special attack
        self.spd = spDe      # special defense
        self.s = sp          # speed
        self.t = typ         # type
        self.m = moves       # moves
        
    
    def __repr__(self):
        
        # ex. ['Charmander', '20', '20', '5', '11', '10', '60', 'Fire', 'Scratch']
        s = '[' + str(self.n) + ', HP: ' + str(self.hp) + '/' + str(self.thp) + ', LVL: '+ \
        str(self.l) + ', ATT: '+ str(self.a) + ', DEF: ' + str(self.d) + ', TYPE: ' \
        + str(self.t) + ', MOVES: ' + str(self.m) + ']'
        return s


class Player:
    
    def __init__(self, player, activePokemon, partyPokemon1, partyPokemon2):
        ''' initializes the state of the player's active and party Pokemon'''
        
        self.p = player            # player name
        self.ap = activePokemon    # active pokemon
        self.pp1 = partyPokemon1   # party pokemon 1
        self.pp2 = partyPokemon2   # party pokemon 2
        
    def __repr__(self):
        
        # ex. ['Player1', 'Charmander', 'Pikachu', 'Squirtle']
        s = '[' + str(self.p) + ', *' + str(self.ap) + ', ' + str(self.pp1) + ', ' + \
        str(self.pp2) + ']'
        return s
        
    def switchToParty1(self):
        ''' switches out activePokemon with partyPokemon1'''
        
        # redirects address of variables
        buffer = '' 
        buffer = self.ap
        self.ap = self.pp1
        self.pp1 = buffer
        
        return self
    
    def switchToParty2(self):
        ''' switches out activePokemon with partyPokemon2'''
        
        # redirects address of variables
        buffer = ''
        buffer = self.ap
        self.ap = self.pp2
        self.pp2 = buffer
        
        return self
        
        
class Battle:
    
    def __init__(self, p1, p2):
        ''' initializes state of the battle with the active pokemon p1 and p2 
            being from the Pokemon class.
        '''
        # Active Pokemon for player 1 and player 2
        self.p1 = p1
        self.p2 = p2    
    
    def __repr__(self):
        
        # display to the console the health of rival and player. displayed in form of current / total
        s1 = str(self.p2.p) + ': ' + str(self.p2.ap.n) + ' (LVL: ' + str(self.p2.ap.l) + ') (HP: ' +\
        str(self.p2.ap.hp) + '/' + str(self.p2.ap.thp) + ') \n'
        s2 = str(self.p1.p) + '(You): ' + str(self.p1.ap.n) + ' (LVL: ' + str(self.p1.ap.l) + ') (HP: ' +\
        str(self.p1.ap.hp) + '/' + str(self.p1.ap.thp) + ')'
        return '\n' + s1 + '\n' + s2
    
    
    def p1action(self, move):
        """" processes the move that player 1 inputted"""
        
        # list covers moves with 40 power. These are all the moves currently in the game and all does 40 power
        x = getDamageDictionary()
        for i in x:
            if move in x[i]:
                power = i

           
        # damage done to rival's active pokemon
        ps = getMovePSDictionary(move)
        if ps == 'Physical':
            
            damage = (((2* self.p1.ap.l/5 +2) * power * self.p1.ap.a/ self.p2.ap.d)/50)+2  # damage calculator
        elif ps == 'Special':
            damage = (((2* self.p1.ap.l/5 +2) * power * self.p1.ap.spa/ self.p2.ap.spd)/50)+2  # damage calculator
        else:
            damage = 0
        # tests if critical strike occurs (1/16 chance), if yes, damage * 1.5
        critchance = random.randint(84, 100)
        if critchance == 100:
            damage *= 1.5
            critchance = True
            
        # tests if move type matches active pokemon's type, if yes, damage * 1.5
        x = getMoveType(move)
        if x in self.p1.ap.t:
            damage *= 1.5
            
        # tests type effectiveness
        numTypes = countNumTypes(self.p2.ap.t)
        y = 1
        for k in range(numTypes):
           y *= effectiveness(self.p2.ap.t[k], x) 
        damage *= y
        
        damage = round(damage) # rounded to nearest integer      
        self.p2.ap.hp -= damage     # subtracts damage from health of player 2's active pokemon
        if self.p2.ap.hp < 0:
            self.p2.ap.hp = 0
        print('\n--You used ' + move + '!')
        
        if damage == 0 and move == 'Splash':
            print('\n--But it did nothing!')
            
        if y == 0:
            print('\n--It had no effect!')
        
        if y > 0 and y < 1:
            print("\n--It wasn't very effective.")
        
        if y > 1:
            print('\n--It was super effective!')
            
        if critchance == True:
            print('\n--A critical hit!')
        
        
    def p2action(self, move):
        """ processes the move that player 1 inputted """
        
        # list covers moves with 40 power. These are all the moves currently in the game and all does 40 power
        x = getDamageDictionary()
        for i in x:
            if move in x[i]:
                power = i
        
        # damage done to rival's active pokemon
        ps = getMovePSDictionary(move)
        if ps == 'Physical':
            
            damage = (((2* self.p1.ap.l/5 +2) * power * self.p2.ap.a/ self.p1.ap.d)/50)+2  # damage calculator
        elif ps == 'Special':
            damage = (((2* self.p1.ap.l/5 +2) * power * self.p2.ap.spa/ self.p1.ap.spd)/50)+2  # damage calculator
        else:
            damage = 0
        # tests if critical strike occurs (1/16 chance), if yes, damage * 1.5
        critchance = random.randint(84, 100)
        if critchance == 100:
            damage *= 1.5
            critchance = True
        
        # tests if move type matches active pokemon's type, if yes, damage * 1.5
        x = getMoveType(move)
        if x in self.p2.ap.t:
            damage *= 1.5
        
        # tests type effectiveness
        numTypes = countNumTypes(self.p1.ap.t)
        y = 1
        for k in range(numTypes):
           y *= effectiveness(self.p1.ap.t[k], x) 
           
        damage *= y    
        damage = round(damage)  # rounded to nearest integer
        self.p1.ap.hp -= damage      # subtracts damage from health of player 1's active pokemon
        if self.p1.ap.hp < 0:
            self.p1.ap.hp = 0
        print('\n--Your rival used ' + move + '!')
        
        if damage == 0 and move == 'Splash':
            print('\n--But it did nothing!')
            
        if y == 0:
            print('\n--It had no effect!')
        
        if y > 0 and y < 1:
            print("\n--It wasn't very effective.")
        
        if y > 1:
            print('\n--It was super effective!')
        
        if critchance == True:
            print('\n--A critical hit!')
        

def main():
    """ user interface to interact with program"""
    
    print('\nHello. Welcome to the development beta of our final project for CS 120 at Clark University. ' \
          + 'Our project is a Pokemon Battle Simulation using what we"ve learned in CS120. ' \
          + 'Press "q" anytime to quit or go back.')
    
    # reads from spreadsheet and initializes pokemon
    stats = PokeStats('PokemonRoster1.csv')
            
    # player 1 active pokemon out in battle, within the Battle class
    p1active = Pokemon(str(stats[0][0]), int(stats[0][1]), int(stats[0][2]), int(stats[0][3]), int(stats[0][4]), int(stats[0][5]), int(stats[0][6]), int(stats[0][7]), int(stats[0][8]), stats[0][9].split('/'), (stats[0][10]).split('/'))
    # player 1 party pokemon
    p1party1 = Pokemon(str(stats[1][0]), int(stats[1][1]), int(stats[1][2]), int(stats[1][3]), int(stats[1][4]), int(stats[1][5]), int(stats[1][6]), int(stats[1][7]), int(stats[1][8]), stats[1][9].split('/'), (stats[1][10]).split('/'))
    p1party2 = Pokemon(str(stats[2][0]), int(stats[2][1]), int(stats[2][2]), int(stats[2][3]), int(stats[2][4]), int(stats[2][5]), int(stats[2][6]), int(stats[2][7]), int(stats[2][8]), stats[2][9].split('/'), (stats[2][10]).split('/'))
    
    # player 2 active pokemon out in battle, within the Battle class
    p2active = Pokemon(str(stats[3][0]), int(stats[3][1]), int(stats[3][2]), int(stats[3][3]), int(stats[3][4]), int(stats[3][5]), int(stats[3][6]), int(stats[3][7]), int(stats[3][8]), stats[3][9].split('/'), (stats[3][10]).split('/'))
    # player 2 party pokemon
    p2party1 = Pokemon(str(stats[4][0]), int(stats[4][1]), int(stats[4][2]), int(stats[4][3]), int(stats[4][4]), int(stats[4][5]), int(stats[4][6]), int(stats[4][7]), int(stats[4][8]), stats[4][9].split('/'), (stats[4][10]).split('/'))
    p2party2 = Pokemon(str(stats[5][0]), int(stats[5][1]), int(stats[5][2]), int(stats[5][3]), int(stats[5][4]), int(stats[5][5]), int(stats[5][6]), int(stats[5][7]), int(stats[5][8]), stats[5][9].split('/'), (stats[5][10]).split('/'))
    
    #initialize Player classes to manage party
    player1 = Player(str(stats[6][1]), p1active, p1party1, p1party2)
    player2 = Player(str(stats[6][3]), p2active, p2party1, p2party2)
    
    # initializes Battle class that interacts with active pokemon
    c = Battle(player1, player2)
    print(c)
    playsound('Rival Theme.mp3', 0)
    
    while True:
        # prevents players from wrong inputs to switch Pokemon when active Pokemon is dead
        if c.p1.ap.hp < 1:
            
            choice2 = input('*Party:\n[' + str(c.p1.pp1.n) + ' (LVL: ' + str(c.p1.pp1.l) + ') (HP: ' + str(c.p1.pp1.hp) + '/' + str(c.p1.pp1.thp) + ') = "1"] [' \
                    + str(c.p1.pp2.n) + ' (LVL: ' + str(c.p1.pp2.l) + ') (HP: ' + str(c.p1.pp2.hp) + '/' + str(c.p1.pp2.thp) + ') = "2"] \n')
            
            if choice2 == '1':   # switches to party Pokemon 1
                p1SwitchToPP1(c)
        
            elif choice2 == '2':   # switches to party Pokemon 2
                p1SwitchToPP2(c)
            else:
                print('\nPlease choose a Pokemon.')
                
        # where the code really starts    
        else:
            
            choice = input('*Please choose your input: \n[Attack = "a"] [Party = "p"] [Quit = "q"] \n')
            
                
            if choice == 'q':   # quits the game
                print('\nThis simulation was made by Kenneth Tang and Nathan Tran. ' \
                       'Thanks for playing!')
                break
            
            elif choice == 'a':
                
                choice2 = input('*Please choose your move: \n[' + str(c.p1.ap.m[0]) + ' = "1"] [' + str(c.p1.ap.m[1]) + ' = "2"] [' + str(c.p1.ap.m[2]) + ' = "3"] [' + str(c.p1.ap.m[3]) + ' = "4"] \n')
                
                if choice2 in ['1', '2', '3', '4']:
                    
                    # player 1 uses 1a move. Currently each Pokemon can also use one move
                    if str(c.p1.ap.m[int(choice2) - 1]) == 'Quick Attack':
                        if p1FirstProcessTurn(c, str(c.p1.ap.m[int(choice2) - 1])) == False:
                            print('\nThis simulation was made by Kenneth Tang and Nathan Tran. ' \
                                  'Thanks for playing!')
                            break
                        
                    elif str(c.p2.ap.m[int(choice2) - 1]) == 'Quick Attack':
                        if p2FirstProcessTurn(c, str(c.p1.ap.m[int(choice2) - 1])) == False:
                            print('\nThis simulation was made by Kenneth Tang and Nathan Tran. ' \
                                  'Thanks for playing!')
                            break
                        
                    elif c.p1.ap.s >= c.p2.ap.s :   # if the speed of player's pokemon is faster
                        
                        if p1FirstProcessTurn(c, str(c.p1.ap.m[int(choice2) - 1])) == False:
                            print('\nThis simulation was made by Kenneth Tang and Nathan Tran. ' \
                                  'Thanks for playing!')
                            break
                            
                    else:   # if rival pokemon is faster
                        if p2FirstProcessTurn(c, str(c.p1.ap.m[int(choice2) - 1])) == False:
                            print('\nThis simulation was made by Kenneth Tang and Nathan Tran. ' \
                                  'Thanks for playing!')
                            break
                        
                else:
                    print("\n" + "That's not a valid choice yet. Try again.")
                    
            elif choice == 'p':
                # menu, pulls up the Pokemon currently in your party
                choice2 = input('*Party:\n[' + str(c.p1.pp1.n) + ' (LVL: ' + str(c.p1.pp1.l) + ') (HP: ' +\
                                str(c.p1.pp1.hp) + '/' + str(c.p1.pp1.thp) + ') = "1"] [' + str(c.p1.pp2.n) + \
                               ' (LVL: ' + str(c.p1.pp2.l) + ') (HP: ' + str(c.p1.pp2.hp) + '/' + str(c.p1.pp2.thp) + ') = "2"] \n')
                
                if choice2 == '1':         
                    p1SwitchToPP1(c)       # switches to party Pokemon 1
                    c.p2action(c.p2.ap.m[random.randint(0,3)])  # takes damage for switching
                    print(c)
            
                elif choice2 == '2':
                    p1SwitchToPP2(c)       # switches to party Pokemon 2
                    c.p2action(c.p2.ap.m[random.randint(0,3)])  # takes damage for switching
                    print(c)
            else:
                print("\n" + "That's not a valid choice. Try again.")
                

def getMoveType(move):
    ''' Used in damage calculating function. Returns the type of the move used'''
    
    d = getMoveDictionary()  # contains a dictionary of the types corresponding moves
    
    for i in d:
        if move in d[i]:     # checks if move is in the values of key
            return i         # return key (type)
    
        
def p1SwitchToPP1(c):
    ''' Switches to party Pokemon 1 by calling a method in Player'''
    
    # check hp of party Pokemon 1
    if c.p1.pp1.hp < 1:
        print('\n' + '--This Pokemon fainted already!' )
    
    # executes switch    
    else:
        c.p1.switchToParty1()
        print('\n' + '--Switch! You can do it ' + str(c.p1.ap.n) + '!')
        print(c)  

        
def p1SwitchToPP2(c):
    ''' Switches to party Pokemon 2 by calling a method in Player'''
    
    # checks hp of party Pokemon 2
    if c.p1.pp2.hp < 1:
        print('\n' + '--This Pokemon fainted already!')
    
    # executes switch    
    else:
        c.p1.switchToParty2()
        print('\n' + "--Switch! I'm counting on you " + str(c.p1.ap.n) + "!") 
        print(c)

def p2PartyRandomSwitch(c):
    
    switchChance = random.randint(0,1)
            
    if switchChance == 0:
        
        c.p2.switchToParty1()
        p2FaintedChoice(c)
        print('\n' + "--Your opponent sent out " + str(c.p2.ap.n) + "!")
        print(c)
        return True  
    else:
        
        c.p2.switchToParty2()
        p2FaintedChoice(c)
        print('\n' + "--Your opponent sent out " + str(c.p2.ap.n) + "!")
        print(c)
        return True

def apFaintedChoice1(c):
    
    if c.p1.pp1.hp >= 1:
                
        c.p1.switchToParty1()

        print('\n' + '--You got this ' + str(c.p1.ap.n) + '!')
        print(c)
        return True

    else:
        print('This Pokemon already fainted!')
        return True
    
def apFaintedChoice2(c):
    
    if c.p1.pp2.hp >= 1:

        c.p1.switchToParty2()
    
        print('\n' + '--I believe in you, ' + str(c.p1.ap.n) + '!')
        print(c)
        return True
    
    else:
        print('This Pokemon already fainted!')  
        return True

def p2FaintedChoice(c):
    
    print('\n' + "Your opponent's Pokemon fainted!")
    choice = input('Your opponent is about to send out ' + str(c.p2.ap.n) + \
                   '. Would you like to switch Pokemon?' + '\n' + \
                   '[Yes = "y"] [No = "n"]' + '\n')
    if choice == 'y':
        choice2 = input('*Party:\n[' + str(c.p1.pp1.n) + ' (LVL: ' + str(c.p1.pp1.l) + \
                        ') (HP: ' + str(c.p1.pp1.hp) + '/' + str(c.p1.pp1.thp) + ') = "1"] [' \
                        + str(c.p1.pp2.n) + ' (LVL: ' + str(c.p1.pp2.l) + ') (HP: ' + \
                        str(c.p1.pp2.hp) + '/' + str(c.p1.pp2.thp) + ') = "2"] [Back = "q"]\n')
        
        if choice2 == '1':         
            p1SwitchToPP1(c)       # switches to party Pokemon 1
            
    
        elif choice2 == '2':
            p1SwitchToPP2(c)       # switches to party Pokemon 2
            
            
def p1FirstProcessTurn(c, p1Move):
    ''' Executes if player inputs a move from Attack choice, and their active
        Pokemon's speed is higher than opponent 
    '''
    
    # method processes move for damage
    c.p1action(p1Move)
    print(c)
    if c.p2.ap.hp < 1:   # if player 2's active pokemon's hp is less than 1, or fainted
        
        if c.p2.pp1.hp < 1 and c.p2.pp2.hp < 1:   # if both of the rival's party pokemon is fainted, then player 1 wins
            print('\n' + 'You won!')
            return False
        # if both party Pokemon are still alive, send one out randomly
        elif c.p2.pp1.hp >= 1 and c.p2.pp2.hp >= 1:
            
            return p2PartyRandomSwitch(c)
            
        elif c.p2.pp1.hp >= 1:   # if the rival's first party Pokemon fainted, send out the second Pokemon
            
            # swapping active pokemon slot with party pokemon slot
            c.p2.switchToParty1()
            # initializes Battle once active pokemon is updated
            p2FaintedChoice(c)
                    
            print('\n' + "--Your opponent sent out " + str(c.p2.ap.n) + "!")
            print(c)
            return True
            
        elif c.p2.pp2.hp >= 1:   # if the rival's second party Pokemon fainted, send out the first Pokemon
            
            # swapping active pokemon slot with party pokemon slot
            c.p2.switchToParty2()
            
              # initializes Battle once active pokemon is updated
            p2FaintedChoice(c)
            print('\n' + "--Your opponent sent out " + str(c.p2.ap.n) + "!" + '\n')
            print(c)
            return True
        
    else:
        # if player 2's pokemon does not faint, their move goes through
        
        c.p2action(c.p2.ap.m[random.randint(0,3)])  
        print(c)
        if c.p1.ap.hp < 1: # when player 1's active pokemon faints
            print('\n--Your Pokemon fainted!')
            
            if c.p1.pp1.hp < 1 and c.p1.pp2.hp < 1:
                print('\n' + 'You lost!')
                return False
            
            # player decides what Pokemon to send out
            choice = input('*Party:\n[' + str(c.p1.pp1.n) + ' (LVL: ' + str(c.p1.pp1.l) + \
                            ') (HP: ' + str(c.p1.pp1.hp) + '/' + str(c.p1.pp1.thp) + ') = "1"] [' \
                            + str(c.p1.pp2.n) + ' (LVL: ' + str(c.p1.pp2.l) + ') (HP: ' + \
                            str(c.p1.pp2.hp) + '/' + str(c.p1.pp2.thp) + ') = "2"] \n')
            
            if choice == '1': # switch to party Pokemon 1
                
                return apFaintedChoice1(c)
                
            elif choice == '2': # switch to party Pokemon 2
                
                return apFaintedChoice2(c)
            
            else:
                print('\nPlease choose a Pokemon.')
                return True
        
        else:
            
            return True

def p2FirstProcessTurn(c, p1Move):
    '''
    Executes if player inputs a move from Attack choice, and their active
    Pokemon's speed is lower than opponent 
    '''
    # method processes move for damage
    c.p2action(c.p2.ap.m[random.randint(0,3)])  
    print(c)
    if c.p1.ap.hp < 1: # when player 1's active pokemon faints, similar behavior to player 2 above
        print('\n--Your Pokemon fainted!')
        
        if c.p1.pp1.hp < 1 and c.p1.pp2.hp < 1:
            print('\n' + 'You lost!')
            return False
        
        choice = input('*Party:\n[' + str(c.p1.pp1.n) + ' (LVL: ' + str(c.p1.pp1.l) + \
                        ') (HP: ' + str(c.p1.pp1.hp) + '/' + str(c.p1.pp1.thp) + ') = "1"] [' \
                        + str(c.p1.pp2.n) + ' (LVL: ' + str(c.p1.pp2.l) + ') (HP: ' + \
                        str(c.p1.pp2.hp) + '/' + str(c.p1.pp2.thp) + ') = "2"] \n')
        
        # player decides which Pokemon to send out
        if choice == '1':
            
            return apFaintedChoice1(c)
            
        elif choice == '2':
            
            return apFaintedChoice2(c)
        
        else:
            print('\nPlease choose a Pokemon.')
            return True
    
    
    else:
        # if player's active pokemon does not faint, their move goes through
        c.p1action(p1Move)
        print(c)
        if c.p2.ap.hp < 1: # when rival's active pokemon faints, similar behavior to player above
            
            if c.p2.pp1.hp < 1 and c.p2.pp2.hp < 1:
                print('\n' + 'You Won!')
                return False
            
            # if both party Pokemon are still alive, send one out randomly
            elif c.p2.pp1.hp >= 1 and c.p2.pp2.hp >= 1:
                
                return p2PartyRandomSwitch(c)
                    
            elif c.p2.pp1.hp >= 1:
                    
                c.p2.switchToParty1()
                p2FaintedChoice(c)
                print('\n' + "--Your opponent sent out " + str(c.p2.ap.n) + "!")
                print(c)
                return True
            
            elif c.p2.pp2.hp >= 1:

                c.p2.switchToParty2()
                
                print('\n' + "--Your opponent sent out " + str(c.p2.ap.n) + "!")
                print(c)
                return True
        else:
                           
            return True

        
def PokeStats(filename):
    """Opens the file containing all the stats and returns a list of list with all the stats."""
    
    grid = [] # make the empty list
    file = open(filename, 'r')
    
    file.readline() # read the header and throw away
    
    for line in file:
        
        if line[-1] == '\n':
            line = line[:-1]        # removes the '\n' from the end of each line 
            
        line = line.split(',')      # splits the line up into list dividing by ','
        grid.append(line)           # add the pokemon and its stats list as another element of the list 
        
    file.close()
    return(grid)


def effectiveness(pokemonType, moveType):
    ''' returns mulitplier for damage based on type effectiveness'''
    
    d = {'Normal': 0, 'Fire': 1, 'Water': 2, 'Grass': 3, 'Electric': 4, 'Ice': 5, \
         'Fighting': 6, 'Poison': 7, 'Ground': 8, 'Flying': 9, 'Psychic': 10, 'Bug': 11, \
         'Rock': 12, 'Ghost': 13, 'Dragon': 14, 'Dark': 15, 'Steel': 16, 'Fairy': 17}
    
    matrix = [[1,1,1,1,1,1,1,1,1,1,1,1,0.5,0,1,1,0.5,1],
              [0,0.5,0.5,2,1,2,1,1,1,1,1,2,0.5,1,0.5,1,2,1],
              [1,2,0.5,0.5,1,1,1,1,2,1,1,1,2,1,0.5,1,1,1],
              [1,0.5,2,0.5,1,1,1,0.5,2,0.5,1,0.5,2,1,0.5,1,0.5,1],
              [1,1,2,0.5,0.5,1,1,1,0,2,1,1,1,1,0.5,1,1,1],
              [1,0.5,0.5,2,1,0.5,1,1,2,2,1,1,1,1,2,1,0.5,1],
              [2,1,1,1,1,2,1,0.5,1,0.5,0.5,0.5,2,0,1,2,2,0.5],
              [1,1,1,2,1,1,1,0.5,0.5,1,1,1,0.5,0.5,1,1,0,2],
              [1,2,1,0.5,2,1,1,2,1,0,1,0.5,2,1,1,1,2,1],
              [1,1,1,2,0.5,1,2,1,1,1,1,2,0.5,1,1,1,0.5,1],
              [1,1,1,1,1,1,2,2,1,1,0.5,1,1,1,1,0,0.5,1],
              [1,0.5,1,2,1,1,0.5,0.5,1,0.5,2,1,1,0.5,1,2,0.5,0.5],
              [1,2,1,1,1,2,0.5,1,0.5,2,1,2,1,1,1,1,0.5,1],
              [0,1,1,1,1,1,1,1,1,1,2,1,1,2,1,0.5,0.5,1],
              [1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,0.5,0],
              [1,1,1,1,1,1,0.5,1,1,1,2,1,1,2,1,0.5,0.5,0.5],
              [1,0.5,0.5,1,1,2,1,1,1,1,1,1,2,1,1,1,0.5,2],
              [1,0.5,1,1,1,1,2,0.5,1,1,1,1,1,1,2,2,0.5,1]]
    
    moveType = d[moveType]
    pokemonType = d[pokemonType]
        
    m = matrix[moveType][pokemonType]
 
    return m 


def countNumTypes(listOfTypes):
    
    if len(listOfTypes) == 0:
        return 0
    if listOfTypes[0] == 'None':
        return 0 + countNumTypes(listOfTypes[1:])
    else:
        return 1 + countNumTypes(listOfTypes[1:])

    
def getMovePSDictionary(move):
    
    d = {'Physical': ['Aerial Ace', 'Bite', 'Brick Break', 'Bug Bite', 'Close Combat', 'Dragon Claw', 'Dragon Pulse', \
                      'Earthquake', 'Fire Fang', 'Ice Punch', 'Karate Chop', 'Metal Claw', 'Nuzzle', \
                      'Quick Attack', 'Razor Leaf', 'Scratch', 'Seed Bomb', 'Slash', 'Spark', 'Stone Edge', \
                      'Tackle', 'Take Down', 'Thrash', 'Vine Whip'], \
        'Special': ['Aura Sphere', 'Confusion', 'Dark Pulse', 'Dragon Breath',  'Ember', 'Flamethrower', \
                    'Gust', 'Ice Beam', 'Thunderbolt', 'Thunder Shock', 'Water Gun', 'Water Pulse'], \
        'Other': ['Splash']}
    
    for i in d:
        if move in d[i]:
            return i

    
def getDamageDictionary():
    
    d = {0: ['Splash'], \
         20: ['Nuzzle'], \
         40: ['Acid', 'Brick Break', 'Ember', 'Gust', 'Quick Attack', 'Scratch', 'Tackle', 'Thunder Shock', 'Vine Whip', 'Water Gun'], \
         50: ['Confusion', 'Dragon Claw', 'Ice Punch', 'Karate Chop', 'Metal Claw'], \
         55: ['Aerial Ace', 'Razor Leaf'], \
         60: ['Bite', 'Bug Bite', 'Dragon Breath', 'Water Pulse'], \
         65: ['Fire Fang', 'Spark'], \
         70: ['Slash'], \
         80: ['Aura Sphere', 'Dark Pulse', 'Thunderbolt', 'Seed Bomb'],\
         85:['Dragon Pulse'], \
         90: ['Flamethrower', 'Ice Beam', 'Take Down'], \
         100: ['Earthquake', 'Stone Edge'], \
         120: ['Close Combat', 'Thrash']} 
    
    return d


def getMoveDictionary():
    ''' Move dictionary for types'''
    
    d = {'Bug': ['Bug Bite'], \
         'Dark': ['Bite', 'Dark Pulse'], \
         'Fighting': ['Aura Sphere', 'Brick Break', 'Close Combat','Karate Chop'],\
         'Fire': ['Ember', 'Fire Fang', 'Flamethrower'], \
         'Grass': ['Razor Leaf', 'Seed Bomb', 'Vine Whip'], \
         'Ground': ['Earthquake'], \
         'Water': ['Aqua Jet', 'Splash', 'Water Gun', 'Water Pulse'], \
         'Normal': ['Tackle', 'Take Down', 'Thrash', 'Scratch', 'Slash', 'Quick Attack'], \
         'Poison': ['Acid'], \
         'Flying': ['Aerial Ace', 'Gust'], \
         'Rock': ['Stone Edge'], \
         'Electric': ['Thunderbolt', 'Thunder Shock', 'Spark'], \
         'Dragon': ['Dragon Breath', 'Dragon Claw', 'Dragon Pulse'], \
         'Ice': ['Ice Beam', 'Ice Punch'], \
         'Steel': ['Metal Claw'], \
         'Psychic': ['Confusion']}
    
    return d


#                c.p2action(c.p2m)   # inputs the rival's active Pokemon's move into the attack method in the Battle class
#                c.p1.ap.hp -= 2
##                p1active.hp = c.p1hp  # player's active pokemon health is copied into that Pokemon's class
#                print('\n--Your rival used ' + c.p2.ap.m + '!')
#                
#                if c.p1.ap.hp < 1:   # if player 1's active pokemon's hp is less than 1, or fainted
#                            
#                            
#                    if c.p1.pp1.hp < 1 and c.p1.pp2.hp < 1:   # if both of the player's party pokemon is fainted, then rival wins
#                        print('\n' + 'You lost!')
#                        break
#                    
#                    elif c.p1.pp1.hp >= 1:   # if the player's first party Pokemon fainted, send out the second Pokemon
#                                
#                        # swapping active pokemon slot with party pokemon slot
##                        buffer = p1active
##                        p1active = p1party1
##                        p1party1 = buffer
#                        c.p1.switchToParty1()
#                          # initializes Battle once active pokemon is updated
#                        print('\n' + '--Your Pokemon fainted, you switched Pokemon!' + '\n')
#                        print(c)
#                        
#                    elif c.p1.pp2.hp >= 1:   # if the player's second party Pokemon fainted, send out the first Pokemon
#                                
#                        # swapping active pokemon slot with party pokemon slot
##                        buffer = p1active
##                        p1active = p1party2
##                        p1party2 = buffer
#                        c.p1.switchToParty2
#                          # initializes Battle once active pokemon is updated
#                        print('\n' + '--Your Pokemon fainted, you switched Pokemon!' + '\n')
#                        print(c)
#                        
#                else:
#                    # if player's active pokemon does not faint, their move goes through
##                    c.p1action(c.p1m)  
##                    p2active.hp = c.p2hp  # MAYBE WRITE A HELPER FUNCTION HERE THAT COPIES THE ACTIVE POKEMON'S STATE/STATS ONTO ITS POKEMON CLASS  
#                    c.p2.ap.hp -= 3
#                    print('\n--You used ' + c.p1.ap.m + '!')
#                    
#                    if c.p2.ap.hp < 1: # when rival's active pokemon faints, similar behavior to player above
#                        
#                        if c.p2.pp1.hp < 1 and c.p2.pp2.hp < 1:
#                            print('\n' + 'You Won!')
#                            break
#                        
#                        elif c.p2.pp1.hp >= 1:
#                                
##                            buffer = p2active
##                            p2active = p2party1
##                            p2party1 = buffer
#                            c.p2.switchToParty1()
#                            
#                            print('\n' + "--Opponent's Pokemon fainted, they switched Pokemon!" + '\n')
#                            print(c)
#                                
#                        elif c.p2.pp2.hp >= 1:
##                            buffer = p2active
##                            p2active = p2party2
##                            p2party2 = buffer
#                            c.p2.switchToParty2
#                            
#                            print('\n' + "--Opponent's Pokemon fainted, they switched Pokemon!" + '\n')
#                            print(c)
#                    else:
#                        print(c)            
#def pokemonInteraction(c, player1, player2):
#    
#    buffer = ''
#    
#    if c.p2hp < 1:   # if player 2's active pokemon's hp is less than 1, or fainted
#                
#                
#        if player2.pp1.hp < 1 and player2.pp2.hp < 1:   # if both of the rival's party pokemon is fainted, then player 1 wins
#            print('\n' + 'You won!')
#            return 'break'
#        
#        elif player2.pp1.hp >= 1:   # if the rival's first party Pokemon fainted, send out the second Pokemon
#            
#            # swapping active pokemon slot with party pokemon slot
#            buffer = p2active
#            p2active = p2party1
#            p2party1 = buffer
#            c = Battle(p1active, p2active)  # initializes Battle once active pokemon is updated
#            print('\n' + '--Your opponent switched Pokemon!' + '\n')
#            print(c)
#            
#        elif p2party2.hp >= 1:   # if the rival's second party Pokemon fainted, send out the first Pokemon
#            
#            # swapping active pokemon slot with party pokemon slot
#            buffer = p2active
#            p2active = p2party2
#            p2party2 = buffer
#            c = Battle(p1active, p2active)  # initializes Battle once active pokemon is updated
#            print('\n' + '--Your opponent switched Pokemon!' + '\n')
#            print(c)
#        
#    else:
#        # if player 2's pokemon does not faint, their move goes through
#        c.p2action(c.p2m)  
#        p1active.hp = c.p1hp  # MAYBE WRITE A HELPER FUNCTION HERE THAT COPIES THE ACTIVE POKEMON'S STATE/STATS ONTO ITS POKEMON CLASS  
#        print('\n' + '--You used ' + c.p1m + '!\n\n--Your rival used ' + c.p2m + '!')
#        print(c)    

#def p2movefirst(c, p1active, p1party1, p1party2, p2active, p2party1, p2party2):
#    
#    c.p2action(c.p2m)   # inputs the rival's active Pokemon's move into the attack method in the Battle class
#    p1active.hp = c.p1hp  # player's active pokemon health is copied into that Pokemon's class
#            
#    if c.p1hp < 1:   # if player 1's active pokemon's hp is less than 1, or fainted
#                
#                
#        if p1party1.hp < 1 and p1party2.hp < 1:   # if both of the player's party pokemon is fainted, then rival wins
#            print('\n' + 'You lost!')
#            break
#        
#        elif p1party1.hp >= 1:   # if the player's first party Pokemon fainted, send out the second Pokemon
#                    
#            # swapping active pokemon slot with party pokemon slot
#            buffer = p1active
#            p1active = p1party1
#            p1party1 = buffer
#            c = Battle(p1active, p2active)  # initializes Battle once active pokemon is updated
#            print('\n' + '--Your Pokemon fainted, you switched Pokemon!' + '\n')
#            rprint(c)
#            
#        elif p1party2.hp >= 1:   # if the player's second party Pokemon fainted, send out the first Pokemon
#                    
#            # swapping active pokemon slot with party pokemon slot
#            buffer = p1active
#            p1active = p1party2
#            p1party2 = buffer
#            c = Battle(p1active, p2active)  # initializes Battle once active pokemon is updated
#            print('\n' + '--Your Pokemon fainted, you switched Pokemon!' + '\n')
#            print(c)
#            
#        else:
#            # if player's active pokemon does not faint, their move goes through
#            c.p1action(c.p1m)  
#            p2active.hp = c.p2hp  # MAYBE WRITE A HELPER FUNCTION HERE THAT COPIES THE ACTIVE POKEMON'S STATE/STATS ONTO ITS POKEMON CLASS  
#            print('\n' + '--You used ' + c.p1m + '!\n\n--Your rival used ' + c.p2m + '!')
#            rreturn(c)
#        
#        if c.p2hp < 1: # when rival's active pokemon faints, similar behavior to player above
#            
#            if p2party1.hp < 1 and p2party2.hp < 1:
#                print('\n' + 'You lost!')
#                break
#            
#            elif p2party1.hp >= 1:
#                    
#                buffer = p2active
#                p2active = p2party1
#                p2party1 = buffer
#                c = Battle(p1active, p2active)
#                print('\n' + "--Opponent's Pokemon fainted, you switched Pokemon!" + '\n')
#                print(c)
#                    
#            elif p2party2.hp >= 1:
#                buffer = p2active
#                p2active = p2party2
#                p2party2 = buffer
#                c = Battle(p1active, p2active)
#                print('\n' + "--Opponent's Pokemon fainted, you switched Pokemon!" + '\n')
#                print(c) 
    
    
        
#        if choice == 'r':
#            print('You rolled a ' + str(roll_dice()) + '.')
    
#def roll_dice():   # roll dice function
#    
#    x = random.randint(1, 6)
#    return x

#def partyRoster1():
#    
#    Charmander(20, 5, 11, 10, ['Fire'])
#    Pidgey(20, 5, 10, 10, ['Normal', 'Flying']) 
#    Pikachu(20, 5, 12, 10, ['Electric'])
#    
#    
#def partyRoster2():
#    
#    Squirtle(20, 5, 11, 13, ['Water'])
#    Eevee(22, 5, 12, 11, ['Normal']) 
#    Vulpix(20, 5, 10, 10, ['Fire'])

        
#    def attack(self, a):
#if __name__ == "__main__":
#    
#    print(Battle(10, 5, 15, 5))
    
        
main()
