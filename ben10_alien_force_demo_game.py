"""
Ben 10: Alien Force - Demo Game
A playable demo showcasing the game features with main menu, tutorial, and demo mode.
"""

from ursina import *
import random
import math

# Initialize the app
app = Ursina()

# Window settings
window.title = "Ben 10: Alien Force - DEMO"
window.borderless = False
window.fullscreen = False
window.exit_button.visible = False
window.fps_counter.enabled = False

# ==================== GAME CONSTANTS ====================

# Colors
SKY_BLUE = color.rgb(135, 206, 235)
GRASS_GREEN = color.rgb(124, 185, 72)
DARK_GREEN = color.rgb(34, 139, 34)
BEN_GREEN = color.rgb(0, 200, 0)
BEN_BLACK = color.rgb(20, 20, 20)
ROCK_GRAY = color.rgb(128, 128, 128)
CAVE_GRAY = color.rgb(80, 80, 80)
MENU_BG = color.rgba(20, 25, 30, 250)
BUTTON_COLOR = color.rgb(50, 180, 50)
BUTTON_HOVER = color.rgb(70, 220, 70)

# ==================== GAME STATE ====================

class GameState:
    def __init__(self):
        self.reset()
        self.current_screen = "menu"  # menu, tutorial, game, demo
        self.demo_mode = False
        self.tutorial_step = 0
        self.demo_timer = 0
    
    def reset(self):
        self.level = 1
        self.max_health = 5
        self.current_health = 5
        self.enemies_defeated = 0
        self.game_over = False
        self.victory = False
        self.score = 0
        self.combo = 0
        self.combo_timer = 0

game_state = GameState()

# ==================== ENVIRONMENT ====================

# Sky
camera.clip_plane_far = 1000
sky = Sky(color=SKY_BLUE)

# Ground
ground = Entity(
    model='plane',
    scale=(100, 1, 100),
    color=GRASS_GREEN,
    texture='white_cube',
    texture_scale=(50, 50),
    collider='box',
    enabled=False
)

# Environment objects lists
trees = []
rocks = []
cave = None
van = None
watchtower = None

def create_tree(position):
    tree_group = Entity(position=position)
    
    trunk = Entity(
        parent=tree_group,
        model='cube',
        scale=(0.3, 1.5, 0.3),
        color=color.rgb(101, 67, 33),
        position=(0, 0.75, 0)
    )
    
    for i, (y, s) in enumerate([(1.8, 1.2), (2.4, 0.9), (3.0, 0.6)]):
        foliage = Entity(
            parent=tree_group,
            model='cone',
            scale=(s, 0.8, s),
            color=DARK_GREEN,
            position=(0, y, 0)
        )
    
    return tree_group

def create_rock(position, scale=1):
    rock = Entity(
        model='sphere',
        scale=(scale * 0.8, scale * 0.5, scale * 0.7),
        color=ROCK_GRAY,
        position=position,
        rotation=(random.randint(0, 30), random.randint(0, 360), random.randint(0, 20))
    )
    return rock

def create_cave():
    cave_group = Entity(position=(-6, 0, 12))
    
    cave_body = Entity(
        parent=cave_group,
        model='sphere',
        scale=(4, 3, 3),
        color=CAVE_GRAY,
        position=(0, 1.5, 0)
    )
    
    cave_entrance = Entity(
        parent=cave_group,
        model='sphere',
        scale=(1.5, 2, 0.5),
        color=color.rgb(30, 30, 30),
        position=(0, 1, 1.5)
    )
    
    for i in range(5):
        angle = random.uniform(0, math.pi)
        x = math.cos(angle) * 2
        y = 0.5 + random.uniform(0, 2)
        detail = Entity(
            parent=cave_group,
            model='sphere',
            scale=(0.8, 0.6, 0.7),
            color=color.rgb(100, 100, 100),
            position=(x, y, 0.5)
        )
    
    return cave_group

