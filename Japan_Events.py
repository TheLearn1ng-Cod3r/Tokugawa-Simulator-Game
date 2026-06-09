import random,subprocess,platform,time
from Japan_Classes import Player
from Japan_Utility import clear
import keyboard

"""Event definitions and stat modification for the game."""
DEFAULT_STAT_MIN = 0
DEFAULT_STAT_MAX = 100


def value_limits(maximum: int, minimum: int, value: int) -> tuple[int, bool]:
    limit_reached = value > maximum or value < minimum
    return min(maximum, max(minimum, value)), limit_reached


def modify_stats(entity: Player, health_mod: float = 0, honour_mod: int = 0, money_mod: int = 0) -> tuple[Player, dict]:
    health_value, health_limited = value_limits(DEFAULT_STAT_MAX, DEFAULT_STAT_MIN, int(entity.health + health_mod))
    honour_value, honour_limited = value_limits(DEFAULT_STAT_MAX, DEFAULT_STAT_MIN, int(entity.honour + honour_mod))
    money_value, money_limited = value_limits(DEFAULT_STAT_MAX, DEFAULT_STAT_MIN, int(entity.money + money_mod))

    entity.health = health_value
    entity.honour = honour_value
    entity.money = money_value

    limits = {"health": health_limited, "honour": honour_limited, "money": money_limited}
    return entity, limits


def can_afford_money(entity: Player, money_mod: int = 0) -> bool:
    """Return True if the money modification does not drop money below zero."""
    return int(entity.money + money_mod) >= DEFAULT_STAT_MIN
# 

