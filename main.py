import pygame
from pygame import mixer
import random
import json
import os
from datetime import datetime

pygame.init()
mixer.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Hero Battle Game")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Fonts
font = pygame.font.SysFont(None, 36)
small_font = pygame.font.SysFont(None, 24)

# Game States
SELECTION = 0
BATTLE = 1
WIN = 2
LOSE = 3
FINAL_WIN = 4
SHOP = 5
WELCOME = 6
TIE = 7
game_state = WELCOME

SAVE_FILE = 'game_save.json'

def get_current_date():
    return datetime.now().strftime("%Y-%m-%d")

def get_daily_shop_items():
    """Generate daily shop items based on current date"""
    today = get_current_date()

    # Base items that are always available
    daily_items = [
        {"name": "Upgrade Health (+10)", "cost": 20, "purchased": False, "type": "upgrade", "stat": "health", "amount": 10},
        {"name": "Upgrade Mana (+10)", "cost": 25, "purchased": False, "type": "upgrade", "stat": "mana", "amount": 10}
    ]

    # Use date as seed for random but deterministic daily items
    random.seed(hash(today))

    # Pool of special daily items
    special_items = [
        {"name": "Unlock Rocket Ability (Mage)", "cost": 50, "purchased": False, "type": "ability", "hero": "Mage", "ability": {"name": "Rocket", "damage": 50, "mana": 30}},
        {"name": "Unlock Ice Blast Ability (Mage)", "cost": 40, "purchased": False, "type": "ability", "hero": "Mage", "ability": {"name": "Ice Blast", "damage": 35, "mana": 20}},
        {"name": "Unlock Lighting Storm Ability (Mage)", "cost": 60, "purchased": False, "type": "ability", "hero": "Mage", "ability": {"name": "Lightning Storm", "damage": 65, "mana": 35}},
        {"name": "Unlock Fire Barrier Ability (Warrior)", "cost": 45, "purchased": False, "type": "ability", "hero": "Warrior", "ability": {"name": "Fire Barrier", "heal": 25, "mana": 20}},
        {"name": "Unlock Multi-Shot Ability (Archer)", "cost": 55, "purchased": False, "type": "ability", "hero": "Archer", "ability": {"name": "Multi-Shot", "damage": 45, "mana": 25}},
        {"name": "Buy Mercenary (reduces enemy damage)", "cost": 30, "purchased": False, "type": "mercenary"},
        {"name": "Buy Veteran Soldier (reduces enemy damage more)", "cost": 60, "purchased": False, "type": "mercenary"},
    ]

    # Select 3 random special items for today
    selected_special = random.sample(special_items, 3)
    daily_items.extend(selected_special)

    # Occasionally add legendary items based on player progress
    if current_level >= 5 and random.random() < 0.3:
        legendary_items = [
            {"name": "Unlock New Hero: Paladin", "cost": 100, "purchased": False, "type": "new_hero", "hero": {
                "name": "Paladin",
                "color": (255, 215, 0),
                "abilities": [
                    {"name": "Holy Strike", "damage": 25, "mana": 12},
                    {"name": "Divine Shield", "heal": 20, "mana": 20},
                    {"name": "Judgement", "damage": 40, "mana": 30}
                ]
            }}
        ]
        daily_items.extend(legendary_items[:1])

    if current_level >= 8 and random.random() < 0.2:
        ultimate_items = [
            {"name": "Unlock Legendary Hero: Legend", "cost": 500, "purchased": False, "type": "new_hero", "hero": {
                "name": "Legend",
                "color": (255, 0, 255),
                "abilities": [
                    {"name": "Supernova", "damage": 100, "mana": 50},
                    {"name": "Regeneration", "heal": 50, "mana": 30},
                    {"name": "Divine Wrath", "damage": 150, "mana": 80}
                ]
            }}
        ]
        daily_items.extend(ultimate_items[:1])

    return daily_items

def load_game():
    global current_level, coins, player_extra_health, player_extra_mana, unlocked_abilities, bought_mercenaries, shop_items, HEROES
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, 'r') as f:
            try:
                save_data = json.load(f)
                current_level = save_data.get('current_level', 1)
                coins = save_data.get('coins', 0)
                player_extra_health = save_data.get('player_extra_health', 0)
                player_extra_mana = save_data.get('player_extra_mana', 0)
                unlocked_abilities = save_data.get('unlocked_abilities', {})
                bought_mercenaries = save_data.get('bought_mercenaries', [])
                shop_items[:] = save_data.get('shop_items', [])
                HEROES[:] = save_data.get('heroes', [])
                print(f"Game loaded: Level {current_level}, Coins: {coins}")
            except Exception as e:
                print(f"Failed to load save: {e}")