def create_van():
    van_group = Entity(position=(-10, 0, 3), rotation=(0, 45, 0))
    
    van_body = Entity(
        parent=van_group,
        model='cube',
        scale=(2, 1.5, 3.5),
        color=BEN_GREEN,
        position=(0, 1, 0)
    )
    
    van_cabin = Entity(
        parent=van_group,
        model='cube',
        scale=(1.8, 1, 1.2),
        color=BEN_GREEN,
        position=(0, 2, -0.8)
    )
    
    windshield = Entity(
        parent=van_group,
        model='cube',
        scale=(1.5, 0.6, 0.1),
        color=color.rgb(150, 200, 255),
        position=(0, 2.1, -1.45)
    )
    
    wheel_positions = [(-1, 0.3, 1), (1, 0.3, 1), (-1, 0.3, -1), (1, 0.3, -1)]
    for wx, wy, wz in wheel_positions:
        wheel = Entity(
            parent=van_group,
            model='cylinder',
            scale=(0.5, 0.2, 0.5),
            color=BEN_BLACK,
            position=(wx, wy, wz),
            rotation=(0, 0, 90)
        )
    
    dish_base = Entity(
        parent=van_group,
        model='cube',
        scale=(0.3, 0.8, 0.3),
        color=color.rgb(80, 80, 80),
        position=(0.5, 2.5, 0.5)
    )
    
    dish = Entity(
        parent=van_group,
        model='sphere',
        scale=(0.8, 0.4, 0.8),
        color=color.rgb(200, 200, 200),
        position=(0.5, 3.1, 0.5)
    )
    
    warning_light = Entity(
        parent=van_group,
        model='cube',
        scale=(0.4, 0.2, 0.6),
        color=color.rgb(255, 165, 0),
        position=(-0.5, 2.6, 0.5)
    )
    
    return van_group

def create_watchtower():
    tower_group = Entity(position=(12, 0, 6))
    
    leg_positions = [(-1, 0, -1), (1, 0, -1), (-1, 0, 1), (1, 0, 1)]
    for lx, ly, lz in leg_positions:
        leg = Entity(
            parent=tower_group,
            model='cube',
            scale=(0.3, 8, 0.3),
            color=BEN_GREEN,
            position=(lx * 0.7, 4, lz * 0.7),
            rotation=(lx * 5, 0, lz * 5)
        )
    
    platform = Entity(
        parent=tower_group,
        model='cube',
        scale=(3, 0.3, 3),
        color=color.rgb(101, 67, 33),
        position=(0, 7, 0)
    )
    
    cabin = Entity(
        parent=tower_group,
        model='cube',
        scale=(2.5, 2, 2.5),
        color=BEN_GREEN,
        position=(0, 8.2, 0)
    )
    
    roof = Entity(
        parent=tower_group,
        model='cone',
        scale=(2, 1, 2),
        color=color.rgb(101, 67, 33),
        position=(0, 9.7, 0)
    )
    
    for angle in [0, 90, 180, 270]:
        rad = math.radians(angle)
        wx = math.sin(rad) * 1.3
        wz = math.cos(rad) * 1.3
        window = Entity(
            parent=tower_group,
            model='cube',
            scale=(0.8, 0.6, 0.1),
            color=color.rgb(150, 200, 255),
            position=(wx, 8.4, wz),
            rotation=(0, angle, 0)
        )
    
    return tower_group

def setup_environment():
    global trees, rocks, cave, van, watchtower
    
    ground.enabled = True
    
    tree_positions = [
        (12, 0, 8), (15, 0, 5), (18, 0, 10),
        (14, 0, 12), (-15, 0, 10), (-18, 0, 8),
        (20, 0, -5), (-12, 0, -8), (8, 0, 15),
        (-20, 0, 15), (25, 0, 3), (-25, 0, -3)
    ]
    trees = [create_tree(pos) for pos in tree_positions]
    
    rock_positions = [
        (-5, 0.2, 3, 0.8), (6, 0.15, -2, 0.5), (-8, 0.2, -5, 0.7),
        (10, 0.15, 2, 0.4), (-3, 0.18, 8, 0.6), (4, 0.12, 10, 0.35),
        (15, 0.2, -8, 0.9), (-12, 0.15, 5, 0.5)
    ]
    rocks = [create_rock((x, y, z), s) for x, y, z, s in rock_positions]
    
    cave = create_cave()
    van = create_van()
    watchtower = create_watchtower()