class Events:
    @staticmethod
    def earthquake(entity: Player) -> None:
        print('Earthquakes ravage through your town, your walls are crumbling, and the tea cup is cracked, do you:')
        choice = input("""
        a) Hide under a table and hope for the best
        b) Go outside and help the others
                       """).lower()
        if "a" in choice:
            chance = random.random() >= 0.5
            if chance:
                if can_afford_money(entity, money_mod=-10):
                    print("You barely survive the falling debris, but your house is in ruins (-10 Money)")
                    modify_stats(entity, money_mod=-10)
                else:
                    print("You don't have enough money to lose, so you stay sheltered and avoid the worst of the debris.")
            else:
                if can_afford_money(entity, money_mod=-10):
                    print("Despite your best efforts, a rock crashes right into your shoulder, drawing blood (-10 Health, -10 Money)")
                    modify_stats(entity, health_mod=-10, money_mod=-10)
                else:
                    print("You don't have enough money to pay for the damage, so you stay put and survive the earthquake more carefully.")
        else:
            print("You save an elder from a falling tree, and the town celebrates you, but you get hurt in the process (+10 Honour, -15 Health)")
            modify_stats(entity, honour_mod=10, health_mod=-15)
        print(entity)


    @staticmethod
    def rice(entity: Player) -> None:
        print("Whilst eating your rice, you notice you feel full, do you:")
        choice = input("""
    a) Throw out the remaining rice
    b) Convert the remaining rice to Onigiri for later
        """).lower()
        if "a" in choice:
            print("As you dump the rice, a farmer watches you, and shakes his head in disappointment (-5 Honour)")
            modify_stats(entity, honour_mod=-5)
        else:
            print("You make some Onigiri, but you suffer from over-eating (-5 Health, +3 Honour)")
            modify_stats(entity, health_mod=-5, honour_mod=3)
        print(entity)
        entity.score += 10
        entity.events += 1

    @staticmethod
    def daimyo_tax(entity: Player) -> None:
        print("A representative of your Daimyo knocks on your door, he says he's here to collect your taxes, do you:")
        choice = input("""
    a) Pay the taxes
    b) Hide your harvest and pray they don't find it
    c)Refuse and face the consequences
        """).lower()
        if "a" in choice:
            if can_afford_money(entity, money_mod=-20):
                print("The daimyo is pleased, but the taxes are high (-20 Money, +5 Honour)")
                modify_stats(entity, money_mod=-20, honour_mod=5)
            else:
                print("You don't have enough money to pay the taxes, so the daimyo leaves unsatisfied.")
        elif "b" in choice:
            chance = random.random() >= 0.5
            if chance:
                print("The representative searches your house, but walks right past the grain! You get away with it (+10 Money)")
                modify_stats(entity, money_mod=10)
            else:
                if can_afford_money(entity, money_mod=-25):
                    print("The representative searches your house, and finds your poorly hidden grain. You face punishment and disgrace, and get whipped (-25 Money, -10 Honour, -10 Health)")
                    modify_stats(entity, money_mod=-25, honour_mod=-10, health_mod=-10)
                else:
                    print("You don't have enough money to pay the fine; somehow you manage to escape with only a warning.")
        else:
            print("The daimyo representative is furious, and you get a public whipping (-10 Health, -20 Honour)")
            modify_stats(entity, health_mod=-10, honour_mod=-20)
        print(entity)
        entity.score += 10
        entity.events += 1

    @staticmethod
    def tsunami(entity: Player) -> None:
        print("You hear a crash. As people flee, you see a giant wave coming from the west shore, do you:")
        choice = input("""
    a) Run for your life! 
    b) Try to save as many people as you can
        """).lower()
        if "a" in choice:
            chance = random.random() >= 0.5
            if chance:
                print("You manage to find a high place, you survived the tsunami, and your house was above the tsunami stone, recieving no damage")
            else:
                print("You start running, but get caught in the debris. You slosh through water, facing severe damage (-17 Health)")
                modify_stats(entity, health_mod=-17)
        else:
            chance = random.random() >= 0.75
            if chance:
                print("Despite your efforts, you fail to save anyone and sustain injuries for nothing (+20 Honour, -20 Health)")
                modify_stats(entity, honour_mod=20, health_mod=-20)
            else:
                print("The water is deafening, but you hear a scream and bring up a child amidst the chaos. You survive, but not without harm (-7 Health, +10 Honour)")
                modify_stats(entity, health_mod=-7, honour_mod=10)
        print(entity)
        entity.score += 10
        entity.events += 1

  # Special Events are events that have 50% of the chance to occur than normal (I think that's how math works ?). I'm planning to make these events give health, but still have a risk.
    @staticmethod
    def dutch_loot(entity: Player) -> None:
        print("SPECIAL EVENT: A dutch ship arrives at your port, he offers a mystery crate, do you:")
        choice = input("""
    a) Accept the crate (-5 Money))
    b) Refuse the crate
""").lower()
        if "a" in choice:
            if can_afford_money(entity, money_mod=-5):
                print("You buy the crate (-5 Money)")
                modify_stats(entity, money_mod=-5)
                clear()
            else:
                print("You don't have enough money to buy the crate, so you refuse the offer.")
                return
            # Roll system to build suspense 
            for i in range(3):
                print(f"Opening crate{'.'*i}...")
                time.sleep(1)
            for i in range(random.randint(6, 12)):
                clear()
                print(random.choice(["-Common-", "-Uncommon-", "-Rare-", "-Legendary-"]))
                time.sleep(0.4)
                clear()
                time.sleep(0.1)
            clear()

            chance = random.random()
            if chance >= 0.88:
                print("You receive the crate, and find a rare artifact worth a fortune! (+30 Money)")
                modify_stats(entity, money_mod=30)

            elif chance >= 0.45:
                print("You receive the crate, and find a vial of western medicine! (+15 Health)")
                modify_stats(entity, health_mod=15)

            elif chance >= 0.15:
                print("You receive the crate, and find a pouch of gold coins! (+10 Money)")
                modify_stats(entity, money_mod=10)

            else:
                print("You receive the crate, but find nothing of value. (0 stat change)")
            print(entity)

        else:
            print("You refuse the crate and the dutch trader carries on...(No stat change)")
        entity.score += 20
        entity.events += 1



    @staticmethod
    def missionaries(entity: Player) -> None:
        print("SPECIAL EVENT: A group of missionaries arrive at your door,wearing hooded cloaks and wide western smiles.They offer to spread their 'Christianity', do you:")
        choice = input("""
        a) Report them
        b) Hear them out    
        """).lower()
        if "a" in choice:
            print(" You report missionaries and they're burned at the stake that same evening (+10 Honour)")
            modify_stats(entity, honour_mod=10)

        else:
            chance = random.random() >= 0.5

            if chance:
                print("You listen to the missionaries, wary of authorities, but the communication stays secret. You feel a weight lifted off your shoulders (+10 Health, -5 Honour)")
                modify_stats(entity, honour_mod=-5, health_mod=10)

            else:
                print("You're in the middle of listening, when the Shogunate breaks through your door. You're punished severely and face disgrace(-25 Health, -15 Honour)")
                modify_stats(entity, health_mod=-25, honour_mod=-15)

        print(entity)
        entity.score += 20
        entity.events += 1

    @staticmethod
    def Ainu(entity: Player) -> None:
        rare_items = {
            "Ainu Artifact": {"money": 15},
            "Santan Silk": {"money": 20},
        }
        uncommon_items = {
            "Attush": {"health": 5, "honour": 5},
            "Tamasai": {"honour": 10},
        }
        common_items = {
            "Traditional Medicine": {"health": 15},
            "Furs": {"money": 5, "health": 5},
            "Food": {"health": 10},
        }
        items : dict = {**common_items, **uncommon_items, **rare_items}
        options : list= random.sample(list(items.keys()), 3)

        print("A group of Ainu traders come by your village. They offer you a vast selection of goods, each with unique benefits, do you:")
        choice = input(f'''
    a) Buy {options[0]}(-10 Money)
    b) Buy {options[1]}(-10 Money)
    c) Buy {options[2]}(-10 Money)
    d) Decline their offer
        ''').lower()
        choice_map = {
            "a": options[0],
            "b": options[1],
            "c": options[2]
        }
        if choice in choice_map:
            item = choice_map[choice]

            if not can_afford_money(entity, money_mod=-10):
                print("You don't have enough money to buy the item, so you decline the offer.")
                return
            print(f"You buy {item}(-10 Money)")
            print(f"From {item} you receive: {", ".join([f'+{v} {k.capitalize()}' for k, v in {**common_items, **uncommon_items, **rare_items}[item].items()])}")
            modify_stats(entity,
                         money_mod=items[item].get("money", 0) - 10,
                         health_mod=items[item].get("health", 0),
                         honour_mod=items[item].get("honour", 0))
            
        else:
            print(" You decline the Ainu's offer and walk away (No stat change)") 

        print(entity)
        entity.score += 10
        entity.events += 1

    @staticmethod
    def lost_money(entity: Player) -> None:
        print(" As you're walking down the street, you notice some coins on the street. There is no one in sight, and it looks untouched. Do you:")
        choice = input("""
    a) Steal the coins
    b) Donate them to the temple
    c) Leave the alone
        """).lower()
        if "a" in choice:
            print("You steal the coins, and walk past a beggar on the street. He eyes you with dissapointment (-10 Honour, + 10 Money)")
            modify_stats(entity, honour_mod=-10, money_mod=10)

        elif "b" in choice:
            print("You donate your coins, and the priest provides you with a nice meal (+10 Honour, + 5 Health)")
            modify_stats(entity, honour_mod=10, health_mod=5)

        else:
            print("You leave the coins alone, and waltz away (No stat change)")

        print(entity)
        entity.score += 10
        entity.events += 1

