import random, time
from Japan_Classes import Player, Samurai, Peasant, Merchant, Artisan, playername
from Japan_Events import Event_List, Role_Events, modify_stats
from Japan_Utility import clear

Role_Map = {1: Samurai, 2: Peasant, 3: Peasant, 4: Merchant, 5: Artisan}
    
clear()
def main() -> None:
    global Event_List
    player = Role_Map[random.randint(1, 5)](
        input('Enter your name or press enter to generate a random name: ').strip() or playername
    )
    clear()
    print(player)
    input("Press anything to continue...")
    clear()

    Event_List = Event_List + [i for i in Role_Events.get(player.role.capitalize(), [])]
    while (player.health > 0 and player.honour > 0) or (player.role == 'Samurai' and player.honour > 10):
        random.choice(Event_List)(player)
        input("Press anything to continue...")
        clear()
    if player.health <= 0:
        print("You succumb to your injuries, and draw your last breath...\n")
        print("GAME OVER")
    elif player.honour <= 0 or (player.role == 'Samurai' and player.honour <= 10):
        if player.role == 'Samurai':
            print("You've disgraced yourself, and you commit Seppuku to restore your honour...")
            print("GAME OVER")
        else: 
            print("You've lost all honour, and are shunned to a life of an outcast...")
            print("GAME OVER")
    print(f"Final Score: {player.score}")
    print(f"Total Events: {player.events}")


if __name__ == "__main__":
    main()