def cleanup_environment():
    global trees, rocks, cave, van, watchtower
    
    ground.enabled = False
    
    for tree in trees:
        destroy(tree)
    trees = []
    
    for rock in rocks:
        destroy(rock)
    rocks = []
    
    if cave:
        destroy(cave)
        cave = None
    if van:
        destroy(van)
        van = None
    if watchtower:
        destroy(watchtower)
        watchtower = None

# ==================== PLAYER ====================

class Player(Entity):
    def __init__(self):
        super().__init__()
        self.position = (0, 0, -5)
        self.rotation_y = 0
        self.speed = 5
        self.attack_cooldown = 0
        self.is_attacking = False
        self.enabled = False
        
        # Body
        self.body = Entity(
            parent=self,
            model='cube',
            scale=(0.6, 0.8, 0.4),
            color=BEN_BLACK,
            position=(0, 1.2, 0)
        )
        
        # Green stripe
        self.stripe = Entity(
            parent=self,
            model='cube',
            scale=(0.62, 0.2, 0.42),
            color=BEN_GREEN,
            position=(0, 1.2, 0)
        )
        
        # Head
        self.head = Entity(
            parent=self,
            model='sphere',
            scale=(0.5, 0.5, 0.5),
            color=color.rgb(255, 220, 177),
            position=(0, 1.9, 0)
        )
        
        # Hair
        self.hair = Entity(
            parent=self,
            model='cube',
            scale=(0.55, 0.3, 0.55),
            color=color.rgb(101, 67, 33),
            position=(0, 2.15, 0)
        )
        
        # Legs
        self.left_leg = Entity(
            parent=self,
            model='cube',
            scale=(0.25, 0.6, 0.25),
            color=color.rgb(107, 142, 35),
            position=(-0.15, 0.5, 0)
        )
        
        self.right_leg = Entity(
            parent=self,
            model='cube',
            scale=(0.25, 0.6, 0.25),
            color=color.rgb(107, 142, 35),
            position=(0.15, 0.5, 0)
        )
        
        # Arms
        self.left_arm = Entity(
            parent=self,
            model='cube',
            scale=(0.2, 0.5, 0.2),
            color=color.rgb(255, 220, 177),
            position=(-0.4, 1.1, 0)
        )
        
        self.right_arm = Entity(
            parent=self,
            model='cube',
            scale=(0.2, 0.5, 0.2),
            color=color.rgb(255, 220, 177),
            position=(0.4, 1.1, 0)
        )
        
        # Omnitrix
        self.omnitrix = Entity(
            parent=self,
            model='cube',
            scale=(0.15, 0.15, 0.15),
            color=BEN_GREEN,
            position=(-0.4, 0.9, 0)
        )
    
    def update(self):
        if not self.enabled or game_state.game_over or game_state.victory:
            return
        
        if game_state.demo_mode:
            self.demo_ai()
        else:
            self.handle_input()
        
        # Attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= time.dt
        
        # Combo timer
        if game_state.combo_timer > 0:
            game_state.combo_timer -= time.dt
        else:
            game_state.combo = 0
    
    def handle_input(self):
        move_direction = Vec3(0, 0, 0)
        
        if held_keys['w'] or held_keys['up arrow']:
            move_direction += Vec3(0, 0, 1)
        if held_keys['s'] or held_keys['down arrow']:
            move_direction += Vec3(0, 0, -1)
        if held_keys['a'] or held_keys['left arrow']:
            move_direction += Vec3(-1, 0, 0)
        if held_keys['d'] or held_keys['right arrow']:
            move_direction += Vec3(1, 0, 0)
        
        self.move(move_direction)
    
    def demo_ai(self):
        """AI control for demo mode"""
        if len(enemies) > 0:
            # Find nearest enemy
            nearest = min(enemies, key=lambda e: distance(self.position, e.position))
            direction = nearest.position - self.position
            direction.y = 0
            
            dist = direction.length()
            
            if dist > 1.8:
                self.move(direction.normalized())
            else:
                self.attack()
        else:
            # Wander around
            game_state.demo_timer += time.dt
            angle = game_state.demo_timer * 0.5
            target = Vec3(math.sin(angle) * 5, 0, math.cos(angle) * 5)
            direction = target - self.position
            direction.y = 0
            if direction.length() > 0.5:
                self.move(direction.normalized())
    
    def move(self, direction):
        if direction.length() > 0:
            direction = direction.normalized()
            self.position += direction * self.speed * time.dt
            self.rotation_y = math.degrees(math.atan2(direction.x, direction.z))
            
            # Walk animation
            walk_cycle = math.sin(time.time() * 10) * 15
            self.left_leg.rotation_x = walk_cycle
            self.right_leg.rotation_x = -walk_cycle
            self.left_arm.rotation_x = -walk_cycle * 0.5
            self.right_arm.rotation_x = walk_cycle * 0.5
        else:
            self.left_leg.rotation_x = 0
            self.right_leg.rotation_x = 0
            self.left_arm.rotation_x = 0
            self.right_arm.rotation_x = 0
        
        # Keep in bounds
        self.x = clamp(self.x, -40, 40)
        self.z = clamp(self.z, -40, 40)
    
    def attack(self):
        if self.attack_cooldown <= 0:
            self.attack_cooldown = 0.5
            self.is_attacking = True
            
            # Attack animation
            self.right_arm.animate_rotation_x(-90, duration=0.1)
            invoke(lambda: self.right_arm.animate_rotation_x(0, duration=0.2), delay=0.15)
            
            # Check hits
            hit_any = False
            for enemy in enemies[:]:
                dist = distance(self.position, enemy.position)
                if dist < 2:
                    enemy.take_damage(1)
                    hit_any = True
            
            if hit_any:
                game_state.combo += 1
                game_state.combo_timer = 2.0
                game_state.score += 100 * game_state.combo
                update_score_display()
            
            invoke(setattr, self, 'is_attacking', False, delay=0.3)
    
    def reset(self):
        self.position = (0, 0, -5)
        self.rotation_y = 0
        self.attack_cooldown = 0
        self.is_attacking = False