class Samurai_Events:
    @staticmethod
    def Duel(entity: Player) -> None:
        print("CLASS EVENT: A samurai walks up to you, and chalenges you to a duel. Do you:")
        choice = input("""
    a) Accept the duel
    b) Mock their master
    c) Descalate
        """).lower()
        if "a" in choice:
            chance = random.random() >= 0.65

            if chance:
                print("The fight is difficult, and you sustain some injuries, but you come out victorious! (+15 Honour, -5 Health)")
                modify_stats(entity, honour_mod=15, health_mod=-5)

            else:
                print("You stumble and flail about. Your sword is knocked from your hand, and you lose miserably (-25 Honour, -20 Health)")
                modify_stats(entity, honour_mod=-25, health_mod=-20)

        elif "b" in choice:
            print(" You mock their master, and the samurai cuts you in blind rage. He walks away in shame at his outburst, but you remain injured (-10 Honour, -15 Health)")
            modify_stats(entity, honour_mod=-10, health_mod=-15)

        else:
            print("You descalate the situation, and gain new found respect from the samurai. (+5 Honour)")
            modify_stats(entity, honour_mod=5)

        print(entity)
        entity.score += 10
        entity.events += 1

    @staticmethod
    def Alternate_Attendance(entity: Player) -> None:
        print("CLASS EVENT: Your Daiymo is going to Edo for their alternate attendace, and offer you a spot on their procession, do you:")
        choice = input("""
    a) Accept the offer
    b) Respectfully decline
        """).lower()
        if "a" in choice:
            print("You attend the procession, and gain respect from the daimyo and senior samurai. However, the long walk is tiring (-3 Health, +15 Honour)")
            modify_stats(entity, honour_mod=15, health_mod=-3)

        else:
            print("You decline the offer with a bow, and the daimyo respects your decision. (+5 Honour)")
            modify_stats(entity, honour_mod=5)

        print(entity)
        entity.score += 15
        entity.events += 1


    @staticmethod
    def Ronin_Ambush(entity: Player) -> None:
        print("CLASS EVENT: On your way home, a group of 5 masked figures surround you. They reveal themselves as Ronin, here to slay your master, do you:")
        choice = input("""
    a) Fight the Ronin 
    b) Run to your master and warm him                 
                       """).lower()
        if "a" in choice:

            for i in range (6):
                chance = random.random() >= 0.3

                if chance:
                    print("You defeat one Ronin, and continue fighting!(+10 Honour, -1 Health, +5 Money)")
                    modify_stats(entity, honour_mod=10, health_mod=-1, money_mod=5)

                else:
                    print("The Ronin cut you down, and you lose the fight, leaving the Ronins to your master. Thankfully, the other samurai finish what you've started.(-20 Honour, -15 Health)")
                    modify_stats(entity, honour_mod=-20, health_mod=-15)
                    break
                
                clear()
        else:
            print("You break past the Ronins to your master. Where the other samurai fend off the ronin (No stat change)")
        print(entity)
        entity.score += 15
        entity.events += 1

