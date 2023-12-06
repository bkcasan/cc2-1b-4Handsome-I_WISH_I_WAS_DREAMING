import os
import random
import time
import sys


class Player:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.inventory = []
        self.health = 100
        self.attack = 15
        self.speed = 10

    def apply_loot(self, loot):
        if loot.effect == "attack":
            self.attack += loot.power
        elif loot.effect == "speed":
            self.speed += loot.power

    def __str__(self):
        inventory_str = ', '.join(str(item) if isinstance(item, Item) else item for item in self.inventory)
        return f"{self.name} - Position: ({self.x}, {self.y}) - Health: {self.health} - Attack: {self.attack} - Speed: {self.speed} - Inventory: {inventory_str}"

class Enemy:
    def __init__(self, name, health, attack, speed):
        self.name = name
        self.health = health
        self.attack = attack
        self.speed = speed
    
    def drop_loot(self):
        loot_options = [
            Item("Attack Boost", "Increases attack power.", "attack", 5),
            Item("Speed Boost", "Increases speed.", "speed", 2)
        ]
        return random.choice(loot_options)

    def __str__(self):
        return f"{self.name} - Health: {self.health} - Attack: {self.attack} - Speed: {self.speed}"

class Item:

    def __init__(self, name, description, effect, power):
        self.name = name
        self.description = description
        self.effect = effect
        self.power = power

    def __str__(self):
        return f"{self.name}: {self.description}"

class CaveMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.map_data = [['.' for _ in range(width)] for _ in range(height)]
        self.items = []
        self.enemies = []
        self.enemies = []
        self.entrance_x = None
        self.entrance_y = None

    def add_wall(self, x, y):
        self.map_data[y][x] = '#'

    def generate_cave_walls(self, num_walls):
        for _ in range(num_walls):
            x = random.randint(1, self.width - 1)
            y = random.randint(1, self.height - 1)
            if self.map_data[y][x] not in ('#', 'D', 'm'):
                self.add_wall(x, y)

    def scatter_loot(self, num_loots):
        for _ in range(num_loots):
            x = random.randint(1, self.width - 2)
            y = random.randint(1, self.height - 2)
            if random.random() < 0.7:
                loot = Item("Attack Boost", "Increases attack power.", "attack", 5)  # Add the missing argument
                self.items.append((x, y, loot))
    def scatter_enemies(self, num_enemies):
        for _ in range(num_enemies):
            x, y = self.get_empty_position()
            self.enemies.append((x, y))

    def get_empty_position(self):
        while True:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if self.map_data[y][x] == '.':
                return x, y

    def set_entrance(self):
        while True:
            x, y = self.get_empty_position()
            if self.map_data[y][x] == '.':
                self.entrance_x = x
                self.entrance_y = y
                self.map_data[y][x] = 'D'
                break

    def set_artifact(self, x, y):
        self.map_data[y][x] = 'A'

    def draw(self, player):
        os.system("clear" if os.name == "posix" else "cls")

        for row in range(self.height):
            for col in range(self.width):
                if player.x == col and player.y == row:
                    print("P", end=" ")  # Player's position
                elif (col, row,) in self.items:
                    print("L", end=" ")  # Loot position
                elif (col, row,) in self.enemies:
                    print("m", end=" ")  # Enemy position
                else:
                    print(self.map_data[row][col], end=" ")
            print()
def start_menu():
    print_typewriter("=== Welcome to the Mysterious Cave ===\n")
    print("1. Start New Game")
    print("2. Quit")
    choice = input("Enter your choice: ")

    if choice == "1":
        main()
    elif choice == "2":
        print("Goodbye!")
        sys.exit()
    else:
        print("Invalid choice. Please enter 1 or 2.")
        start_menu()