player = Player()

# ==================== ENEMY ====================

class Enemy(Entity):
    def __init__(self, position):
        super().__init__()
        self.position = position
        self.speed = 2
        self.health = 2
        self.attack_cooldown = 0
        self.is_alive = True
        
        # Body
        self.body = Entity(
            parent=self,
            model='sphere',
            scale=(0.5, 0.7, 0.4),
            color=color.rgb(100, 100, 100),
            position=(0, 0.8, 0)
        )
        
        # Head
        self.head = Entity(
            parent=self,
            model='sphere',
            scale=(0.4, 0.4, 0.35),
            color=color.rgb(120, 120, 120),
            position=(0, 1.4, 0)
        )
        
        # Eyes
        self.left_eye = Entity(
            parent=self,
            model='sphere',
            scale=(0.15, 0.2, 0.1),
            color=color.rgb(200, 50, 50),
            position=(-0.12, 1.45, 0.15)
        )
        
        self.right_eye = Entity(
            parent=self,
            model='sphere',
            scale=(0.15, 0.2, 0.1),
            color=color.rgb(200, 50, 50),
            position=(0.12, 1.45, 0.15)
        )
        
        # Arms
        self.left_arm = Entity(
            parent=self,
            model='cube',
            scale=(0.15, 0.5, 0.15),
            color=color.rgb(90, 90, 90),
            position=(-0.35, 0.9, 0)
        )
        
        self.right_arm = Entity(
            parent=self,
            model='cube',
            scale=(0.15, 0.5, 0.15),
            color=color.rgb(90, 90, 90),
            position=(0.35, 0.9, 0)
        )
        
        # Legs
        self.left_leg = Entity(
            parent=self,
            model='cube',
            scale=(0.18, 0.4, 0.18),
            color=color.rgb(80, 80, 80),
            position=(-0.15, 0.35, 0)
        )
        
        self.right_leg = Entity(
            parent=self,
            model='cube',
            scale=(0.18, 0.4, 0.18),
            color=color.rgb(80, 80, 80),
            position=(0.15, 0.35, 0)
        )
    
    def update(self):
        if not self.is_alive or game_state.game_over or game_state.victory:
            return
        
        # Move towards player
        direction = player.position - self.position
        direction.y = 0
        
        if direction.length() > 0.1:
            direction = direction.normalized()
            self.position += direction * self.speed * time.dt
            self.rotation_y = math.degrees(math.atan2(direction.x, direction.z))
            
            walk_cycle = math.sin(time.time() * 8) * 20
            self.left_leg.rotation_x = walk_cycle
            self.right_leg.rotation_x = -walk_cycle
        
        # Attack
        dist = distance(self.position, player.position)
        if dist < 1.5 and self.attack_cooldown <= 0:
            self.attack_player()
        
        if self.attack_cooldown > 0:
            self.attack_cooldown -= time.dt
    
    def attack_player(self):
        self.attack_cooldown = 1.5
        game_state.current_health -= 1
        game_state.combo = 0  # Reset combo when hit
        update_health_display()
        
        player.body.color = color.red
        invoke(setattr, player.body, 'color', BEN_BLACK, delay=0.2)
        
        if game_state.current_health <= 0:
            trigger_game_over()
    
    def take_damage(self, damage):
        self.health -= damage
        
        self.body.color = color.white
        invoke(setattr, self.body, 'color', color.rgb(100, 100, 100), delay=0.1)
        
        if self.health <= 0:
            self.die()
    
    def die(self):
        self.is_alive = False
        game_state.enemies_defeated += 1
        game_state.score += 500
        update_score_display()
        
        self.animate_scale(0, duration=0.3)
        destroy(self, delay=0.3)
        enemies.remove(self)
        
        if len(enemies) == 0:
            trigger_victory()