class Peasant_Events:
    @staticmethod
    def Starvation(entity: Player) -> None:
        print("CLASS EVENT: A famine hits your village, and food is scarce. Do you:")
        choice = input("""
    a) Steal food from your neighbour
    b) Group together and ration food with your village
            """).lower()
        if "a" in choice:
            chance = random.random() >= 0.333
            if chance:
                print( "You break into your neighbour's house at midnight, and grab a few pounds of rice. Your neighbour wakes up in the morning with no clue and a hungry family (-3 Honour, +10 Health)")
                modify_stats(entity, honour_mod=-3, health_mod=10)
            else:
                print(" You walk into your neighbour's house in pure daylight, get caught, and your entire goningumi faces the consequences (-15 Honour, -10 Health)")
                modify_stats(entity, honour_mod=-15, health_mod=-10)
        else:
            print(" The goningumi groups together to ration, and you all scrape by (+5 Honour, -5 Health)")
            modify_stats(entity, honour_mod=5, health_mod=-5)
        print(entity)
        entity.score += 10
        entity.events += 1


    @staticmethod
    def Goningumi(entity: Player) -> None:
        print("CLASS EVENT: A member of your goningumi has been accused of theft. The shogunate are coming to investigate them. Do you:")
        choice = input(""" PLACEHOLDER 
    a) Testify against the member
    b) Defend them 
                       """).lower()
        if "a" in choice:
            chance = random.random() >= 0.5
            if chance:
                print("You testify against the member, and they are found guilty. The shogunate punishes your neighbour severly (-5 Honour)")
                modify_stats(entity, honour_mod=-5)
            else:
                print("You testify against the member, but they are found innocent. The shogunate punishes you all for false accusations, and the goningumi considers you a rat (-15 Honour, -15 Health)")
                modify_stats(entity, honour_mod=-15, health_mod=-15)
        else:
            chance = random.random() >= 0.5
            if chance:
                print("You defend the member, and they are cleared. The member pays you for your help, and  (+10 Honour, +10 Money)")
                modify_stats(entity, honour_mod=10, money_mod=10)
            else:
                print("You defend the member, but they are found guilty regardless. The shogunate punishes you all, and the village places you both under Murahachibu (-20 Honour, -20 Health)")
                modify_stats(entity, honour_mod=-20, health_mod=-20)
        print(entity)
        entity.score += 10
        entity.events += 1
    

    def Farming_Crops(entity: Player) -> None:
        print("CLASS EVENT: You're farming crops when you reach a tough stalk Do you:")
        choice = input("""
    a) Pull it out
    b) Get a friend to help
    c) Move on to the next
        """).lower()
        if "a" in choice:
            clear()
            for i in range(3):
                print(f"Pulling{'.'*i}...")
                time.sleep(1)
            clear()
            print("Press Space to Pull!")
            time.sleep(2)
            score = 0
            while score < 100:
                clear()
                if keyboard.is_pressed("space"):
                    score += random.randint(1, 5)/ random.randint(1, 3)
                    print(f"Score: {score:.2f}/100")
                    while keyboard.is_pressed("space"):
                        time.sleep(0.01) 
                    time.sleep(0.1)
                else:
                    print(f"Score: {score:.2f}/100")
                    print("Keep pulling!")
            clear()
            print("You pull the stalk out, and gain a good harvest! You enjoy your hard earned rice (+10 Money, + 5 Health)")
            modify_stats(entity, money_mod=10, health_mod=5)
        elif "b" in choice:
            clear()
            for i in range(3):
                print(f"Pulling with a friend{'.'*i}...")
                time.sleep(1)
            clear()
            print("Press Space to Pull!")
            time.sleep(2)
            score = 0
            while score < 50:
                clear()
                if keyboard.is_pressed("space"):
                    score += random.randint(1, 5)/ random.randint(1, 3)
                    print(f"Score: {score:.2f}/50")
                    while keyboard.is_pressed("space"):
                        time.sleep(0.01) 
                    time.sleep(0.1)
                else:
                    print(f"Score: {score:.2f}/50")
                    print("Keep pulling!")
            clear()
            print("You pull the stalk out with the help of your friend, and gain a good harvest! You enjoy your hard earned rice, giving half to your friend (+5 Money, + 3 Health)")
            modify_stats(entity, money_mod=5, health_mod=3)
        else:
            print("You move on to the next stalk, and miss out on a good harvest. You starve from the lack of food(-5 Health)")
            modify_stats(entity, health_mod=-5 )
        print(entity)
        entity.score += 10
        entity.events += 1


