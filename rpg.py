import random 
import time
import threading
import tkinter as tk
from tkinter import scrolledtext

# ========================
#   RPG Textbasiertes Spiel (mit GUI)
# ========================

# --- GUI-Helferklasse ---
class GameGUI:
    def __init__(self, title="Python RPG"):
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry("700x480")

# --- Klassen für das Spiel ---
class Player:
    def __init__(self, name):
        self.name = name
        self.hp = 100
        self.attack = 10
        self.gold = 0
        self.inventory = []

    def is_alive(self):
        return self.hp > 0

class Enemy:
    def __init__(self, name, hp, attack, gold_reward):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.gold_reward = gold_reward

    def is_alive(self):
        return self.hp > 0


# --- Landschaften & Gegner ---
landscapes = {
    "Wald": [
        Enemy("Wolf", 30, 5, 10),
        Enemy("Räuber", 40, 7, 15)
    ],
    "Berge": [
        Enemy("Goblin", 35, 6, 12),
        Enemy("Troll", 60, 10, 25)
    ],
    "Dorf": [],
}

quests = [
    {"name": "Besiege 1 Wolf im Wald", "target": "Wolf", "done": False, "reward": 30},
    {"name": "Besiege einen Troll in den Bergen", "target": "Troll", "done": False, "reward": 50},
]

# --- Hilfsfunktionen ---
def slow_print(text, delay=0.03):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def show_stats(player):
    print(f"\n{name}'s Status:")
    print(f"❤️  HP: {player.hp}")
    print(f"⚔️  Angriff: {player.attack}")
    print(f"💰 Gold: {player.gold}")
    print(f"🎒 Inventar: {', '.join(player.inventory) if player.inventory else 'leer'}\n")


def fight(player, enemy):
    slow_print(f"⚔️ Du kämpfst gegen {enemy.name}!")

    while player.is_alive() and enemy.is_alive():
        print(f"\n{player.name}: {player.hp} HP | {enemy.name}: {enemy.hp} HP")
        action = input("Willst du [A]ngreifen oder [F]lucht ergreifen? ").lower()

        if action == "a":
            damage = random.randint(player.attack - 3, player.attack + 3)
            slow_print(f"💥 Du triffst {enemy.name} für {damage} Schaden!")
            enemy.hp -= damage
        elif action == "f":
            slow_print("🏃 Du fliehst!")
            return False
        else:
            slow_print("Ungültige Eingabe!")
            continue

        if enemy.is_alive():
            damage = random.randint(enemy.attack - 2, enemy.attack + 2)
            slow_print(f"{enemy.name} greift dich an und verursacht {damage} Schaden!")
            player.hp -= damage

    if player.is_alive():
        slow_print(f"✅ Du hast {enemy.name} besiegt!")
        player.gold += enemy.gold_reward
        slow_print(f"💰 Du erhältst {enemy.gold_reward} Gold!")
        check_quests(player, enemy)
        return True
    else:
        slow_print("☠️ Du wurdest besiegt...")
        return False


def check_quests(player, enemy):
    for quest in quests:
        if quest["target"] == enemy.name and not quest["done"]:
            quest["done"] = True
            player.gold += quest["reward"]
            slow_print(f"🎉 Quest abgeschlossen: {quest['name']}! (+{quest['reward']} Gold)")


def explore(player, location):
    enemies = landscapes.get(location, [])
    if not enemies:
        slow_print("Hier ist es friedlich. Du ruhst dich aus.")
        player.hp = min(100, player.hp + 10)
        return

    enemy = random.choice(enemies)
    fight(player, Enemy(enemy.name, enemy.hp, enemy.attack, enemy.gold_reward))


def show_quests():
    print("\n📜 Deine Quests:")
    for quest in quests:
        status = "✅" if quest["done"] else "❌"
        print(f"  {status} {quest['name']}")
    print()


# --- Hauptspiel ---
slow_print("🌍 Willkommen zum Python RPG!")
name = input("Wie heißt dein Held? ")
player = Player(name)
slow_print(f"Willkommen, {name}! Dein Abenteuer beginnt...")

while player.is_alive():
    show_stats(player)
    print("Orte, die du besuchen kannst: Wald, Berge, Dorf")
    choice = input("Wohin willst du reisen? (oder 'q' zum Beenden) ").capitalize()

    if choice == "Q":
        slow_print("👋 Auf Wiedersehen, Held!")
        break
    elif choice in landscapes:
        explore(player, choice)
    else:
        slow_print("Dieser Ort existiert nicht...")

    show_quests()

if not player.is_alive():
    slow_print("💀 Dein Abenteuer endet hier...")