enemies = []

def spawn_enemies():
    global enemies
    enemy_positions = [
        (0, 0, 8),
        (5, 0, 10),
        (-5, 0, 12)
    ]
    
    for pos in enemy_positions:
        enemy = Enemy(pos)
        enemies.append(enemy)

def clear_enemies():
    global enemies
    for enemy in enemies[:]:
        destroy(enemy)
    enemies.clear()

# ==================== UI COMPONENTS ====================

# --- Main Menu UI ---
menu_container = Entity(parent=camera.ui, enabled=True)

menu_bg = Entity(
    parent=menu_container,
    model='quad',
    scale=(2, 2),
    color=MENU_BG,
    z=0.1
)

# Title
menu_title = Text(
    text="BEN 10",
    parent=menu_container,
    position=(0, 0.35),
    origin=(0, 0),
    scale=5,
    color=BEN_GREEN
)

menu_subtitle = Text(
    text="ALIEN FORCE",
    parent=menu_container,
    position=(0, 0.25),
    origin=(0, 0),
    scale=2.5,
    color=color.white
)

menu_demo_label = Text(
    text="~ DEMO VERSION ~",
    parent=menu_container,
    position=(0, 0.17),
    origin=(0, 0),
    scale=1.2,
    color=color.yellow
)

# Menu Buttons
class MenuButton(Button):
    def __init__(self, text, y_pos, action):
        super().__init__(
            text=text,
            parent=menu_container,
            scale=(0.4, 0.08),
            position=(0, y_pos),
            color=BUTTON_COLOR,
            highlight_color=BUTTON_HOVER,
            pressed_color=color.rgb(30, 150, 30)
        )
        self.action = action
        self.text_entity.scale = 0.8
    
    def on_click(self):
        self.action()