def combat(player, enemy):
    print("\n----- Combat Menu -----")
    print(f"Player: {player.health} HP - Attack: {player.attack} - Speed: {player.speed}")
    print(f"{enemy.name}: {enemy.health} HP - Attack: {enemy.attack} - Speed: {enemy.speed}")
    print("-----------------------")

    while player.health > 0 and enemy.health > 0:
        print("\nPlayer's turn:")
        print("1. Attack")
        print("2. Run")
        action = input("Choose your action: ")

        if action == "1":
            player_attack_damage = random.randint(1, player.attack)
            enemy.health -= player_attack_damage
            print(f"You dealt {player_attack_damage} damage to {enemy.name}!")
        elif action == "2":
            run_success = random.random() < 0.5
            if run_success:
                print("You successfully escaped from the battle!")
                return
            else:
                print("Failed to escape! The enemy attacks.")


        if enemy.health <= 0:
            print(f"\nYou defeated {enemy.name}!")
            loot_drop = generate_loot()
            print(f"You obtained: {loot_drop}")
            apply_loot(player, loot_drop)
            player.health = min(100, player.health + 0.2 * player.health)
            print(f"You regained 20% health. Current health: {player.health}")
            return

        # Enemy's turn
        print("\nEnemy's turn:")
        enemy_attack_damage = random.randint(1, enemy.attack)
        player.health -= enemy_attack_damage
        print(f"{enemy.name} attacks! You take {enemy_attack_damage} damage.")

    # Combat ends
    if player.health <= 0:
        print("\nYou were defeated in battle. Game Over.")
        sys.exit()

def generate_loot():
    loot_options = ["Attack Boost", "Speed Boost"]
    return random.choice(loot_options)

def apply_loot(player, loot):
    if loot == "Attack Boost":
        player.attack += 5
        print(f"You gained an Attack Boost! Your attack is now {player.attack}.")
    elif loot == "Speed Boost":
        player.speed += 2
        print(f"You gained a Speed Boost! Your speed is now {player.speed}.")


def clear_screen():
    os.system("clear" if os.name == "posix" else "cls")

def display_encounter_message():
    clear_screen()
    print_typewriter("YOU HAVE ENCOUNTERED AN ENEMY !\n")

def move_player(player, direction, cave_map):
    new_x, new_y = player.x, player.y

    if direction == "W" and player.y > 0:
        new_y -= 1
    elif direction == "A" and player.x > 0:
        new_x -= 1
    elif direction == "S" and player.y < cave_map.height - 1:
        new_y += 1
    elif direction == "D" and player.x < cave_map.width - 1:
        new_x += 1

    if 0 <= new_x < cave_map.width and 0 <= new_y < cave_map.height:
        if (new_x, new_y) in cave_map.items:
            loot_index = cave_map.items.index((new_x, new_y))
            _, _, loot = cave_map.items[loot_index]
            player.inventory.append(loot)
            cave_map.items.pop(loot_index)
            if loot.effect == "attack":
                player.attack += 5

        if (new_x, new_y) in cave_map.enemies:
            enemy_index = cave_map.enemies.index((new_x, new_y))
            enemy_position = cave_map.enemies.pop(enemy_index)
            enemy = Enemy("Monster", 20, 10, 5) 
            display_encounter_message()
            combat(player, enemy)
            return 
        
        if cave_map.map_data[new_y][new_x] != '#':
            player.x, player.y = new_x, new_y

def print_typewriter(text, delay=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)

