import math
import arcade
import pymunk
import logging
from game_logic import ImpulseVector


logger = logging.getLogger("game_object")


class Bird(arcade.Sprite):
    """
    Bird class. This represents an angry bird. All the physics is handled by Pymunk,
    the init method only set some initial properties
    """
    def __init__(
        self,
        image_path: str,
        impulse_vector: ImpulseVector,
        x: float,
        y: float,
        space: pymunk.Space,
        mass: float = 5,
        radius: float = 12,
        max_impulse: float = 100,
        power_multiplier: float = 50,
        elasticity: float = 0.8,
        friction: float = 1,
        collision_layer: int = 0,
    ):
        super().__init__(image_path, 1)
        # body
        moment = pymunk.moment_for_circle(mass, 0, radius)
        body = pymunk.Body(mass, moment)
        body.position = (x, y)

        impulse = min(max_impulse, impulse_vector.impulse) * power_multiplier
        impulse_pymunk = impulse * pymunk.Vec2d(1, 0)
        # apply impulse
        body.apply_impulse_at_local_point(impulse_pymunk.rotated(impulse_vector.angle))
        # shape
        shape = pymunk.Circle(body, radius)
        shape.elasticity = elasticity
        shape.friction = friction
        shape.collision_type = collision_layer

        space.add(body, shape)

        self.body = body
        self.shape = shape

    def update(self):
        """
        Update the position of the bird sprite based on the physics body position
        """
        self.center_x = self.shape.body.position.x
        self.center_y = self.shape.body.position.y
        self.radians = self.shape.body.angle

class YellowBird(Bird):
    def __init__(self, 
                 image_path: str, 
                 impulse_vector: ImpulseVector, 
                 x: float, y: float, 
                 space: pymunk.Space, 
                 impulse_multiplier: float = 3
                 ):
        super().__init__(image_path, 
                         impulse_vector, 
                         x, 
                         y, 
                         space)
        self.impulse_multiplier = impulse_multiplier
        self.has_boosted = False  # Para evitar que el impulso aumente varias veces

    def on_click(self):
        if not self.has_boosted:
            impulse = self.impulse_multiplier * self.body.velocity.length
            logger.debug(f"Chuck esta siendo impulsado con: {impulse} de impulso")
            impulse_vector = pymunk.Vec2d(impulse, 0).rotated(self.body.angle)
            self.body.apply_impulse_at_local_point(impulse_vector)
            logger.debug(f"Chuck ha sido impulsado")
            self.has_boosted = True  # Asegura que el impulso solo aumente una vez

class BlueBird(Bird):
    def __init__(self, 
                 image_path: str, 
                 impulse_vector: ImpulseVector, 
                 x: float, y: float, 
                 space: pymunk.Space, 
                 sprites_list: arcade.SpriteList,
                 birds_list: arcade.SpriteList,
                 angle_offset: float = 30
                 ):
        super().__init__(image_path, 
                         impulse_vector, 
                         x, 
                         y, 
                         space)
        self.angle_offset = angle_offset
        self.has_split = False
        self.sprites_list = sprites_list  
        self.birds_list = birds_list

    def on_click(self):
        if not self.has_split:
            logger.debug(f"Blue esta siendo dividido")
            # Calcular las nuevas direcciones
            angles = [self.body.angle + math.radians(self.angle_offset),
                      self.body.angle,
                      self.body.angle - math.radians(self.angle_offset)]
            logger.debug(f"Se calcularon las nuevas direcciones para dividir a Blue: {angles}")
            i = 1
            for angle in angles:
                # Mantener la velocidad actual del pájaro
                velocity = self.body.velocity.rotated(angle - self.body.angle)

                # Crear un nuevo bird con la misma velocidad y diferente ángulo
                new_bird = Bird(
                    self.texture.name,  
                    ImpulseVector(velocity.length, angle),
                    self.body.position.x,
                    self.body.position.y,
                    self.shape.space,
                    mass=self.shape.body.mass,
                    radius=self.shape.radius,
                    max_impulse=velocity.length,
                    power_multiplier=1,  
                    elasticity=self.shape.elasticity,
                    friction=self.shape.friction,
                    collision_layer=self.shape.collision_type
                )

                # Aplicar la velocidad al nuevo bird
                new_bird.body.velocity = velocity

                # Añadir el nuevo pájaro a la lista
                self.sprites_list.append(new_bird)
                self.birds_list.append(new_bird)
                logger.debug(f"Se crearo un nuevo Blue con el angulo {i} calculado")
                i+=1


            # Remover el BlueBird original
            self.remove_from_sprite_lists()
            self.shape.space.remove(self.shape, self.body)
            self.has_split = True
class Pig(arcade.Sprite):
    def __init__(
        self,
        x: float,
        y: float,
        space: pymunk.Space,
        mass: float = 2,
        elasticity: float = 0.8,
        friction: float = 0.4,
        collision_layer: int = 0,
    ):
        super().__init__("assets/img/pig_failed.png", 0.1)
        moment = pymunk.moment_for_circle(mass, 0, self.width / 2 - 3)
        body = pymunk.Body(mass, moment)
        body.position = (x, y)
        shape = pymunk.Circle(body, self.width / 2 - 3)
        shape.elasticity = elasticity
        shape.friction = friction
        shape.collision_type = collision_layer
        space.add(body, shape)
        self.body = body
        self.shape = shape

    def update(self):
        self.center_x = self.shape.body.position.x
        self.center_y = self.shape.body.position.y
        self.radians = self.shape.body.angle


class PassiveObject(arcade.Sprite):
    """
    Passive object that can interact with other objects.
    """
    def __init__(
        self,
        image_path: str,
        x: float,
        y: float,
        space: pymunk.Space,
        mass: float = 2,
        elasticity: float = 0.8,
        friction: float = 1,
        collision_layer: int = 0,
    ):
        super().__init__(image_path, 1)

        moment = pymunk.moment_for_box(mass, (self.width, self.height))
        body = pymunk.Body(mass, moment)
        body.position = (x, y)
        shape = pymunk.Poly.create_box(body, (self.width, self.height))
        shape.elasticity = elasticity
        shape.friction = friction
        shape.collision_type = collision_layer
        space.add(body, shape)
        self.body = body
        self.shape = shape

    def update(self):
        self.center_x = self.shape.body.position.x
        self.center_y = self.shape.body.position.y
        self.radians = self.shape.body.angle


class Column(PassiveObject):
    def __init__(self, x, y, space):
        super().__init__("assets/img/column.png", x, y, space)


class StaticObject(arcade.Sprite):
    def __init__(
            self,
            image_path: str,
            x: float,
            y: float,
            space: pymunk.Space,
            mass: float = 2,
            elasticity: float = 0.8,
            friction: float = 1,
            collision_layer: int = 0,
    ):
        super().__init__(image_path, 1)