btn_play = MenuButton("▶  PLAY GAME", 0.0, lambda: start_game(False))
btn_demo = MenuButton("🎬  WATCH DEMO", -0.12, lambda: start_game(True))
btn_tutorial = MenuButton("📖  TUTORIAL", -0.24, show_tutorial)
btn_quit = MenuButton("✕  QUIT", -0.36, application.quit)

menu_instructions = Text(
    text="Use WASD to move, SPACE to attack",
    parent=menu_container,
    position=(0, -0.45),
    origin=(0, 0),
    scale=0.9,
    color=color.rgb(150, 150, 150)
)

# --- Tutorial UI ---
tutorial_container = Entity(parent=camera.ui, enabled=False)

tutorial_bg = Entity(
    parent=tutorial_container,
    model='quad',
    scale=(1.2, 0.8),
    color=color.rgba(20, 20, 30, 240),
    position=(0, 0)
)

tutorial_title = Text(
    text="TUTORIAL",
    parent=tutorial_container,
    position=(0, 0.28),
    origin=(0, 0),
    scale=2.5,
    color=BEN_GREEN
)

tutorial_texts = [
    "Welcome to Ben 10: Alien Force!\n\nYou play as Ben Tennyson, equipped with\nthe powerful Omnitrix.",
    "MOVEMENT\n\nUse W, A, S, D keys or Arrow Keys\nto move Ben around the battlefield.",
    "COMBAT\n\nPress SPACE to attack nearby enemies.\nGet close to them and strike!",
    "COMBOS\n\nHit enemies quickly to build combos!\nHigher combos = More points!",
    "OBJECTIVE\n\nDefeat all alien enemies to win.\nDon't let your health reach zero!",
    "You're ready!\n\nGood luck, hero!"
]

tutorial_content = Text(
    text=tutorial_texts[0],
    parent=tutorial_container,
    position=(0, 0.05),
    origin=(0, 0),
    scale=1.2,
    color=color.white
)

tutorial_progress = Text(
    text="1 / 6",
    parent=tutorial_container,
    position=(0, -0.25),
    origin=(0, 0),
    scale=1,
    color=color.rgb(150, 150, 150)
)

tutorial_hint = Text(
    text="Press SPACE to continue, ESC to return",
    parent=tutorial_container,
    position=(0, -0.32),
    origin=(0, 0),
    scale=0.8,
    color=color.yellow
)

# --- Game UI ---
game_ui_container = Entity(parent=camera.ui, enabled=False)

# Level/Health Panel
ui_panel = Entity(
    parent=game_ui_container,
    model='quad',
    scale=(0.24, 0.13),
    color=color.rgba(205, 190, 160, 245),
    position=(-0.76, 0.42),
    origin=(-0.5, 0.5)
)

level_text = Text(
    text="Level: 1",
    parent=game_ui_container,
    position=(-0.74, 0.40),
    scale=1.6,
    color=color.rgb(30, 30, 30)
)

health_label = Text(
    text="Health:",
    parent=game_ui_container,
    position=(-0.74, 0.36),
    scale=1.3,
    color=color.rgb(30, 30, 30)
)

health_bar_bg = Entity(
    parent=game_ui_container,
    model='quad',
    scale=(0.12, 0.022),
    color=color.rgb(50, 50, 50),
    position=(-0.67, 0.335),
    origin=(-0.5, 0)
)

health_bar = Entity(
    parent=game_ui_container,
    model='quad',
    scale=(0.12, 0.022),
    color=color.rgb(80, 200, 80),
    position=(-0.67, 0.335),
    origin=(-0.5, 0)
)

health_text = Text(
    text="5/5",
    parent=game_ui_container,
    position=(-0.53, 0.34),
    scale=1.2,
    color=color.rgb(30, 30, 30)
)

# Score Panel
score_panel = Entity(
    parent=game_ui_container,
    model='quad',
    scale=(0.2, 0.08),
    color=color.rgba(30, 30, 40, 220),
    position=(0.7, 0.42),
    origin=(0.5, 0.5)
)