class Merchant_Events:

    @staticmethod
    def Over_Charge(entity: Player) -> None:
        print("CLASS EVENT: A customer comes to you, and asks for one of your cheaper items. He's unsuspecting, with a child at his knees, do you:")
        choice = input("""
    a) Charge him full price
    b) Overcharge him
    c) Give him a discount
                       """).lower()
        if "a" in choice:
            print("You charge him normal price, and say hi to the child. After a nice conversation and a promise of return, you say goodbye to your customer (+10 Money)")
            modify_stats(entity, money_mod=10)
        elif "b" in choice:
            print(" You charge him more than 20% the real price, and make a huge profit. You can hear his stressed chattering as he leaves, and you get shunned by your coworker (+13 Money, -7 Honour)")
            modify_stats(entity, money_mod=13,honour_mod=-7)
        else:
            print(r"You take a look at the customer, and give him a 20% discount. He lets out a sigh of relief, explaining his struggles with the Daimyo's taxes.""(+8 Money, +7 Honour)")
            modify_stats(entity,money_mod=8,honour_mod=7)
        print(entity)
        entity.events += 1
        entity.score += 10


    @staticmethod
    def Samurai_Debt(entity: Player) -> None:
        print(" CLASS EVENT: A samurai bursts through your door, demanding you release him of his taxes. He slams his hands on the desk, sword gleaming in his sheath, do you:")
        choice = input("""
    a) Refuse
    b) Release his debt
                       """).lower()
        if "a" in choice:
            print(" You stand your ground, insisting he pays. He stands up, seemingly ready to attack. But instead he deflates and mopes out the door, change on the desk (+15 Money)")
            modify_stats(entity,money_mod=15)
        else:
             print(" You release him of his debt. He smiles smugly and spits at you, before swaggering out. You feel dishonoured(-10 Money, -5 Honour)")
             modify_stats(entity, money_mod=-10,honour_mod=-5)
        print(entity)
        entity.events += 1
        entity.score += 10
    

    @staticmethod
    def a():
        ...
        

# Turns the Events into a list
Common_Events : list[callable]= [Events.earthquake, Events.rice, Events.daimyo_tax, Events.tsunami, Events.Ainu, Events.lost_money]
Rare_Events : list[callable]= [Events.dutch_loot, Events.missionaries]
Role_Events : dict[str, list[callable]] = {
    "Samurai": [Samurai_Events.Duel, Samurai_Events.Alternate_Attendance, Samurai_Events.Ronin_Ambush],
    "Peasant": [Peasant_Events.Starvation, Peasant_Events.Goningumi, Peasant_Events.Farming_Crops],
    "Merchant" : [Merchant_Events.Over_Charge, Merchant_Events.Samurai_Debt]
}
Event_List : list[callable] = [ i for i in Common_Events * 2] + [i for i in Rare_Events]
# NOTE The following code if for event testing, and shouldn't be touched or taken as part of the project
if __name__ == "__main__":
    player = Player(name="Test Player")
    print(player) 
    for _ in Event_List:
        print(_.__name__)
    input("Press anything to continue...")
    clear()
    while player.health > 0 and player.honour > 0:
        Merchant_Events.Over_Charge(player)
# TODO: Add 2-4 more events(3), and seperate lists(COMPLETED). Also maybe make class specific events? Just 2-3 per class?(Samurai and Peasant Completed, still waiting on merchant,)