def save_game():
    save_data = {
        'current_level': current_level,
        'coins': coins,
        'player_extra_health': player_extra_health,
        'player_extra_mana': player_extra_mana,
        'unlocked_abilities': unlocked_abilities,
        'bought_mercenaries': bought_mercenaries,
        'shop_items': shop_items,
        'heroes': HEROES
    }
    try:
        with open(SAVE_FILE, 'w') as f:
            json.dump(save_data, f)
        print(f"Game saved: Level {current_level}, Coins: {coins}")
    except Exception as e:
        print(f"Failed to save: {e}")
    finally:
        f.close() if 'f' in locals() and not f.closed else None

# Default data
default_shop_items = [
    {"name": "Upgrade Health (+10)", "cost": 20, "purchased": False, "type": "upgrade", "stat": "health", "amount": 10},
    {"name": "Upgrade Mana (+10)", "cost": 25, "purchased": False, "type": "upgrade", "stat": "mana", "amount": 10},
    {"name": "Unlock Rocket Ability (Mage)", "cost": 50, "purchased": False, "type": "ability", "hero": "Mage", "ability": {"name": "Rocket", "damage": 50, "mana": 30}},
    {"name": "Buy Mercenary (reduces enemy damage)", "cost": 30, "purchased": False, "type": "mercenary"},
    {"name": "Unlock New Hero: Paladin", "cost": 100, "purchased": False, "type": "new_hero", "hero": {
        "name": "Paladin",
        "color": (255, 215, 0),
        "abilities": [
            {"name": "Holy Strike", "damage": 25, "mana": 12},
            {"name": "Divine Shield", "heal": 20, "mana": 20},
            {"name": "Judgement", "damage": 40, "mana": 30}
        ]
    }},
    {"name": "Unlock Legendary Hero: Legend", "cost": 1000, "purchased": False, "type": "new_hero", "hero": {
        "name": "Legend",
        "color": (255, 0, 255),
        "abilities": [
            {"name": "Supernova", "damage": 100, "mana": 50},
            {"name": "Regeneration", "heal": 50, "mana": 30},
            {"name": "Divine Wrath", "damage": 150, "mana": 80}
        ]
    }}
]

# Heroes Data
HEROES = [
    {
        "name": "Warrior",
        "color": RED,
        "image": "warrior.png",
        "abilities": [
            {"name": "Slash", "damage": 20, "mana": 10},
            {"name": "Block", "heal": 10, "mana": 15},
            {"name": "Charge", "damage": 30, "mana": 20}
        ]
    },
    {
        "name": "Mage",
        "color": BLUE,
        "image": "mage.png",
        "abilities": [
            {"name": "Fireball", "damage": 25, "mana": 12},
            {"name": "Heal", "heal": 15, "mana": 18},
            {"name": "Lightning", "damage": 35, "mana": 25}
        ]
    },
    {
        "name": "Archer",
        "color": GREEN,
        "image": "archer.png",
        "abilities": [
            {"name": "Shoot Arrow", "damage": 18, "mana": 8},
            {"name": "Poison Arrow", "damage": 15, "effect": "poison", "mana": 10},
            {"name": "Rapid Fire", "damage": 40, "mana": 30}
        ]
    }
]

class Hero:
    def __init__(self, data):
        self.name = data["name"]
        self.color = data["color"]
        self.health = 100 + player_extra_health
        self.mana = 100 + player_extra_mana
        self.abilities = data["abilities"] + unlocked_abilities.get(data["name"], [])

# Enemy class
class Enemy:
    def __init__(self, level):
        self.max_health = 100 + level * 50  # Increasing health with level
        self.health = self.max_health
        self.mana = 50
        self.poison = 0
        self.abilities = [
            {"name": "Attack", "damage": 10 + level * 2},
            {"name": "Heal", "heal": 10},
            {"name": "Special", "damage": 20 + level * 4}
        ]

selected_hero = None
enemy = None

hero_buttons = []
ability_buttons = []

# Animation
animation_frames = 0
animation_button = -1
damage_texts = []