score_label = Text(
    text="SCORE",
    parent=game_ui_container,
    position=(0.72, 0.405),
    origin=(1, 0),
    scale=0.9,
    color=color.yellow
)

score_text = Text(
    text="0",
    parent=game_ui_container,
    position=(0.72, 0.37),
    origin=(1, 0),
    scale=1.5,
    color=color.white
)

combo_text = Text(
    text="",
    parent=game_ui_container,
    position=(0, 0.25),
    origin=(0, 0),
    scale=2,
    color=color.orange,
    enabled=False
)

# Objective Panel
objective_panel = Entity(
    parent=game_ui_container,
    model='quad',
    scale=(0.26, 0.095),
    color=color.rgba(30, 32, 35, 250),
    position=(-0.76, -0.42),
    origin=(-0.5, -0.5)
)

objective_accent = Entity(
    parent=game_ui_container,
    model='quad',
    scale=(0.006, 0.075),
    color=color.rgb(180, 60, 60),
    position=(-0.755, -0.395),
    origin=(-0.5, 0)
)

objective_title = Text(
    text="OBJECTIVE:",
    parent=game_ui_container,
    position=(-0.74, -0.355),
    scale=1.0,
    color=color.rgb(255, 200, 50)
)

omnitrix_circle = Entity(
    parent=game_ui_container,
    model='circle',
    scale=(0.028, 0.028),
    color=color.rgb(50, 180, 50),
    position=(-0.73, -0.395)
)

objective_text = Text(
    text="Defeat the enemy!",
    parent=game_ui_container,
    position=(-0.695, -0.395),
    scale=1.0,
    color=color.white
)

# Demo Mode Indicator
demo_indicator = Text(
    text="🎬 DEMO MODE - Press ESC to return to menu",
    parent=game_ui_container,
    position=(0, 0.45),
    origin=(0, 0),
    scale=1,
    color=color.yellow,
    enabled=False
)

# Result screens
result_panel = Entity(
    parent=game_ui_container,
    model='quad',
    scale=(0.6, 0.4),
    color=color.rgba(20, 20, 30, 240),
    position=(0, 0),
    enabled=False
)

result_text = Text(
    text="",
    parent=game_ui_container,
    position=(0, 0.08),
    origin=(0, 0),
    scale=3,
    color=color.white,
    enabled=False
)

result_score = Text(
    text="",
    parent=game_ui_container,
    position=(0, -0.02),
    origin=(0, 0),
    scale=1.5,
    color=color.yellow,
    enabled=False
)

restart_text = Text(
    text="Press R to restart or ESC for menu",
    parent=game_ui_container,
    position=(0, -0.1),
    origin=(0, 0),
    scale=1.2,
    color=color.white,
    enabled=False
)

# ==================== UI UPDATE FUNCTIONS ====================

def update_health_display():
    health_ratio = game_state.current_health / game_state.max_health
    health_bar.scale_x = 0.12 * health_ratio
    health_text.text = f"{game_state.current_health}/{game_state.max_health}"
    
    if game_state.current_health <= 2:
        health_bar.color = color.rgb(220, 60, 60)
    elif game_state.current_health <= 3:
        health_bar.color = color.rgb(220, 180, 50)
    else:
        health_bar.color = color.rgb(80, 200, 80)

def update_score_display():
    score_text.text = str(game_state.score)
    
    if game_state.combo > 1:
        combo_text.text = f"COMBO x{game_state.combo}!"
        combo_text.enabled = True
        combo_text.animate_scale(2.2, duration=0.1)
        invoke(lambda: combo_text.animate_scale(2, duration=0.1), delay=0.1)
    else:
        combo_text.enabled = False

# ==================== GAME FLOW FUNCTIONS ====================

def show_menu():
    game_state.current_screen = "menu"
    menu_container.enabled = True
    tutorial_container.enabled = False
    game_ui_container.enabled = False
    
    cleanup_environment()
    clear_enemies()
    player.enabled = False
    
    camera.position = (0, 5, -10)
    camera.rotation_x = 15

