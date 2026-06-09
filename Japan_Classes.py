import random

def name_generator() -> str:
# First name options if player doesn't choose one
    first_names = [
    "Hiro","Kenji","Akira","Taro","Ren","Daichi","Yuki","Haru","Sora","Takumi","Satoru","Roronoa","Yuri"
    ]
    # Last name options if player doesn't choose one
    last_names = [
    "Tanaka","Sato","Kobayashi","Yamamoto","Nakamura","Ito","Watanabe","Suzuki","Takahashi","Mori","Gojo","Zoro","Hanamichi"
    ]
    playername = random.choice(first_names) + " " + random.choice(last_names)
    return playername
playername = name_generator()

class Player: # Base Player class, all players have these stats, but they are modified by their class
    def __init__(self, name:str = playername, health : float = 50, honour : int = 50, money : int = 50):
        self.name = name if name else name_generator()
        self.health : float = health
        self.honour : int = honour
        self.money : int = money
        self.role : str = 'Player' # Default role, will be overridden by child classes
        self.score : int = 0
        self.events : int = 0
    def __str__(self) -> str:
        return f"""{self.name}({self.role})
Health: {self.health}
Honour: {self.honour}
Money: {self.money}"""


# More Honour for the Samurai, 20% chance of Ronin, effects TBD, but Samurai can die of Low Honour 
class Samurai(Player):
    def __init__(self, name:str = playername, health : float = 50, honour : int = 50, money : int = 50):
        super().__init__(name, health, honour, money)
        ronin_chance = [False,False,False,False,True]
        self.role : str = 'Ronin' if random.choice(ronin_chance) == True else 'Samurai'
        # +20% Honour & Health W Class 🔥🔥🔥, but -20% Money :( 
        self.honour = int(round(self.honour * 1.2))
        self.health = int(round(self.health * 1.2))
        self.money = int(round(self.money * 0.8))

#Peasant Class with basic stats, no buff
class Peasant(Player):
    def __init__(self, name:str = playername, health : float = 50, honour : int = 50, money : int = 50):
        super().__init__(name, health, honour, money)
        self.role : str = 'Peasant'
        # No buff, L Class 😂

#Merchant Class gains 20% more money        
class Merchant(Player):
    def __init__(self, name:str = playername, health : float = 50, honour : int = 50, money : int = 50):
        super().__init__(name, health, honour, money)
        self.role : str = 'Merchant'
        # +20% Money
        self.money = int(round(self.money * 1.2))

#Artisan has 10% less honour
class Artisan(Player):
    def __init__(self, name:str = playername, health : float = 50, honour : int = 50, money : int = 50):
        super().__init__(name, health, honour, money)
        self.role : str = 'Artisan'
        # -10% Honour
        self.honour = int(round(self.honour * 0.9))