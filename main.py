import pygame
import random
import json
import os
from datetime import datetime

pygame.init()

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
DARK_RED = (139, 0, 0)
DARK_BLUE = (0, 0, 139)

import math

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
DEBUG_MODE = False

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
        {"name": "Unlock Lightning Storm Ability (Mage)", "cost": 60, "purchased": False, "type": "ability", "hero": "Mage", "ability": {"name": "Lightning Storm", "damage": 65, "mana": 35}},
        {"name": "Unlock Fire Barrier Ability (Warrior)", "cost": 45, "purchased": False, "type": "ability", "hero": "Warrior", "ability": {"name": "Fire Barrier", "heal": 25, "mana": 20}},
        {"name": "Unlock Multi-Shot Ability (Archer)", "cost": 55, "purchased": False, "type": "ability", "hero": "Archer", "ability": {"name": "Multi-Shot", "damage": 45, "mana": 25}},
        {"name": "Unlock Dragon Scales Ability (Warrior)", "cost": 70, "purchased": False, "type": "ability", "hero": "Warrior", "ability": {"name": "Dragon Scales", "heal": 40, "mana": 25}},
        {"name": "Unlock Shadow Arrow Ability (Archer)", "cost": 65, "purchased": False, "type": "ability", "hero": "Archer", "ability": {"name": "Shadow Arrow", "damage": 55, "mana": 35}},
        {"name": "Unlock Meteor Ability (Mage)", "cost": 75, "purchased": False, "type": "ability", "hero": "Mage", "ability": {"name": "Meteor", "damage": 80, "mana": 45}},
        {"name": "Buy Mercenary (reduces enemy damage)", "cost": 30, "purchased": False, "type": "mercenary"},
        {"name": "Buy Veteran Soldier (reduces enemy damage more)", "cost": 60, "purchased": False, "type": "mercenary"},
        {"name": "Buy Elite Mercenary (much stronger!", "cost": 120, "purchased": False, "type": "mercenary"},
    ]

    # Daily Epic Hero - changes every day
    epic_heroes = [
        {
            "name": "Unlock Epic Hero: Ninja", "cost": 500, "purchased": False, "type": "new_hero", "hero": {
                "name": "Ninja",
                "color": (50, 50, 50),
                "abilities": [
                    {"name": "Stealth Strike", "damage": 45, "mana": 15},
                    {"name": "Shuriken Barrage", "damage": 60, "mana": 30},
                    {"name": "Shadow Clone", "damage": 35, "mana": 20}
                ]
            }
        },
        {
            "name": "Unlock Epic Hero: Sorcerer", "cost": 500, "purchased": False, "type": "new_hero", "hero": {
                "name": "Sorcerer",
                "color": (138, 43, 226),
                "abilities": [
                    {"name": "Dark Magic", "damage": 55, "mana": 25},
                    {"name": "Soul Drain", "damage": 40, "heal": 20, "mana": 35},
                    {"name": "Arcane Explosion", "damage": 70, "mana": 40}
                ]
            }
        },
        {
            "name": "Unlock Epic Hero: Valkyrie", "cost": 500, "purchased": False, "type": "new_hero", "hero": {
                "name": "Valkyrie",
                "color": (220, 20, 60),
                "abilities": [
                    {"name": "Spear of Destiny", "damage": 50, "mana": 20},
                    {"name": "Divine Wind", "damage": 35, "heal": 25, "mana": 30},
                    {"name": "Valkyrie Chant", "damage": 65, "mana": 35}
                ]
            }
        },
        {
            "name": "Unlock Epic Hero: Summoner", "cost": 500, "purchased": False, "type": "new_hero", "hero": {
                "name": "Summoner",
                "color": (35, 107, 142),
                "abilities": [
                    {"name": "Spirit Wolf", "damage": 48, "mana": 18},
                    {"name": "Elemental Avatar", "heal": 35, "mana": 28},
                    {"name": "Ancient Phoenix", "damage": 75, "mana": 45}
                ]
            }
        }
    ]

    # Daily Legendary Hero - changes every day
    legendary_heroes = [
        {
            "name": "Unlock Legendary Hero: Dragon Lord", "cost": 1000, "purchased": False, "type": "new_hero", "hero": {
                "name": "Dragon Lord",
                "color": (255, 69, 0),
                "abilities": [
                    {"name": "Dragon Breath", "damage": 90, "mana": 40},
                    {"name": "Scale Armor", "heal": 60, "mana": 30},
                    {"name": "Divine Draconic Wrath", "damage": 130, "mana": 70}
                ]
            }
        },
        {
            "name": "Unlock Legendary Hero: Archangel", "cost": 1000, "purchased": False, "type": "new_hero", "hero": {
                "name": "Archangel",
                "color": (255, 215, 0),
                "abilities": [
                    {"name": "Sacred Light", "damage": 85, "heal": 40, "mana": 35},
                    {"name": "Divine Intervention", "heal": 80, "mana": 45},
                    {"name": "Judgment Day", "damage": 125, "mana": 80}
                ]
            }
        },
        {
            "name": "Unlock Legendary Hero: Death Knight", "cost": 1000, "purchased": False, "type": "new_hero", "hero": {
                "name": "Death Knight",
                "color": (105, 105, 105),
                "abilities": [
                    {"name": "Life Drain", "damage": 95, "heal": 35, "mana": 30},
                    {"name": "Death Coil", "damage": 80, "mana": 40},
                    {"name": "Army of the Dead", "damage": 120, "mana": 75}
                ]
            }
        },
        {
            "name": "Unlock Legendary Hero: Phoenix Rider", "cost": 1000, "purchased": False, "type": "new_hero", "hero": {
                "name": "Phoenix Rider",
                "color": (255, 140, 0),
                "abilities": [
                    {"name": "Immolation", "damage": 100, "heal": 30, "mana": 50},
                    {"name": "Phoenix Fire", "damage": 110, "mana": 60},
                    {"name": "Rebirth", "heal": 100, "mana": 80}
                ]
            }
        }
    ]

    # Select 2 random special items for today (reduced to make room for heroes)
    selected_special = random.sample(special_items, 2)
    daily_items.extend(selected_special)

    # Add daily Epic Hero
    epic_index = random.randint(0, len(epic_heroes) - 1)
    daily_items.append(epic_heroes[epic_index])

    # Add daily Legendary Hero (different from Epic)
    legendary_index = random.randint(0, len(legendary_heroes) - 1)
    daily_items.append(legendary_heroes[legendary_index])

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
skip_button = None