def show_tutorial():
    game_state.current_screen = "tutorial"
    game_state.tutorial_step = 0
    
    menu_container.enabled = False
    tutorial_container.enabled = True
    game_ui_container.enabled = False
    
    update_tutorial_text()

def update_tutorial_text():
    tutorial_content.text = tutorial_texts[game_state.tutorial_step]
    tutorial_progress.text = f"{game_state.tutorial_step + 1} / {len(tutorial_texts)}"

def next_tutorial_step():
    game_state.tutorial_step += 1
    if game_state.tutorial_step >= len(tutorial_texts):
        show_menu()
    else:
        update_tutorial_text()

def start_game(demo_mode=False):
    game_state.current_screen = "game"
    game_state.demo_mode = demo_mode
    game_state.reset()
    game_state.demo_timer = 0
    
    menu_container.enabled = False
    tutorial_container.enabled = False
    game_ui_container.enabled = True
    
    demo_indicator.enabled = demo_mode
    
    result_panel.enabled = False
    result_text.enabled = False
    result_score.enabled = False
    restart_text.enabled = False
    
    setup_environment()
    
    player.reset()
    player.enabled = True
    
    clear_enemies()
    spawn_enemies()
    
    update_health_display()
    update_score_display()
    
    level_text.text = f"Level: {game_state.level}"
    objective_text.text = "Defeat the enemy!"
    
    camera.position = (0, 10, -15)
    camera.rotation_x = 25

def trigger_game_over():
    game_state.game_over = True
    
    result_panel.enabled = True
    result_text.text = "GAME OVER"
    result_text.color = color.red
    result_text.enabled = True
    result_score.text = f"Final Score: {game_state.score}"
    result_score.enabled = True
    restart_text.enabled = True

def trigger_victory():
    game_state.victory = True
    
    result_panel.enabled = True
    result_text.text = "VICTORY!"
    result_text.color = BEN_GREEN
    result_text.enabled = True
    result_score.text = f"Final Score: {game_state.score}"
    result_score.enabled = True
    restart_text.enabled = True
    objective_text.text = "All enemies defeated!"

def restart_game():
    game_state.reset()
    game_state.demo_timer = 0
    
    result_panel.enabled = False
    result_text.enabled = False
    result_score.enabled = False
    restart_text.enabled = False
    
    player.reset()
    
    clear_enemies()
    spawn_enemies()
    
    update_health_display()
    update_score_display()
    
    level_text.text = f"Level: {game_state.level}"
    objective_text.text = "Defeat the enemy!"

# ==================== MAIN UPDATE & INPUT ====================

def update():
    if game_state.current_screen == "game":
        # Camera follow
        target_pos = player.position + Vec3(0, 8, -12)
        camera.position = lerp(camera.position, target_pos, time.dt * 5)
        camera.look_at(player.position + Vec3(0, 1, 0))

def input(key):
    if game_state.current_screen == "menu":
        if key == 'escape':
            application.quit()
    
    elif game_state.current_screen == "tutorial":
        if key == 'space':
            next_tutorial_step()
        elif key == 'escape':
            show_menu()
    
    elif game_state.current_screen == "game":
        if key == 'space' and not game_state.demo_mode:
            player.attack()
        
        if key == 'r' and (game_state.game_over or game_state.victory):
            restart_game()
        
        if key == 'escape':
            show_menu()

# ==================== INITIALIZATION ====================

# Start at menu
show_menu()

# Console instructions
print("=" * 40)
print("  BEN 10: ALIEN FORCE - DEMO")
print("=" * 40)
print("  Main Menu Controls:")
print("    - Click buttons to navigate")
print("    - ESC to quit")
print("")
print("  Game Controls:")
print("    - WASD / Arrows: Move")
print("    - SPACE: Attack")
print("    - R: Restart (after game ends)")
print("    - ESC: Return to menu")
print("=" * 40)

# Run the game
app.run()
