import math
import logging
import arcade
import arcade.key
import pymunk

from game_object import Bird, YellowBird, BlueBird, Column, Pig
from game_logic import get_impulse_vector, Point2D, get_distance

logging.basicConfig(level=logging.DEBUG)
logging.getLogger("arcade").setLevel(logging.WARNING)
logging.getLogger("pymunk").setLevel(logging.WARNING)
logging.getLogger("PIL").setLevel(logging.WARNING)

logger = logging.getLogger("main")

WIDTH = 1800
HEIGHT = 800
TITLE = "Angry birds"
GRAVITY = -900


class App(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, TITLE)
        self.background = arcade.load_texture("assets/img/background3.png")
        #Crear score para actualizar puntaje
        self.score = 0

        # crear espacio de pymunk
        self.space = pymunk.Space()
        self.space.gravity = (0, GRAVITY)

        # agregar piso
        floor_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        floor_shape = pymunk.Segment(floor_body, [0, 15], [WIDTH, 15], 0.0)
        floor_shape.friction = 10
        self.space.add(floor_body, floor_shape)

        self.sprites = arcade.SpriteList()
        self.birds = arcade.SpriteList()
        self.world = arcade.SpriteList()
        self.add_columns()
        self.add_pigs()

        self.start_point = Point2D()
        self.end_point = Point2D()
        self.distance = 0
        self.draw_line = False
        self.bird_type = "red"

        # agregar un collision handler
        self.handler = self.space.add_default_collision_handler()
        self.handler.post_solve = self.collision_handler

    def collision_handler(self, arbiter, space, data):
        impulse_norm = arbiter.total_impulse.length
        if impulse_norm < 100:
            return True
        logger.debug(impulse_norm)
        if impulse_norm > 1200:
            for obj in self.world:
                if obj.shape in arbiter.shapes:
                    obj.remove_from_sprite_lists()
                    self.space.remove(obj.shape, obj.body)
                    self.score += 15

        return True

    def add_columns(self):
        for x in range(WIDTH // 2, WIDTH, 300):
            logger.debug(f"Posion de la columna: {x}")
            column = Column(x, 50, self.space)
            self.sprites.append(column)
            self.world.append(column)

    def add_pigs(self):
        pig1 = Pig(WIDTH / 2, 100, self.space)
        self.sprites.append(pig1)
        self.world.append(pig1)

    def on_update(self, delta_time: float):
        self.space.step(1 / 60.0)  # actualiza la simulacion de las fisicas
        self.update_collisions()
        self.sprites.update()

    def update_collisions(self):
        pass

    def create_level(self):
        pass
    
    def change_level(self):
        pass


    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.start_point = Point2D(x, y)
            self.end_point = Point2D(x, y)
            self.draw_line = True
            logger.debug(f"Start Point: {self.start_point}")

        if button == arcade.MOUSE_BUTTON_RIGHT:
            for bird in self.birds:
                if isinstance(bird, YellowBird) and not bird.has_boosted:
                    bird.on_click()
                    break
                elif isinstance(bird, BlueBird) and not bird.has_split:
                    bird.on_click()
                    break

    def on_mouse_drag(self, x: int, y: int, dx: int, dy: int, buttons: int, modifiers: int):
        if buttons == arcade.MOUSE_BUTTON_LEFT:
            self.end_point = Point2D(x, y)
            logger.debug(f"Dragging to: {self.end_point}")

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        if button == arcade.MOUSE_BUTTON_LEFT:
            logger.debug(f"Releasing from: {self.end_point}")
            self.draw_line = False
            impulse_vector = get_impulse_vector(self.start_point, self.end_point)
            if self.bird_type == "red":
                bird = Bird(F"assets/img/{self.bird_type}-bird.png", impulse_vector, x, y, self.space)
            elif self.bird_type == "yellow":
                bird = YellowBird(F"assets/img/{self.bird_type}-bird.png", impulse_vector, x, y, self.space)
            elif self.bird_type == "blue":
                bird = BlueBird(F"assets/img/{self.bird_type}-bird.png", impulse_vector, x, y, self.space, self.sprites, self.birds)
            self.sprites.append(bird)
            self.birds.append(bird)

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.Q:
            self.bird_type = "red"
        elif symbol == arcade.key.W:
            self.bird_type = "yellow"
        elif symbol == arcade.key.E:
            self.bird_type = "blue"

    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, WIDTH, HEIGHT, self.background)
        arcade.draw_lrwh_rectangle_textured(30, 700, 80, 80, arcade.load_texture(f"assets/img/{self.bird_type}-bird.png"))
        self.sprites.draw()
        if self.draw_line:
            arcade.draw_line(self.start_point.x, self.start_point.y, self.end_point.x, self.end_point.y,
                             arcade.color.BLACK, 3)
            
        start_x = 1350
        start_y = HEIGHT - 30
        arcade.draw_text(f"Score: {self.score}",
                         start_x,
                         start_y,
                         arcade.color.FRENCH_WINE,
                         18, bold=True)


def main():
    app = App()
    arcade.run()


if __name__ == "__main__":
    main()