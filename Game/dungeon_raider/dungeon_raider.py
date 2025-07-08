import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random
import math
import sys
import time
import os

# Initialize pygame
pygame.init()
screen_width, screen_height = 880, 620
screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
pygame.display.set_caption("Dungeon Raider 3D - Enhanced")

# Camera settings
CAMERA_DISTANCE = 12
CAMERA_HEIGHT = 5
CAMERA_ANGLE = 0
CAMERA_SENSITIVITY = 2

# Game settings
PLAYER_SPEED = 0.15
CHASER_BASE_SPEED = 0.07
MAX_LEVEL = 10
MAX_LIVES = 3

# Colors
BLUE = (0, 0.5, 1)
RED = (1, 0, 0)
YELLOW = (1, 1, 0)
GREEN = (0, 1, 0)
GRAY = (0.5, 0.5, 0.5)
PURPLE = (0.5, 0, 0.5)
ORANGE = (1, 0.5, 0)

# Fonts
font = pygame.font.SysFont("Arial", 32, True)
large_font = pygame.font.SysFont("Arial", 64, True)


def load_texture(image_path, default_color=None):
    """Load texture with error handling and fallback color"""
    try:
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Texture not found: {image_path}")

        texture_surface = pygame.image.load(image_path).convert_alpha()
        texture_data = pygame.image.tostring(texture_surface, "RGBA", True)
        width, height = texture_surface.get_size()

        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
        return texture_id
    except Exception as e:
        print(f"Error loading texture: {e}")
        if default_color:
            # Create a colored texture as fallback
            texture_id = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, texture_id)
            color_data = [int(c * 255) for c in default_color] + [255]  # RGBA
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, 1, 1, 0, GL_RGBA, GL_UNSIGNED_BYTE, bytes(color_data))
            return texture_id
        return None


def draw_3d_sprite(x, y, z, width, height, texture=None, color=None, rotation=0):
    """Draw a 2D sprite in 3D space that always faces the camera"""
    glPushMatrix()
    glTranslatef(x, y, z)

    # Rotate to face camera (billboarding)
    glRotatef(-CAMERA_ANGLE, 0, 0, 1)
    glRotatef(90, 1, 0, 0)  # Stand upright

    if texture:
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, texture)
        glColor3f(1, 1, 1)  # White to show texture properly
    elif color:
        glColor3f(*color)

    half_w = width / 2
    half_h = height / 2

    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex3f(-half_w, -half_h, 0)
    glTexCoord2f(1, 0)
    glVertex3f(half_w, -half_h, 0)
    glTexCoord2f(1, 1)
    glVertex3f(half_w, half_h, 0)
    glTexCoord2f(0, 1)
    glVertex3f(-half_w, half_h, 0)
    glEnd()

    if texture:
        glDisable(GL_TEXTURE_2D)

    glPopMatrix()


class Entity:
    def __init__(self, x, y, z, width, height, texture=None, color=None):
        self.x = x
        self.y = y
        self.z = z
        self.width = width
        self.height = height
        self.texture = texture
        self.color = color

    def draw(self):
        draw_3d_sprite(self.x, self.y, self.z, self.width, self.height, self.texture, self.color)

    def get_rect(self):
        return pygame.Rect(self.x - self.width / 2, self.y - self.height / 2, self.width, self.height)


class Treasure(Entity):
    def __init__(self, x, y, z, width, height, closed_texture, open_texture):
        super().__init__(x, y, z, width, height, closed_texture)
        self.closed_texture = closed_texture
        self.open_texture = open_texture
        self.is_open = False
        self.open_time = 0

    def open(self):
        if not self.is_open:
            self.is_open = True
            self.texture = self.open_texture
            self.open_time = time.time()
            return True
        return False

    def draw(self):
        if self.is_open and time.time() - self.open_time < 0.5:
            glPushMatrix()
            glTranslatef(self.x, self.y, self.z + 0.2 * math.sin((time.time() - self.open_time) * 10))
            draw_3d_sprite(0, 0, 0, self.width, self.height, self.texture)
            glPopMatrix()
        else:
            super().draw()


class Player(Entity):
    def __init__(self, x, y, z):
        super().__init__(x, y, z, 1.5, 2.0)
        self.speed = PLAYER_SPEED
        self.rotation = 0