# Animation
animation_frames = 0
animation_button = -1
damage_texts = []
damage_text_counter = 0

# Enhanced Visual Effects
particles = []
screen_shake = 0
fade_start = 0
fade_duration = 1000
brightness = 1.0
hue_shift = 0.0

class Particle:
    def __init__(self, x, y, color, dx, dy, life=30):
        self.x = x
        self.y = y
        self.color = color
        self.dx = dx
        self.dy = dy
        self.life = life
        self.size = random.randint(2, 6)

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.dy += 0.2  # gravity
        self.dx *= 0.98  # friction
        self.life -= 1
        return self.life > 0

    def draw(self, surface):
        if self.life > 0:
            alpha = min(255, self.life * 8)
            color_with_alpha = tuple(list(self.color) + [alpha])
            pygame.draw.circle(surface, color_with_alpha, (int(self.x), int(self.y)), self.size)

# Timing for enemy AI
class GameTimer:
    def __init__(self):
        self.last_enemy_turn = 0
        self.ENEMY_TURN_DELAY = 1000  # 1 second in milliseconds
        self.enemy_turn_count = 0
        self.player_turn_count = 0
        self.waiting_for_enemy_turn = False

game_timer = GameTimer()

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
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.play(-1)  # Loop indefinitely
        else:
            # Fallback to enhanced procedural music generation
            generate_procedural_music(state)
    except:
        # If music fails, generate procedural fallback
        generate_procedural_music(state)