# Background Audio System
audio_files = {
    'battle_bgm': 'battle_music.ogg',
    'victory_bgm': 'victory_music.ogg',
    'defeat_bgm': 'defeat_music.ogg',
    'menu_bgm': 'menu_music.ogg'
}

def play_background_music(state):
    """Play appropriate background music for the current game state"""
    try:
        if state in ['battle', 'selection', 'welcome']:
            music_file = audio_files.get('battle_bgm', 'battle_music.ogg')
        elif state == 'win':
            music_file = audio_files.get('victory_bgm', 'victory_music.ogg')
        elif state in ['lose', 'tie']:
            music_file = audio_files.get('defeat_bgm', 'defeat_music.ogg')
        elif state == 'shop':
            music_file = audio_files.get('menu_bgm', 'menu_music.ogg')
        else:
            music_file = audio_files.get('menu_bgm', 'menu_music.ogg')

        if os.path.exists(music_file):
            mixer.music.load(music_file)
            mixer.music.play(-1)  # Loop indefinitely
        else:
            # Fallback to procedural tone generation
            generate_fallback_music(state)
    except:
        # If music fails, generate procedural fallback
        generate_fallback_music(state)

def generate_fallback_music(state):
    """Generate basic procedural music if audio files don't exist"""
    try:
        # Simple square wave tone generation for different states
        sample_rate = 44100
        duration = 2.0  # 2 seconds

        if state == 'welcome':
            frequency = 261.63  # C4
        elif state == 'battle':
            frequency = 392.00  # G4
        elif state == 'win':
            frequency = 523.25  # C5
        elif state == 'lose':
            frequency = 146.83  # D3
        elif state == 'shop':
            frequency = 293.66  # D4
        else:
            frequency = 220.00  # A3

        # Create simple audio data using procedural generation
        import numpy as np
        if 'np' in globals():
            t = np.linspace(0, duration, int(sample_rate * duration), False)
            wave = np.sin(frequency * 2 * np.pi * t) * 0.3
            fade_out = np.linspace(1, 0, int(sample_rate * 0.5))
            wave[-len(fade_out):] *= fade_out

            # Create simple pygame mixer Sound
            # For demo purposes, we'll just use pygame's built-in sound
            pass
        else:
            # Fallback: no numpy, just continue with silence
            pass

    except:
        pass  # Silent fail if music generation fails

# Initialize background music for welcome screen
play_background_music('welcome')