def handle_landmark(player, objectives, cave_map):
    if cave_map.map_data[player.y][player.x] == "D":
        if not objectives["Defeat All Enemies"]:
            print_typewriter("You are not yet eligible to enter the cave, defeat all enemies first\n")
            input("Press Enter to continue...")
            return

        print("You now approach the entrance of a dark cave. It emanates an eerie atmosphere.")
        print("Legend has it that the cave conceals the ancient artifact you seek.")
        input("Press Enter to enter the cave...\n")

        artifact_x, artifact_y = 8, 8
        cave_map.set_artifact(artifact_x, artifact_y)

        while True:
            cave_map.draw(player)

            print("\nControls: W=Up, A=Left, S=Down, D=Right, Q=Quit, I=Inventory")
            action = input("Enter your move: ").upper()

            if action == "Q":
                print("Goodbye!")
                sys.exit()

            elif action == "I":
                view_inventory(player)
                continue

            move_player(player, action, cave_map)

            if player.x == artifact_x and player.y == artifact_y:
                print("You found the ancient artifact!")
                objectives["Find the Artifact"] = True
                input("Press Enter to continue...")
                return

    if cave_map.map_data[player.y][player.x] == "D":
        if not objectives["Defeat All Enemies"]:
            print("You approach the entrance of a dark cave, but the path seems perilous.")
            print("You sense the presence of enemies. Defeat them before entering the cave.")
            input("Press Enter to continue...")
            return

        print("You approach the entrance of a dark cave. It emanates an eerie atmosphere.")
        print("Legend has it that the cave conceals the ancient artifact you seek.")
        input("Press Enter to enter the cave...\n")

        artifact_x, artifact_y = 8, 8
        cave_map.set_artifact(artifact_x, artifact_y)

        while True:
            cave_map.draw(player)

            print("\nControls: W=Up, A=Left, S=Down, D=Right, Q=Quit, I=Inventory")
            action = input("Enter your move: ").upper()

            if action == "Q":
                print("Goodbye!")
                sys.exit()

            elif action == "I":
                view_inventory(player)
                continue

            move_player(player, action, cave_map)

            if player.x == artifact_x and player.y == artifact_y:
                print("You found the ancient artifact!")
                objectives["Find the Artifact"] = True
                input("Press Enter to continue...")
                return

    if cave_map.map_data[player.y][player.x] == "D":
        print("You approach the entrance of a dark cave. It emanates an eerie atmosphere.")
        print("Legend has it that the cave conceals the ancient artifact you seek.")
        input("Press Enter to enter the cave...\n")

        artifact_x, artifact_y = 8, 8
        cave_map.set_artifact(artifact_x, artifact_y)

        while True:
            cave_map.draw(player)

            print("\nControls: W=Up, A=Left, S=Down, D=Right, Q=Quit, I=Inventory")
            action = input("Enter your move: ").upper()

            if action == "Q":
                print("Goodbye!")
                sys.exit()

            elif action == "I":
                view_inventory(player)
                continue

            move_player(player, action, cave_map)

            if player.x == artifact_x and player.y == artifact_y:
                print("You found the ancient artifact!")
                objectives["Find the Artifact"] = True
                input("Press Enter to continue...")


def display_objectives(objectives):
    print("\n--- Objectives ---")
    for objective, completed in objectives.items():
        status = "Complete" if completed else "Incomplete"
        print(f"{objective}: {status}")
    print("-------------------\n")

def view_inventory(player):
    print("\n--- Inventory ---")
    for item in player.inventory:
        print(item)
    print("-----------------\n")

def main():
    player_name = input("Enter your name: ")
    print_typewriter(f"\nGreetings, {player_name}!\n")
    print_typewriter("You are an explorer on a quest to find a legendary artifact hidden in a mysterious land.\n")
    print_typewriter("Rumors speak of a dark cave around the area, where the artifact might be hidden. Be cautious, and good luck!\n")
    print_typewriter("Press Enter to start your adventure...")
    input()

    player = Player(player_name, 0, 0)
    cave_map = CaveMap(10, 10)
    cave_map.set_entrance()
    cave_map.generate_cave_walls(50)
    cave_map.scatter_loot(5) 
    cave_map.scatter_enemies(10)  

    objectives = {
        "Defeat All Enemies": False,
        "Find the Artifact": False,
        "Enter the Cave": False 
    }


    while True:
        cave_map.draw(player)

        print(player)
        display_objectives(objectives)

        if not objectives["Defeat All Enemies"]:
            print("---- Defeat all enemies in the area before entering the dark cave. ----\n")
            print("m - enemies")
            print("D - dark cave")
        elif player.x == cave_map.entrance_x and player.y == cave_map.entrance_y:
            print_typewriter("\nYou are at the entrance of a dark cave.")
            print_typewriter("Press 'D' to enter the cave.")

        print("\nControls: W=Up, A=Left, S=Down, D=Right, Q=Quit, I=Inventory")
        action = input("Enter your move: ").upper()

        if action == "Q":
            print_typewriter("Goodbye!")
            sys.exit()

        elif action == "I":
            view_inventory(player)
            continue

        move_player(player, action, cave_map)

        if not objectives["Defeat All Enemies"] and all((x, y) not in cave_map.enemies for x in range(cave_map.width) for y in range(cave_map.height)):
            objectives["Defeat All Enemies"] = True
            print_typewriter("\nYou have defeated all enemies in the area!")

        handle_landmark(player, objectives, cave_map)

        if all(objectives.values()):
            print_typewriter("\nCongratulations! You've found the artifact. You can continue exploring or quit the game.")
            display_objectives(objectives)
            input("Press Enter to continue...")

if __name__ == "__main__":
    start_menu()