def generate_procedural_music(state):
    """Generate enhanced procedural music with melodies and chords"""
    try:
        import numpy as np

        # Music parameters
        sample_rate = 44100
        bpm = 120
        seconds_per_beat = 60.0 / bpm

        # Different musical scales and progressions for different states
        if state == 'welcome':
            # Majestic welcome theme - A minor scale
            root_note = 220.00  # A3
            scale = [0, 2, 4, 5, 7, 9, 11, 12]  # A minor scale + octave
            progression = [9, 11, 12, 11, 9, 7, 5, 4]  # Simple melody
            harmony = [0, 4, 7]  # Am chord

        elif state == 'battle':
            # Intense battle theme - E minor scale
            root_note = 164.81  # E3
            scale = [0, 2, 4, 5, 7, 9, 11, 12]  # E minor
            progression = [7, 9, 11, 12, 11, 9, 7, 5, 4, 2]  # Fast paced
            harmony = [0, 3, 7]  # Em chord

        elif state == 'win':
            # Triumphant victory theme - C major scale
            root_note = 261.63  # C4
            scale = [0, 2, 4, 5, 7, 9, 11, 12]  # C major
            progression = [4, 5, 7, 9, 11, 12, 11, 9, 7, 5, 4, 0]  # Rising then falling
            harmony = [0, 4, 7]  # C chord

        elif state == 'lose' or state == 'tie':
            # Somber defeat theme - D minor scale
            root_note = 146.83  # D3
            scale = [0, 2, 3, 5, 7, 8, 10, 12]  # D minor
            progression = [0, -3, -5, -7, -8, -10]  # Descending sadness
            harmony = [0, 3, 7]  # Dm chord

        elif state == 'shop':
            # Peaceful shopping theme - F major scale
            root_note = 174.61  # F3
            scale = [0, 2, 4, 5, 7, 9, 11, 12]  # F major
            progression = [9, 7, 5, 4, 2, 0, -2, -5]  # Gentle wandering
            harmony = [0, 4, 7]  # F chord
        else:
            root_note = 220.00
            scale = [0, 2, 4, 5, 7, 9, 11, 12]
            progression = [4, 5, 7, 9, 11, 12]
            harmony = [0, 4, 7]

        # Generate musical phrases
        melody_duration = 8  # Number of notes
        harmony_duration = 4  # Number of harmony changes

        # Create melody line
        melody_notes = [root_note * (2 ** (scale[note % len(scale)] / 12)) for note in progression]
        melody_times = np.linspace(0, melody_duration * seconds_per_beat, len(melody_notes) * 100)
        melody_wave = np.zeros_like(melody_times)

        # Generate smooth melody
        note_samples = len(melody_times) // len(melody_notes)
        for i, note_freq in enumerate(melody_notes):
            start_idx = i * note_samples
            end_idx = min((i + 1) * note_samples, len(melody_times))

            # ADSR envelope for each note
            attack = 0.1 * note_samples
            decay = 0.2 * note_samples
            sustain = 0.7
            release = 0.1 * note_samples

            t_note = melody_times[start_idx:end_idx] - melody_times[start_idx]
            envelope = np.ones(len(t_note)) * sustain

            # Attack
            attack_samples = int(min(attack, len(t_note) * 0.5))
            if attack_samples > 0:
                envelope[:attack_samples] = np.linspace(0, 1, attack_samples)

            # Decay
            decay_end = int(min(attack + decay, len(t_note) * 0.8))
            if decay_end > attack:
                envelope[int(attack):decay_end] = np.linspace(1, sustain, decay_end - int(attack))

            # Release
            release_start = max(0, len(t_note) - int(release))
            if release_start < len(t_note):
                envelope[release_start:] = np.linspace(envelope[release_start], 0, len(t_note) - release_start)

            # Add vibrato for expressiveness
            vibrato = 0.005 * np.sin(2 * np.pi * 5 * t_note)

            # Mix waveforms for richer sound
            wave1 = np.sin(2 * np.pi * note_freq * t_note * (1 + vibrato))
            wave2 = 0.5 * np.sin(2 * np.pi * note_freq * 2 * t_note)  # Octave
            wave3 = 0.25 * np.sin(2 * np.pi * note_freq * 3 * t_note)  # Fifth
            wave = (wave1 + wave2 + wave3) * envelope * 0.3

            melody_wave[start_idx:end_idx] += wave

        # Create harmony/background track
        harmony_notes = [root_note * (2 ** (harmony[i] / 12)) for i in range(len(harmony))]
        harmony_times = np.linspace(0, melody_duration * seconds_per_beat, len(harmony_times))
        harmony_wave = np.zeros_like(harmony_times)

        harmony_samples = len(harmony_times) // len(harmony_notes)
        for i, note_freq in enumerate(harmony_notes):
            start_idx = i * harmony_samples
            end_idx = min((i + 1) * harmony_samples, len(harmony_times))

            t_note = harmony_times[start_idx:end_idx] - harmony_times[start_idx]
            envelope = np.ones(len(t_note)) * 0.2  # Softer volume

            wave = np.sin(2 * np.pi * note_freq * t_note) * envelope
            harmony_wave[start_idx:end_idx] += wave

        # Combine melody and harmony
        final_wave = melody_wave + harmony_wave * 0.4

        # Add some noise/reverb for texture
        noise_factor = 0.01
        reverb = np.convolve(final_wave, np.ones(500) / 500, mode='same')
        final_wave = final_wave + reverb * noise_factor + np.random.normal(0, 0.001, len(final_wave))

        # Create pygame sound and play
        # Convert to 16-bit signed integer format
        final_wave = (final_wave * 32767).astype(np.int16)

        # Create a simple loop by repeating the melody
        sound = pygame.mixer.Sound(final_wave.tobytes())
        sound.play(-1)  # Loop indefinitely

    except Exception as e:
        # Completely silent if music generation fails - no fallback beep
        pass

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
    if not save_flags['win']:
        play_background_music('win')
        save_game()
        save_flags['win'] = True
    screen.fill(BLACK)
    title = font.render("Victory!", True, GREEN)
    screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 150))
    subtitle = small_font.render(f"Level {current_level} Completed! +30 Coins. Total: {coins}", True, WHITE)
    screen.blit(subtitle, (SCREEN_WIDTH//2 - subtitle.get_width()//2, 200))
    # Show current level and progress with visual indicators
    level_display = f"LEVEL {current_level}/20"
    level_display_text = small_font.render(level_display, True, WHITE)
    screen.blit(level_display_text, (SCREEN_WIDTH//2 - level_display_text.get_width()//2, 210))

    # Progress bar showing level progression
    progress_width = 300
    progress_height = 10
    progress_x = SCREEN_WIDTH//2 - progress_width//2
    progress_y = 225
    pygame.draw.rect(screen, DARK_RED, (progress_x, progress_y, progress_width, progress_height))
    filled_width = int(progress_width * (current_level / 20))
    pygame.draw.rect(screen, GREEN, (progress_x, progress_y, filled_width, progress_height))

    again = small_font.render("Press P for next level or Q to quit", True, WHITE)
    screen.blit(again, (SCREEN_WIDTH//2 - again.get_width()//2, 240))

def draw_lose():
    if not save_flags['lose']:
        play_background_music('lose')
        save_game()
        save_flags['lose'] = True
    screen.fill(BLACK)
    title = font.render("Defeat", True, RED)
    screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 150))
    subtitle = small_font.render("The enemy was too strong!", True, WHITE)
    screen.blit(subtitle, (SCREEN_WIDTH//2 - subtitle.get_width()//2, 200))
    again = small_font.render("Press R to play again or Q to quit", True, WHITE)
    screen.blit(again, (SCREEN_WIDTH//2 - again.get_width()//2, 250))

def draw_final_win():
    if not save_flags['final_win']:
        play_background_music('win')
        save_game()
        save_flags['final_win'] = True
    screen.fill(BLACK)
    title = font.render("All Levels Completed!", True, GREEN)
    screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 150))
    subtitle = small_font.render("Congratulations!", True, WHITE)
    screen.blit(subtitle, (SCREEN_WIDTH//2 - subtitle.get_width()//2, 200))
    coins_text = small_font.render(f"Total Coins: {coins}", True, GREEN)
    screen.blit(coins_text, (SCREEN_WIDTH//2 - coins_text.get_width()//2, 230))
    again = small_font.render("Press R for main menu or Q to quit", True, WHITE)
    screen.blit(again, (SCREEN_WIDTH//2 - again.get_width()//2, 280))

def draw_tie():
    if not save_flags['tie']:
        play_background_music('lose')
        save_game()
        save_flags['tie'] = True
    screen.fill(BLACK)
    title = font.render("Tie!", True, YELLOW)
    screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 150))
    subtitle = small_font.render(f"Mana depleted! +15 Coins. Total: {coins}", True, WHITE)
    screen.blit(subtitle, (SCREEN_WIDTH//2 - subtitle.get_width()//2, 200))
    again = small_font.render("Press P for next level, R to retry or Q to quit", True, WHITE)
    screen.blit(again, (SCREEN_WIDTH//2 - again.get_width()//2, 250))

def draw_shop():
    global animation_frames, hue_shift
    # Animated rainbow background for shop
    hue_shift += 0.02  # Faster for shop
    if hue_shift > 1:
        hue_shift = 0
    # Rainbow effect: rotate through colors but brighter for shop
    r = int(150 + 100 * abs(math.sin(2 * math.pi * hue_shift)))
    g = int(100 + 150 * abs(math.sin(2 * math.pi * hue_shift + 2)))
    b = int(200 + 50 * abs(math.sin(2 * math.pi * hue_shift + 4)))
    screen.fill((r, g, b))

    # Add some moving particles in shop for atmosphere
    for i in range(10):
        particle_x = int(SCREEN_WIDTH * abs(math.sin(hue_shift + i)) % SCREEN_WIDTH)
        particle_y = int(SCREEN_HEIGHT * abs(math.cos(hue_shift * 2 + i)) % SCREEN_HEIGHT)
        particle_size = 3 + int(math.sin(hue_shift * 3 + i * 0.5) * 2)
        pygame.draw.circle(screen, WHITE + (50,), (particle_x, particle_y), particle_size)

    # Epic shop title with glowing effects
    glow_surface = pygame.Surface((SCREEN_WIDTH, 100))
    glow_surface.fill((r, g, b))
    glow_surface.set_alpha(100)

    for glow_offset in range(5):
        glow_surface.fill((r//2, g//2, b//2))
        glow_surface.set_alpha(50 - glow_offset * 10)
        screen.blit(glow_surface, (0 - glow_offset, 40 - glow_offset * 2))

    title = font.render("EPIC SHOP", True, BLACK)
    title_x = SCREEN_WIDTH//2 - title.get_width()//2
    screen.blit(title, (title_x, 50))

    # Epic coins display with animation
    coins_text = small_font.render(f"💰 EPIC COINS: {coins} 💰", True, WHITE)
    coins_bg = pygame.Surface((coins_text.get_width() + 40, coins_text.get_height() + 10))
    coins_bg.fill(BLACK)
    coins_bg.set_alpha(200)
    screen.blit(coins_bg, (40, 65))
    screen.blit(coins_text, (50, 70))

    # Shop items with enhanced visuals
    y_offset = 100
    item_height = 40
    item_width = 600

    for i, item in enumerate(shop_items):
        if not item["purchased"]:
            # Check mouse hover for items
            mouse_x, mouse_y = pygame.mouse.get_pos()
            item_rect = pygame.Rect(50, y_offset, item_width, item_height)
            is_hovering_item = item_rect.collidepoint(mouse_x, mouse_y)

            # Determine if item is legendary, epic, or normal
            if item.get("cost", 0) >= 1000:
                item_bg_color = (255, 215, 0)  # Legendary - Gold
                border_color = (255, 69, 0)   # Red-Orange
                text_color = BLACK
                rarity_text = "⭐ LEGENDARY ⭐"
            elif item.get("cost", 0) >= 500:
                item_bg_color = (186, 85, 211)  # Epic - Medium Orchid
                border_color = (138, 43, 226)   # Blue Violet
                text_color = WHITE
                rarity_text = "✨ EPIC ✨"
            elif item.get("type") == "new_hero":
                item_bg_color = (255, 105, 180)  # New Hero - Hot Pink
                border_color = (220, 20, 60)     # Crimson
                text_color = BLACK
                rarity_text = "🗡️ HERO 🗡️"
            else:
                item_bg_color = (70, 130, 180)   # Normal - Steel Blue
                border_color = (25, 25, 112)     # Midnight Blue
                text_color = WHITE
                rarity_text = "⬜ NORMAL ⬜"

            # Animated pulsing for epic/legendary items
            if item.get("cost", 0) >= 500:
                pulse_factor = 1 + 0.2 * abs(math.sin(current_time * 0.005 + i))
                final_bg = tuple(min(255, int(c * pulse_factor)) for c in item_bg_color)
            else:
                final_bg = item_bg_color

            # Create item background with glow
            pygame.draw.rect(screen, final_bg, item_rect, border_radius=10)

            # Border and glow effects
            for glow_level in range(3):
                glow_rect = pygame.Rect(50 - glow_level, y_offset - glow_level,
                                      item_width + glow_level * 2, item_height + glow_level * 2)
                glow_alpha = 100 - glow_level * 30
                glow_color = border_color + (glow_alpha,)
                pygame.draw.rect(screen, glow_color, glow_rect, border_radius=10)

            # Enhanced border
            pygame.draw.rect(screen, border_color, item_rect, 3, border_radius=10)

            # Item content
            text_x = 70
            text_y = y_offset + 10

            # Rarity indicator
            rarity_surface = small_font.render(rarity_text, True, text_color)
            screen.blit(rarity_surface, (text_x, text_y))

            # Item name with cost
            item_text = f"{item['name']} - {item['cost']} coins"
            name_surface = small_font.render(item_text, True, text_color)
            screen.blit(name_surface, (text_x, text_y + 20))

            # Highlight cursor on hover
            if is_hovering_item:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                # Add extra glow on hover
                pygame.draw.rect(screen, WHITE + (100,), item_rect, 2, border_radius=10)

            y_offset += item_height + 5  # Adjusted spacing

    # Epic return text with glow
    return_bg = pygame.Surface((300, 40))
    return_bg.fill((150, 200, 255))
    return_bg.set_alpha(150)
    screen.blit(return_bg, (SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT - 50))

    return_text = small_font.render("Press B to go back", True, BLACK)
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
        "- P: Next level after battle",
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
    global animation_frames, damage_text_counter, hue_shift, screen_shake
    # Dynamic background based on game state
    if game_timer.waiting_for_enemy_turn:
        bg_color = (30, 30, 50)  # Dark blue when waiting for enemy
    else:
        hue_shift += 0.01
        if hue_shift > 1:
            hue_shift = 0
        # Rainbow effect: rotate through colors
        r = int(128 + 127 * abs(math.sin(2 * math.pi * hue_shift)))
        g = int(128 + 127 * abs(math.sin(2 * math.pi * hue_shift + 2)))
        b = int(128 + 127 * abs(math.sin(2 * math.pi * hue_shift + 4)))
        bg_color = (r, g, b)

    screen.fill(bg_color)

    if DEBUG_MODE:
        # Debug info at top left
        debug_text = small_font.render(f"Lvl:{current_level} PT:{game_timer.player_turn_count} ET:{game_timer.enemy_turn_count} WT:{game_timer.waiting_for_enemy_turn}", True, WHITE)
        screen.blit(debug_text, (10, 10))
        hero_y = 30
    else:
        hero_y = 10

    if selected_hero is not None and enemy is not None:
        # Draw hero info with glow effect
        for offset in range(3):
            glow_color = tuple(max(0, c - 50) for c in selected_hero.color)
            glow_text = font.render(f"{selected_hero.name} HP: {selected_hero.health} Mana: {selected_hero.mana}", True, glow_color).convert_alpha()
            glow_text.set_alpha(100 - offset * 30)
            screen.blit(glow_text, (10 + offset, hero_y + offset))

        hero_text = font.render(f"{selected_hero.name} HP: {selected_hero.health} Mana: {selected_hero.mana}", True, selected_hero.color)
        screen.blit(hero_text, (10, hero_y))

        # Draw enemy info with glow effect
        for offset in range(3):
            glow_color = tuple(max(0, c - 50) for c in RED)
            glow_text = font.render(f"Enemy HP: {enemy.health} Mana: {enemy.mana}", True, glow_color).convert_alpha()
            glow_text.set_alpha(100 - offset * 30)
            screen.blit(glow_text, (SCREEN_WIDTH//2 + 10 + offset, 10 + offset))

        enemy_text = font.render(f"Enemy HP: {enemy.health} Mana: {enemy.mana}", True, RED)
        screen.blit(enemy_text, (SCREEN_WIDTH//2 + 10, 10))

        # Draw abilities as BIG, HIGHLIGHTED buttons
        global ability_buttons
        global skip_button  # Add global for skip button
        ability_buttons = []
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Check if player can't use any abilities due to mana
        can_use_any_ability = any(selected_hero.mana >= a.get("mana", 0) for a in selected_hero.abilities)

        if not can_use_any_ability:
            skip_button = pygame.Rect(600, SCREEN_HEIGHT - 90, 160, 80)  # Set skip button

            # IMPORTANT: Check if SKIP button is being hovered/clicked DURING drawing
            mouse_x, mouse_y = pygame.mouse.get_pos()
            is_hovering_skip = skip_button.collidepoint(mouse_x, mouse_y)

            # Draw skip button with visual feedback
            skip_bg_color = (150, 150, 255) if is_hovering_skip else (100, 100, 200)
            missing_bg_color = tuple(max(0, c - 30) for c in skip_bg_color)  # Slightly darker for depth

            # Multi-layer glowing border
            for glow_layer in range(3):
                glow_rect = pygame.Rect(600 - glow_layer, SCREEN_HEIGHT - 90 - glow_layer,
                                      160 + glow_layer * 2, 80 + glow_layer * 2)
                glow_alpha = 150 - glow_layer * 40
                if glow_alpha > 0:
                    pygame.draw.rect(screen, skip_bg_color + (glow_alpha,), glow_rect, border_radius=8)

            # Main button fill
            pygame.draw.rect(screen, skip_bg_color, skip_button, border_radius=8)

            # Inner border for 3D effect
            pygame.draw.rect(screen, missing_bg_color, skip_button, border_radius=8, width=1)
            pygame.draw.rect(screen, skip_bg_color, skip_button, border_radius=8, width=3)

            # Highlighted border when hovering
            if is_hovering_skip:
                highlight_color = (255, 255, 100)  # Bright yellow highlight
                pygame.draw.rect(screen, highlight_color, skip_button, border_radius=8, width=4)

            # Enhanced text rendering with multiple effects
            skip_font = pygame.font.SysFont(None, 36) if is_hovering_skip else pygame.font.SysFont(None, 32)
            button_text = "SKIP" if is_hovering_skip else "SKIP"
            sub_text = "TURN" if is_hovering_skip else "TURN"

            # Main text with drop shadow
            text_x = 600 + 160//2
            text_y = SCREEN_HEIGHT - 90 + 80//2

            # Draw centered text with shadow effect
            skip_text = skip_font.render(button_text, True, (255, 255, 255))
            sub_text_render = skip_font.render(sub_text, True, (255, 255, 255))

            # Adjust Y position for two-line text
            total_height = skip_text.get_height() + sub_text_render.get_height() + 2
            start_y = text_y - total_height // 2

            # Draw main "SKIP" text
            main_text_x = text_x - skip_text.get_width() // 2
            main_text_y = start_y

            # Shadow behind text
            shadow_offset = 3
            shadow = skip_font.render(button_text, True, (0, 0, 0, 180)).convert_alpha()
            shadow.set_alpha(180)
            screen.blit(shadow, (main_text_x + shadow_offset, main_text_y + shadow_offset))

            # Glow effect for hovering
            if is_hovering_skip:
                glow = skip_font.render(button_text, True, (255, 255, 150)).convert_alpha()
                glow.set_alpha(100)
                for glow_x, glow_y in [(main_text_x-1, main_text_y), (main_text_x+1, main_text_y),
                                      (main_text_x, main_text_y-1), (main_text_x, main_text_y+1)]:
                    screen.blit(glow, (glow_x, glow_y))

            # Main text
            screen.blit(skip_text, (main_text_x, main_text_y))

            # Draw "TURN" text below
            sub_text_x = text_x - sub_text_render.get_width() // 2
            sub_text_y = start_y + skip_text.get_height() + 2

            # Shadow for "TURN"
            sub_shadow = skip_font.render(sub_text, True, (0, 0, 0, 180)).convert_alpha()
            sub_shadow.set_alpha(180)
            screen.blit(sub_shadow, (sub_text_x + shadow_offset, sub_text_y + shadow_offset))

            # Glow effect for "TURN" when hovering
            if is_hovering_skip:
                sub_glow = skip_font.render(sub_text, True, (255, 255, 150)).convert_alpha()
                sub_glow.set_alpha(100)
                for sub_glow_x, sub_glow_y in [(sub_text_x-1, sub_text_y), (sub_text_x+1, sub_text_y),
                                              (sub_text_x, sub_text_y-1), (sub_text_x, sub_text_y+1)]:
                    screen.blit(sub_glow, (sub_glow_x, sub_glow_y))

            # Main "TURN" text
            screen.blit(sub_text_render, (sub_text_x, sub_text_y))

            # Dynamic cursor for SKIP button interaction
            if is_hovering_skip:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

        else:
            skip_button = None  # Clear skip button if can use abilities

        # Ability box dimensions and positioning
        box_width = 160
        box_height = 80
        button_y = SCREEN_HEIGHT - 90

        for i, ability in enumerate(selected_hero.abilities):
            x = 10 + i * (box_width + 10)  # Spacing between buttons
            y = button_y

            # Check if mouse is hovering over this ability
            button_rect = pygame.Rect(x, y, box_width, box_height)
            ability_buttons.append(button_rect)
            is_hovering = button_rect.collidepoint(mouse_x, mouse_y)

            # Dynamic colors based on state
            has_mana = selected_hero.mana >= ability.get("mana", 0)
            base_color = GREEN if has_mana else DARK_RED

            # Enhanced background colors with pulsing
            if is_hovering and has_mana:
                bg_base = (50, 200, 50)  # Bright green hover
                pulse_factor = 1.2 + 0.3 * math.sin(current_time * 0.01)
            elif animation_button == i:
                bg_base = (255, 255, 100)  # Yellow for selected
                pulse_factor = 1.3
            elif has_mana:
                bg_base = (30, 120, 30)  # Normal available
                pulse_factor = 1.0
            else:
                bg_base = (120, 30, 30)  # No mana available
                pulse_factor = 1.0

            # Pulsing background effect
            bg_color = tuple(min(255, int(c * pulse_factor)) for c in bg_base)
            bg_surface = pygame.Surface((box_width, box_height))
            bg_surface.fill(bg_color)
            bg_surface.set_alpha(200)

            # Draw background with glow layers
            for glow_offset in range(5):
                glow_rect = pygame.Rect(x - glow_offset, y - glow_offset,
                                      box_width + glow_offset * 2, box_height + glow_offset * 2)
                glow_color_alpha = bg_color + (50 - glow_offset * 10,)
                pygame.draw.rect(screen, glow_color_alpha, glow_rect, border_radius=8)

            # Main button background
            pygame.draw.rect(screen, bg_color, button_rect, border_radius=8)

            # Border highlight
            border_thickness = 4 if is_hovering else 2
            border_color = YELLOW if is_hovering and has_mana else WHITE
            pygame.draw.rect(screen, border_color, button_rect, border_thickness, border_radius=8)

            # Large, colorful ability text
            text_font = pygame.font.SysFont(None, 32) if is_hovering else font
            ability_name = ability['name']
            mana_cost = ability.get('mana', 0)

            text_color = WHITE if is_hovering else (YELLOW if has_mana else DARK_RED)

            # Split text into name and cost for better layout
            name_text = text_font.render(ability_name, True, text_color)
            cost_text = text_font.render(f"{mana_cost} mana", True, text_color)

            # Center text in button
            total_width = max(name_text.get_width(), cost_text.get_width())
            start_x = x + (box_width - total_width) // 2
            start_y = y + box_height // 2 - (name_text.get_height() + cost_text.get_height() + 5) // 2

            # Draw name and cost with shadow/outline for better visibility
            shadow_offset = 2
            shadow_color = (0, 0, 0, 180)

            # Text shadow/glow
            for tx, ty in [(start_x - shadow_offset, start_y - shadow_offset),
                          (start_x + shadow_offset, start_y - shadow_offset),
                          (start_x - shadow_offset, start_y + shadow_offset),
                          (start_x + shadow_offset, start_y + shadow_offset)]:
                name_shadow = text_font.render(ability_name, True, shadow_color).convert_alpha()
                name_shadow.set_alpha(128)
                screen.blit(name_shadow, (tx, ty))
                cost_shadow = text_font.render(f"{mana_cost} mana", True, shadow_color).convert_alpha()
                cost_shadow.set_alpha(128)
                screen.blit(cost_shadow, (tx, ty + name_text.get_height() + 5))

            # Main text
            screen.blit(name_text, (start_x, start_y))
            screen.blit(cost_text, (start_x, start_y + name_text.get_height() + 5))

            # Add special effects for certain abilities
            is_powerful = ability_name in ["Lightning", "Charge", "Rapid Fire"]
            is_early_ability = game_timer.player_turn_count < 3

            if is_powerful and is_early_ability:
                # Lock icon for powerful abilities in early turns
                lock_text = text_font.render("LOCKED", True, RED)
                lock_x = x + box_width//2 - lock_text.get_width()//2
                lock_y = y + box_height - lock_text.get_height() - 5
                screen.blit(lock_text, (lock_x, lock_y))

                # Dim the button when locked
                locked_overlay = pygame.Surface((box_width, box_height))
                locked_overlay.fill((0, 0, 0))
                locked_overlay.set_alpha(100)
                screen.blit(locked_overlay, (x, y))

        # Update and draw particles
        particles[:] = [p for p in particles if p.update()]
        for particle in particles:
            particle.draw(screen)

        # Enhanced battle animation
        if animation_frames > 0:
            # Screen shake effect
            if animation_frames > 5:
                screen_shake = random.randint(-5, 5)

            # Central impact animation
            center_x, center_y = SCREEN_WIDTH//2, SCREEN_HEIGHT//2

            # Draw expanding circles with color gradients
            for radius in range(0, animation_frames * 20, 10):
                alpha = max(0, 255 - radius)
                circle_color = tuple(list(selected_hero.color) + [alpha])
                pygame.draw.circle(screen, circle_color, (center_x + screen_shake, center_y), radius, 3)

            # Lightning effects for special attacks
            if animation_button >= 2:  # Assuming powerful abilities are at indices 2+
                for _ in range(5):
                    start_x = random.randint(0, SCREEN_WIDTH)
                    end_x = random.randint(0, SCREEN_WIDTH)
                    lightning_color = YELLOW if random.random() > 0.5 else WHITE
                    pygame.draw.line(screen, lightning_color, (start_x, 0), (end_x, SCREEN_HEIGHT), 2)

            animation_frames -= 1
            if animation_frames <= 0:
                screen_shake = 0
        else:
            screen_shake = 0

        # Animated damage texts with particle trails
        filtered_texts = []
        y_offset = 50
        for text, pos, life in damage_texts:
            if life > 0:
                # Pulse effect
                if life > 50:
                    pulse = 1.0
                else:
                    pulse = 1.0 + 0.3 * abs(math.sin(2 * math.pi * (60 - life) / 60))

                # Create temporary surface for pulsing
                pulse_text = pygame.transform.smoothscale(text,
                    (int(text.get_width() * pulse), int(text.get_height() * pulse)))

                # Rainbow color cycling for text
                text_hue = (hue_shift * 360 + life * 10) % 360
                r = int(128 + 127 * math.sin(math.radians(text_hue)))
                g = int(128 + 127 * math.sin(math.radians(text_hue + 120)))
                b = int(128 + 127 * math.sin(math.radians(text_hue + 240)))

                # Recolor text if it's damage/healing
                if "(weak)" in str(text) or any(word in str(text) for word in ["-", "+"]):
                    pulse_text = pygame.transform.smoothscale(small_font.render(
                        str(text).replace('<pygame.Surface(', '').replace(')>', ''), True, (r, g, b)),
                        (int(text.get_width() * pulse), int(text.get_height() * pulse)))
                    pulse_text = pulse_text.convert_alpha()
                    pulse_text.set_alpha(min(255, life * 4))

                text_x = pos[0] - pulse_text.get_width() // 2 + screen_shake
                text_y = y_offset + abs(math.sin(current_time * 0.01 + y_offset)) * 10

                screen.blit(pulse_text, (text_x, text_y))
                life -= 2  # Faster fade

                if life > 0:
                    filtered_texts.append((text, pos, life))
                else:
                    # Create farewell particles when text fades
                    create_particles(text_x + pulse_text.get_width()//2, text_y + pulse_text.get_height()//2,
                                   (r, g, b), count=15, spread=30, speed=5)

                y_offset += 60  # More spacing for animation

        damage_texts[:] = filtered_texts

        # Apply temporary effects for special game states
        if game_timer.waiting_for_enemy_turn:
            # Pulsing border when waiting for enemy
            border_alpha = int(128 + 127 * math.sin(current_time * 0.008))
            border_color = RED + (border_alpha,)
            pygame.draw.rect(screen, border_color, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 5)

        # Draw current level indicator
        level_text = small_font.render(f"Level {current_level}", True, WHITE)
        level_bg = pygame.Surface((level_text.get_width() + 20, level_text.get_height() + 10))
        level_bg.fill(BLACK)
        level_bg.set_alpha(128)
        screen.blit(level_bg, (SCREEN_WIDTH - level_text.get_width() - 30, 20))
        screen.blit(level_text, (SCREEN_WIDTH - level_text.get_width() - 25, 25))

        # Health/Mana bars with glow effects
        bar_y = hero_y + 35
        # Hero health bar
        total_health = 100 + player_extra_health
        health_ratio = selected_hero.health / total_health
        pygame.draw.rect(screen, RED, (10, bar_y, int(200 * health_ratio), 20))
        pygame.draw.rect(screen, DARK_RED, (10, bar_y, 200, 20), 2)
        # Glow for low health
        if health_ratio < 0.3:
            for offset in range(3):
                glow_rect = pygame.Rect(10 - offset, bar_y - offset, int(200 * health_ratio) + offset * 2, 20 + offset * 2)
                pygame.draw.rect(screen, RED, glow_rect, 1)

        # Hero mana bar
        total_mana = 100 + player_extra_mana
        mana_ratio = selected_hero.mana / total_mana
        mana_y = bar_y + 25
        pygame.draw.rect(screen, BLUE, (10, mana_y, int(200 * mana_ratio), 20))
        pygame.draw.rect(screen, DARK_BLUE, (10, mana_y, 200, 20), 2)

        # Enemy health bar (mirrored style)
        enemy_bar_x = SCREEN_WIDTH - 210
        enemy_health_ratio = enemy.health / enemy.max_health
        pygame.draw.rect(screen, RED, (enemy_bar_x, 45, int(200 * enemy_health_ratio), 20))
        pygame.draw.rect(screen, DARK_RED, (enemy_bar_x, 45, 200, 20), 2)

        # Enemy mana bar
        enemy_mana_ratio = enemy.mana / 50
        enemy_mana_y = 70
        pygame.draw.rect(screen, BLUE, (enemy_bar_x, enemy_mana_y, int(200 * enemy_mana_ratio), 20))
        pygame.draw.rect(screen, DARK_BLUE, (enemy_bar_x, enemy_mana_y, 200, 20), 2)

def create_particles(x, y, color, count=8, spread=50, speed=3):
    """Create particle effects for attacks/healing"""
    for _ in range(count):
        dx = random.uniform(-speed, speed)
        dy = random.uniform(-speed, speed)
        particles.append(Particle(x + random.uniform(-spread, spread),
                                y + random.uniform(-spread, spread), color, dx, dy))

# Initialize global variables
current_level = 1
coins = 0
player_extra_health = 0
player_extra_mana = 0
unlocked_abilities = {}
bought_mercenaries = []
shop_items = default_shop_items.copy()

# Save flags to prevent continuous saving
save_flags = {'win': False, 'lose': False, 'tie': False, 'final_win': False}

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
    game_timer.enemy_turn_count += 1

    if enemy.health > 0 and selected_hero.health > 0:
        # Enemy chooses random ability
        ability_index = random.randint(0, len(enemy.abilities) - 1)
        ability = enemy.abilities[ability_index]

        # Prevent Special ability from being used in first 2 turns
        if ability.get("name") == "Special" and game_timer.enemy_turn_count < 3:
            # Force Attack instead
            ability = enemy.abilities[0]  # Attack is index 0

        if ability.get("name") == "Heal" and enemy.mana >= 5 and enemy.health < enemy.max_health:
            enemy.mana -= 5
            heal_amount = ability["heal"]
            enemy.health = min(enemy.health + heal_amount, enemy.max_health)
            damage_texts.append((small_font.render(f"Enemy healed {heal_amount}", True, BLUE), [600, 200], 60))
        else:
            # Reduce damage if mercenaries are bought
            damage_reduction = len(bought_mercenaries) * 0.1
            if "damage" in ability:
                reduced_damage = ability["damage"] * (1 - damage_reduction)
                selected_hero.health -= reduced_damage
                damage_texts.append((small_font.render(f"Enemy {ability.get('name', 'Attack')}: -{int(reduced_damage)}", True, RED), [200, 200], 60))
            else:
                # If no damage key, treat as a special attack with base damage
                reduced_damage = (10 + current_level * 2) * (1 - damage_reduction)
                selected_hero.health -= reduced_damage
                damage_texts.append((small_font.render(f"Enemy {ability.get('name', 'Special')}: -{int(reduced_damage)}", True, RED), [200, 200], 60))

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
    global selected_hero, enemy, hero_buttons, ability_buttons, animation_frames, animation_button, damage_texts, game_state, save_flags
    selected_hero = None
    enemy = None
    hero_buttons = []
    ability_buttons = []
    animation_frames = 0
    animation_button = -1
    damage_texts = []
    game_timer.last_enemy_turn = 0
    game_timer.enemy_turn_count = 0
    game_timer.player_turn_count = 0
    game_timer.waiting_for_enemy_turn = False
    game_state = WELCOME

    # Reset save flags for new game
    save_flags = {'win': False, 'lose': False, 'tie': False, 'final_win': False}

    # Main loop
while running:
    clock.tick(60)
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # Common keys that work in any state
            if event.key == pygame.K_q:
                running = False
            elif event.key == pygame.K_d and not DEBUG_MODE:
                DEBUG_MODE = True
                print("DEBUG MODE: ON")
            elif event.key == pygame.K_d and DEBUG_MODE:
                DEBUG_MODE = False
                print("DEBUG MODE: OFF")
            elif game_state == WELCOME:
                game_state = SELECTION
                load_game()
            elif game_state == SELECTION and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    game_state = SHOP
                    play_background_music('shop')
                elif event.key == pygame.K_b:
                    game_state = SELECTION
            elif game_state == SHOP and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    game_state = SELECTION
            elif game_state == WIN and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    current_level += 1
                    coins += 30
                    reset_game()
                    if current_level > 20:
                        game_state = FINAL_WIN
                    else:
                        game_state = SELECTION
                    # Reset save flags after restart
                    save_flags = {'win': False, 'lose': False, 'tie': False, 'final_win': False}
                elif event.key == pygame.K_r:
                    reset_game()
                    save_flags = {'win': False, 'lose': False, 'tie': False, 'final_win': False}
            elif game_state in [LOSE, TIE, FINAL_WIN] and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    if game_state == WIN:
                        current_level += 1
                        coins += 30
                    elif game_state == TIE:
                        coins += 15
                    elif game_state == LOSE:
                        current_level = 1
                    elif game_state == FINAL_WIN:
                        pass
                    reset_game()
                    if current_level > 20:
                        game_state = FINAL_WIN
                    else:
                        game_state = SELECTION
                    # Reset save flags after restart
                    save_flags = {'win': False, 'lose': False, 'tie': False, 'final_win': False}
                elif event.key == pygame.K_p and game_state == TIE:
                    # Allow P key in TIE state for progression (but no rewards in tie)
                    current_level += 1
                    reset_game()
                    if current_level > 20:
                        game_state = FINAL_WIN
                    else:
                        game_state = SELECTION
                    save_flags = {'win': False, 'lose': False, 'tie': False, 'final_win': False}
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if game_state == SELECTION:
                for i, button in enumerate(hero_buttons):
                    if button.collidepoint(mouse_x, mouse_y):
                        selected_hero = Hero(HEROES[i])
                        enemy = Enemy(current_level)
                        game_state = BATTLE
                        # Reset turn counts for new battle
                        game_timer.enemy_turn_count = 0
                        game_timer.player_turn_count = 0
                        break
            elif game_state == BATTLE:
                # Check skip button first if available
                skip_clicked = False
                if skip_button is not None and skip_button.collidepoint(mouse_x, mouse_y):
                    # Skip turn - directly trigger TIE since you can't use any abilities
                    game_state = TIE
                    coins += 15
                    skip_clicked = True

                if not skip_clicked:
                    for i, button in enumerate(ability_buttons):
                        if button.collidepoint(mouse_x, mouse_y):
                            ability = selected_hero.abilities[i]
                            mana_cost = ability.get("mana", 0)
                            if selected_hero.mana >= mana_cost:
                                selected_hero.mana -= mana_cost
                                game_timer.player_turn_count += 1

                                # Check if player can use powerful abilities
                                is_powerful_ability = (ability["name"] in ["Lightning", "Charge", "Rapid Fire"])

                                # Prevent powerful abilities from being used in first 2 turns - completely locked
                                if is_powerful_ability and game_timer.player_turn_count < 3:
                                    # Cannot use powerful abilities yet - show message and continue without turn
                                    damage_texts.append((small_font.render(f"{ability['name']} LOCKED! Available after turn 3", True, RED), [400, 300], 60))
                                    continue  # Skip the ability, don't use turn

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
                                        # Start timer for enemy turn (after damage abilities only)
                                        game_timer.last_enemy_turn = current_time + game_timer.ENEMY_TURN_DELAY
                                        game_timer.waiting_for_enemy_turn = True
                                elif "heal" in ability:
                                    heal_amount = ability["heal"]
                                    selected_hero.health = min(selected_hero.health + heal_amount, 100 + player_extra_health)
                                    damage_texts.append((small_font.render(f"{ability['name']}: +{heal_amount}", True, BLUE), [200, 200], 60))
                                    # Healing abilities don't trigger enemy turns
                                    continue
                            else:
                                # Not enough mana - show message
                                damage_texts.append((small_font.render("Not enough mana!", True, RED), [400, 300], 60))
                            break
            elif game_state == SHOP:
                # Shop item purchasing by mouse click
                y_offset = 100
                for i, item in enumerate(shop_items):
                    if not item["purchased"]:
                        text_rect = pygame.Rect(50, y_offset, 400, 30)
                        if text_rect.collidepoint(mouse_x, mouse_y):
                            purchase_item(i)
                        y_offset += 30

    # Enemy AI timing - ONLY trigger after player action
    if game_state == BATTLE and selected_hero is not None and enemy is not None and game_timer.waiting_for_enemy_turn:
        if current_time - game_timer.last_enemy_turn > game_timer.ENEMY_TURN_DELAY:
            if enemy.health > 0 and selected_hero.health > 0:
                enemy_turn()
                game_timer.last_enemy_turn = current_time
                game_timer.waiting_for_enemy_turn = False

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