def draw_hero_selection():
    screen.fill(BLACK)
    title = font.render("Choose Your Hero", True, WHITE)
    screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 50))

    shop_prompt = small_font.render("Press S for Shop", True, WHITE)
    screen.blit(shop_prompt, (SCREEN_WIDTH//2 - shop_prompt.get_width()//2, 80))

    global hero_buttons
    hero_buttons = []
    for i, hero in enumerate(HEROES):
        text = font.render(hero["name"], True, hero["color"])
        x = SCREEN_WIDTH//2 - text.get_width()//2
        y = 150 + i * 80
        hero_buttons.append(pygame.Rect(x, y, text.get_width(), text.get_height()))
        screen.blit(text, (x, y))

def draw_win():
    play_background_music('win')
    screen.fill(BLACK)
    title = font.render("Victory!", True, GREEN)
    screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 150))
    subtitle = small_font.render(f"Level {current_level} Completed! +30 Coins. Total: {coins}", True, WHITE)
    screen.blit(subtitle, (SCREEN_WIDTH//2 - subtitle.get_width()//2, 200))
    again = small_font.render("Press R for next level or Q to quit", True, WHITE)
    screen.blit(again, (SCREEN_WIDTH//2 - again.get_width()//2, 250))
    save_game()

def draw_lose():
    screen.fill(BLACK)
    title = font.render("Defeat", True, RED)
    screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 150))
    subtitle = small_font.render("The enemy was too strong!", True, WHITE)
    screen.blit(subtitle, (SCREEN_WIDTH//2 - subtitle.get_width()//2, 200))
    again = small_font.render("Press R to play again or Q to quit", True, WHITE)
    screen.blit(again, (SCREEN_WIDTH//2 - again.get_width()//2, 250))
    save_game()

def draw_final_win():
    screen.fill(BLACK)
    title = font.render("All Levels Completed!", True, GREEN)
    screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 150))
    subtitle = small_font.render("Congratulations!", True, WHITE)
    screen.blit(subtitle, (SCREEN_WIDTH//2 - subtitle.get_width()//2, 200))
    coins_text = small_font.render(f"Total Coins: {coins}", True, GREEN)
    screen.blit(coins_text, (SCREEN_WIDTH//2 - coins_text.get_width()//2, 230))
    again = small_font.render("Press R for main menu or Q to quit", True, WHITE)
    screen.blit(again, (SCREEN_WIDTH//2 - again.get_width()//2, 280))
    save_game()

def draw_tie():
    screen.fill(BLACK)
    title = font.render("Tie!", True, YELLOW)
    screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 150))
    subtitle = small_font.render(f"Mana depleted! +15 Coins. Total: {coins}", True, WHITE)
    screen.blit(subtitle, (SCREEN_WIDTH//2 - subtitle.get_width()//2, 200))
    again = small_font.render("Press R to retry level or Q to quit", True, WHITE)
    screen.blit(again, (SCREEN_WIDTH//2 - again.get_width()//2, 250))
    save_game()

def draw_shop():
    screen.fill((100, 100, 100))
    title = font.render("Shop", True, WHITE)
    screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 50))
    coins_text = small_font.render(f"Coins: {coins}", True, WHITE)
    screen.blit(coins_text, (50, 70))
    y_offset = 100
    for item in shop_items:
        if not item["purchased"]:
            text = small_font.render(f"{item['name']} - {item['cost']} coins", True, WHITE)
            screen.blit(text, (50, y_offset))
            y_offset += 30
    return_text = small_font.render("Press B to go back", True, WHITE)
    screen.blit(return_text, (SCREEN_WIDTH//2 - return_text.get_width()//2, SCREEN_HEIGHT - 50))

def draw_welcome():
    screen.fill(BLACK)
    title = font.render("Hero Battle Game", True, WHITE)
    screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 100))

    instructions = [
        "Controls:",
        "- Mouse: Click to select heroes and use abilities",
        "- S: Open shop to buy upgrades",
        "- B: Go back from shop",
        "- R: Restart after battle/end game",
        "- Q: Quit game",
        "",
        "Goal: Battle through 20 levels and defeat enemies!",
        "",
        "Press any key to start"
    ]

    y = 180
    for line in instructions:
        if line == "":
            y += 30
        elif line.startswith("- ") or line.startswith("Controls:") or line.startswith("Goal:"):
            text = small_font.render(line, True, GREEN)
            screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, y))
            y += 25
        else:
            text = small_font.render(line, True, WHITE)
            screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, y))
            y += 25

def draw_battle():
    screen.fill(WHITE)
    # Draw hero info
    hero_text = font.render(f"{selected_hero.name} HP: {selected_hero.health} Mana: {selected_hero.mana}", True, selected_hero.color)
    screen.blit(hero_text, (10, 10))

    # Draw enemy info
    enemy_text = font.render(f"Enemy HP: {enemy.health} Mana: {enemy.mana}", True, RED)
    screen.blit(enemy_text, (SCREEN_WIDTH//2 + 10, 10))

    # Draw abilities
    global ability_buttons
    ability_buttons = []
    for i, ability in enumerate(selected_hero.abilities):
        color = GREEN if selected_hero.mana >= ability.get("mana", 0) else RED
        text = small_font.render(f"{ability['name']} ({ability.get('mana', 0)} mana)", True, color)
        x = 10 + i * 200
        y = SCREEN_HEIGHT - 60
        ability_buttons.append(pygame.Rect(x, y, text.get_width(), text.get_height()))
        screen.blit(text, (x, y))

    # Animation
    if animation_frames > 0:
        pygame.draw.circle(screen, selected_hero.color, (400, 300), animation_frames * 10)
        animation_frames -= 1

    # Damage texts
    for text, pos, life in damage_texts:
        pygame.draw.rect(screen, BLACK, (pos[0]-50, pos[1]-20, 100, 40))
        screen.blit(text, pos)
        life -= 1

    damage_texts[:] = [(t, p, l) for t, p, l in damage_texts if l > 0]

# Initialize global variables
current_level = 1
coins = 0
player_extra_health = 0
player_extra_mana = 0
unlocked_abilities = {}
bought_mercenaries = []
shop_items = default_shop_items.copy()

def refresh_shop_items():
    """Check if shop needs to be refreshed for the new day"""
    global shop_items
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, 'r') as f:
            try:
                save_data = json.load(f)
                last_refresh = save_data.get('last_daily_refresh', '')
                current_date = get_current_date()

                if last_refresh != current_date or save_data.get('daily_shop_items') is None:
                    # New day or no daily shop - generate new items
                    new_shop_items = get_daily_shop_items()
                    shop_items = new_shop_items

                    # Update save with new date and items
                    save_data['last_daily_refresh'] = current_date
                    save_data['daily_shop_items'] = new_shop_items
                    save_data['shop_items'] = new_shop_items

                    with open(SAVE_FILE, 'w') as w:
                        json.dump(save_data, w)
                    print(f"Shop refreshed for {current_date}")
                else:
                    # Load existing daily shop items
                    shop_items = save_data.get('daily_shop_items', default_shop_items.copy())
                    print(f"Using existing shop for {current_date}")
            except Exception as e:
                print(f"Error refreshing shop: {e}")
                shop_items = get_daily_shop_items()
    else:
        # No save file, generate new shop
        shop_items = get_daily_shop_items()

        # Create initial save with daily shop
        initial_save = {
            'current_level': current_level,
            'coins': coins,
            'player_extra_health': player_extra_health,
            'player_extra_mana': player_extra_mana,
            'unlocked_abilities': unlocked_abilities,
            'bought_mercenaries': bought_mercenaries,
            'shop_items': shop_items,
            'daily_shop_items': shop_items,
            'last_daily_refresh': get_current_date(),
            'heroes': HEROES
        }
        try:
            with open(SAVE_FILE, 'w') as f:
                json.dump(initial_save, f)
        except Exception as e:
            print(f"Failed to create initial save: {e}")

load_game()
refresh_shop_items()

print("Starting Hero Battle Game...")
print("Welcome to the game!")

# Main game loop
running = True
clock = pygame.time.Clock()

def enemy_turn():
    global game_state
    if enemy.health > 0 and selected_hero.health > 0:
        # Enemy chooses random ability
        ability_index = random.randint(0, len(enemy.abilities) - 1)
        ability = enemy.abilities[ability_index]

        if ability["name"] == "Heal" and enemy.mana >= 5 and enemy.health < enemy.max_health:
            enemy.mana -= 5
            heal_amount = ability["heal"]
            enemy.health = min(enemy.health + heal_amount, enemy.max_health)
            damage_texts.append((small_font.render(f"Enemy healed {heal_amount}", True, BLUE), [600, 200], 60))
        else:
            # Reduce damage if mercenaries are bought
            damage_reduction = len(bought_mercenaries) * 0.1
            reduced_damage = ability["damage"] * (1 - damage_reduction)
            selected_hero.health -= reduced_damage
            damage_texts.append((small_font.render(f"Enemy {ability['name']}: -{int(reduced_damage)}", True, RED), [200, 200], 60))

            if selected_hero.health <= 0:
                game_state = LOSE
                selected_hero.health = 0
            elif selected_hero.mana <= 0 and not any(selected_hero.mana >= a.get("mana", 0) for a in selected_hero.abilities):
                game_state = TIE
            else:
                pass  # Continue battle

def purchase_item(index):
    global coins, player_extra_health, player_extra_mana, unlocked_abilities, bought_mercenaries
    item = shop_items[index]
    if not item["purchased"] and coins >= item["cost"]:
        coins -= item["cost"]
        item["purchased"] = True
        if item["type"] == "upgrade":
            if item["stat"] == "health":
                player_extra_health += item["amount"]
            elif item["stat"] == "mana":
                player_extra_mana += item["amount"]
        elif item["type"] == "ability":
            if item["hero"] not in unlocked_abilities:
                unlocked_abilities[item["hero"]] = []
            unlocked_abilities[item["hero"]].append(item["ability"])
        elif item["type"] == "mercenary":
            bought_mercenaries.append(item)
        elif item["type"] == "new_hero":
            HEROES.append(item["hero"])

def reset_game():
    global selected_hero, enemy, hero_buttons, ability_buttons, animation_frames, animation_button, damage_texts, game_state
    selected_hero = None
    enemy = None
    hero_buttons = []
    ability_buttons = []
    animation_frames = 0
    animation_button = -1
    damage_texts = []
    game_state = WELCOME

# Main loop
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if game_state == WELCOME:
                game_state = SELECTION
                load_game()
        elif game_state == SELECTION:
            if event.key == pygame.K_s:
                game_state = SHOP
                play_background_music('shop')
            elif event.key == pygame.K_b:
                game_state = SELECTION
            elif game_state == SHOP:
                if event.key == pygame.K_b:
                    game_state = SELECTION
            elif game_state in [WIN, LOSE, TIE, FINAL_WIN]:
                if event.key == pygame.K_r:
                    if game_state == WIN:
                        current_level += 1
                        coins += 30 if game_state == WIN else 15
                    elif game_state == TIE:
                        coins += 15
                    elif game_state == FINAL_WIN:
                        pass
                    else:
                        current_level = 1
                    reset_game()
                    if current_level > 20:
                        game_state = FINAL_WIN
                    else:
                        game_state = SELECTION
                elif event.key == pygame.K_q:
                    running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if game_state == SELECTION:
                for i, button in enumerate(hero_buttons):
                    if button.collidepoint(mouse_x, mouse_y):
                        selected_hero = Hero(HEROES[i])
                        enemy = Enemy(current_level)
                        game_state = BATTLE
                        break
            elif game_state == BATTLE:
                for i, button in enumerate(ability_buttons):
                    if button.collidepoint(mouse_x, mouse_y):
                        ability = selected_hero.abilities[i]
                        mana_cost = ability.get("mana", 0)
                        if selected_hero.mana >= mana_cost:
                            selected_hero.mana -= mana_cost
                            if "damage" in ability:
                                damage = ability["damage"]
                                if ability.get("effect") == "poison":
                                    enemy.poison += 1
                                    damage_texts.append((small_font.render(f"{ability['name']}: -{damage} +Poison", True, GREEN), [600, 200], 60))
                                else:
                                    damage_texts.append((small_font.render(f"{ability['name']}: -{damage}", True, GREEN), [600, 200], 60))
                                enemy.health -= damage
                                animation_frames = 10
                                animation_button = i
                                if enemy.health <= 0:
                                    if current_level >= 10:
                                        game_state = FINAL_WIN
                                        coins += 30
                                    else:
                                        game_state = WIN
                                        coins += 30
                                    enemy.health = 0
                                elif selected_hero.mana <= 0 and not any(selected_hero.mana >= a.get('mana', 0) for a in selected_hero.abilities):
                                    game_state = TIE
                                    coins += 15
                                else:
                                    enemy_turn()
                            elif "heal" in ability:
                                heal_amount = ability["heal"]
                                selected_hero.health = min(selected_hero.health + heal_amount, 100 + player_extra_health)
                                damage_texts.append((small_font.render(f"{ability['name']}: +{heal_amount}", True, BLUE), [200, 200], 60))
                                enemy_turn()
            elif game_state == SHOP:
                # Shop item purchasing by mouse click
                y_offset = 100
                for i, item in enumerate(shop_items):
                    if not item["purchased"]:
                        text_rect = pygame.Rect(50, y_offset, 400, 30)
                        if text_rect.collidepoint(mouse_x, mouse_y):
                            purchase_item(i)
                        y_offset += 30

    # Handle mouse hover for cursor change
    mouse_x, mouse_y = pygame.mouse.get_pos()
    hovering = False

    if game_state == SELECTION:
        for button in hero_buttons:
            if button.collidepoint(mouse_x, mouse_y):
                hovering = True
                break
    elif game_state == BATTLE:
        for button in ability_buttons:
            if button.collidepoint(mouse_x, mouse_y):
                hovering = True
                break
    elif game_state == SHOP:
        y_offset = 100
        for item in shop_items:
            if not item["purchased"]:
                text_rect = pygame.Rect(50, y_offset, 400, 30)
                if text_rect.collidepoint(mouse_x, mouse_y):
                    hovering = True
                    break
                y_offset += 30

    if hovering:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    else:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    # Draw based on state
    if game_state == WELCOME:
        draw_welcome()
    elif game_state == SELECTION:
        draw_hero_selection()
    elif game_state == BATTLE:
        draw_battle()
    elif game_state == WIN:
        draw_win()
    elif game_state == LOSE:
        draw_lose()
    elif game_state == FINAL_WIN:
        draw_final_win()
    elif game_state == TIE:
        draw_tie()
    elif game_state == SHOP:
        draw_shop()

    pygame.display.flip()

pygame.quit()