class Game:
    def __init__(self):
        self.obstacles = []
        self.reset_game()

    def reset_game(self):
        self.level = 1
        self.score = 0
        self.lives = MAX_LIVES
        self.timer = 60
        self.last_time = time.time()
        self.game_over = False
        self.game_over_time = 0
        self.load_assets()
        self.init_entities()

    def load_assets(self):
        if not os.path.exists("assets"):
            os.makedirs("assets")
            print("Created 'assets' directory. Please add your texture files.")

        self.textures = {
            "player": load_texture("assets/player.png", BLUE),
            "chaser": load_texture("assets/chaser.png", RED),
            "treasure_closed": load_texture("assets/treasure_closed.png", YELLOW),
            "treasure_open": load_texture("assets/treasure_open.png", ORANGE),
            "gate": load_texture("assets/gate.png", GREEN),
            "obstacle": load_texture("assets/obstacle.png", GRAY),
            "floor1": load_texture("assets/floor1.png", (0.2, 0.2, 0.3)),
            "floor2": load_texture("assets/floor2.png", (0.3, 0.2, 0.2)),
            "floor3": load_texture("assets/floor3.png", (0.2, 0.3, 0.2)),
        }

    def init_entities(self):
        self.player = Player(0, 0, 0.1)
        self.player.texture = self.textures["player"]

        self.chaser = Entity(
            random.randint(-15, 15),
            random.randint(-15, 15),
            0.1,
            1.5, 2.0,
            self.textures["chaser"]
        )

        self.chaser_speed = CHASER_BASE_SPEED + self.level * 0.01
        self.obstacles = self.generate_obstacles(min(3 + self.level, 7))

        self.treasure = Treasure(
            *self.find_valid_position(1.2, 1.2),
            0.1,
            1.2, 1.2,
            self.textures["treasure_closed"],
            self.textures["treasure_open"]
        )

        self.gate = Entity(
            *self.find_valid_position(1.8, 2.0),
            0.1,
            1.8, 2.0,
            self.textures["gate"]
        )
        self.gate_active = False

    def find_valid_position(self, width, height):
        while True:
            x = random.randint(-15, 15)
            y = random.randint(-15, 15)
            entity = Entity(x, y, 0, width, height)
            if not self.check_collision(entity, [self.player] + self.obstacles):
                return x, y

    def generate_obstacles(self, count):
        obstacles = []
        for _ in range(count):
            x, y = self.find_valid_position(
                random.uniform(1.2, 2.0),
                random.uniform(1.2, 2.0))
            obstacles.append(Entity(
                x, y, 0.1,
                random.uniform(1.2, 2.0),
                random.uniform(1.2, 2.0),
                self.textures["obstacle"]
            ))
        return obstacles

    def check_collision(self, entity, entities):
        rect1 = entity.get_rect()
        for other in entities:
            rect2 = other.get_rect()
            if rect1.colliderect(rect2):
                return True
        return False

    def draw_text(self, text, font, color, x, y):
        glDisable(GL_TEXTURE_2D)
        text_surface = font.render(text, True, color)
        text_data = pygame.image.tostring(text_surface, "RGBA", True)
        width, height = text_surface.get_size()

        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, screen_width, 0, screen_height)

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        glRasterPos2f(x, screen_height - y)
        glDrawPixels(width, height, GL_RGBA, GL_UNSIGNED_BYTE, text_data)

        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()

    def setup_camera(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60, (screen_width / screen_height), 0.1, 100.0)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        rad_angle = math.radians(CAMERA_ANGLE)
        cam_x = self.player.x - CAMERA_DISTANCE * math.sin(rad_angle)
        cam_y = self.player.y - CAMERA_DISTANCE * math.cos(rad_angle)
        cam_z = CAMERA_HEIGHT

        look_ahead = 5
        look_x = self.player.x + math.sin(rad_angle) * look_ahead
        look_y = self.player.y + math.cos(rad_angle) * look_ahead

        gluLookAt(
            cam_x, cam_y, cam_z,
            look_x, look_y, self.player.z,
            0, 0, 1
        )

    def draw_floor(self):
        floor_texture = self.textures[f"floor{min(3, self.level)}"]

        if floor_texture:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, floor_texture)
            glColor3f(1, 1, 1)
        else:
            glColor3f(0.2, 0.2, 0.3)

        size = 30
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex3f(-size, -size, 0)
        glTexCoord2f(10, 0)
        glVertex3f(size, -size, 0)
        glTexCoord2f(10, 10)
        glVertex3f(size, size, 0)
        glTexCoord2f(0, 10)
        glVertex3f(-size, size, 0)
        glEnd()

        glDisable(GL_TEXTURE_2D)

    def draw_all(self):
        glClearColor(0.1, 0.1, 0.15, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        self.setup_camera()
        self.draw_floor()

        if self.game_over:
            self.draw_game_over_screen()
            return

        for obstacle in self.obstacles:
            obstacle.draw()

        self.player.draw()
        self.chaser.draw()
        self.treasure.draw()

        if self.gate_active:
            self.gate.draw()

        self.draw_hud()

    def draw_game_over_screen(self):
        # شاشة Game Over مع تعليمات إعادة التشغيل
        self.draw_text("GAME OVER", large_font, RED,
                       screen_width // 2 - 150, screen_height // 2 - 50)
        self.draw_text(f"Final Score: {self.score}", font, (1, 1, 1),
                       screen_width // 2 - 100, screen_height // 2 - 120)
        self.draw_text("Press ENTER to Play Again", font, GREEN,
                       screen_width // 2 - 150, screen_height // 2 + 50)
        self.draw_text("Press ESC to Quit", font, (1, 1, 1),
                       screen_width // 2 - 100, screen_height // 2 + 100)

    def draw_hud(self):
        self.draw_text(f"Score: {self.score}", font, (1, 1, 1), 20, 40)
        self.draw_text(f"Level: {self.level}/{MAX_LEVEL}", font, (1, 1, 1), 20, 80)
        self.draw_text(f"Time: {int(self.timer)}", font, (1, 1, 1), 20, 120)
        self.draw_text(f"Lives: {self.lives}", font, (1, 1, 1), 20, 160)

    def update(self, keys, mouse_rel):
        now = time.time()
        delta_time = now - self.last_time
        self.last_time = now

        if self.game_over:
            # التحقق من ضغط Enter لإعادة التشغيل
            if keys[pygame.K_RETURN]:
                self.reset_game()
            return

        if not self.game_over:
            self.timer -= delta_time
            if self.timer <= 0:
                self.game_over = True
                self.game_over_time = now
                return

        global CAMERA_ANGLE
        CAMERA_ANGLE = (CAMERA_ANGLE - mouse_rel[0] * CAMERA_SENSITIVITY) % 360

        move_speed = self.player.speed
        rad_angle = math.radians(CAMERA_ANGLE)

        dx, dy = 0, 0
        if keys[pygame.K_w]:
            dy -= move_speed
        if keys[pygame.K_s]:
            dy += move_speed
        if keys[pygame.K_a]:
            dx -= move_speed
        if keys[pygame.K_d]:
            dx += move_speed

        future_player = Entity(
            self.player.x + dx,
            self.player.y + dy,
            self.player.z,
            self.player.width,
            self.player.height
        )

        if not self.check_collision(future_player, self.obstacles):
            self.player.x += dx
            self.player.y += dy

        dx = self.player.x - self.chaser.x
        dy = self.player.y - self.chaser.y
        dist = math.hypot(dx, dy)
        if dist > 0:
            self.chaser.x += (dx / dist) * self.chaser_speed
            self.chaser.y += (dy / dist) * self.chaser_speed

        if not self.treasure.is_open and self.check_collision(self.player, [self.treasure]):
            if self.treasure.open():
                self.score += random.randint(10, 50)
                self.gate_active = True

        if self.gate_active and self.check_collision(self.player, [self.gate]):
            if self.level >= MAX_LEVEL:
                self.game_over = True
                self.game_over_time = time.time()
            else:
                self.level += 1
                self.timer = 60
                self.init_entities()

        if self.check_collision(self.player, [self.chaser]):
            self.lives -= 1
            if self.lives <= 0:
                self.game_over = True
                self.game_over_time = time.time()
            else:
                self.player.x, self.player.y = 0, 0
                self.chaser.x, self.chaser.y = random.randint(-15, 15), random.randint(-15, 15)

    def run(self):
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)

        clock = pygame.time.Clock()
        while True:
            mouse_rel = pygame.mouse.get_rel()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()
            self.update(keys, mouse_rel)
            self.draw_all()
            pygame.display.flip()

            clock.tick(60)


if __name__ == "__main__":
    print("Starting Dungeon Raider 3D...")
    print("Controls:")
    print("- WASD to move")
    print("- Mouse to look around")
    print("- ESC to quit")
    print("- ENTER to restart after Game Over")

    if not os.path.exists("assets"):
        print("\nNote: Please create an 'assets' folder and add:")
        print("player.png, chaser.png, treasure_closed.png, treasure_open.png, gate.png")
        print("floor1.png, floor2.png, floor3.png (optional)")

    Game().run()