from game_object import Column, Pig, Box, Beam, Triangle_Beam
WIDTH = 1600
HEIGHT = 600

box_width = 30  # Ancho de cada Box
box_height = 30  # Altura de cada Box
column_width = 25  # Ancho de cada columna
column_height = 90  # Altura de cada columna
beam_width = 100  # Ancho de cada Beam
beam_height = 20  # Altura de cada Beam
beam_size = 34  # Tamaño de cada Triangle Beam (piramide)

#funciones para crear las figuras de los niveles
def add_pigs(space, sprites, world, x ,y):
    pig1 = Pig(x, y, space)
    sprites.append(pig1)
    world.append(pig1)


def create_pyramid(space, sprites, world, num_rows: int, start_x: int, start_y: int):
        column_width = 25
        column_height = 90
        beam_width = 100
        beam_height = 20

        for row in range(num_rows):
            # Calcular la cantidad de cuartos en esta fila
            num_quarters = num_rows - row

            # Calcular el desplazamiento para centrar la fila en relación con el punto inicial
            row_start_x = start_x - (num_quarters * (column_width + beam_width) // 2)

            for i in range(num_quarters):
                # Posición de la columna izquierda
                column_left_x = row_start_x + i * (column_width + beam_width)
                column_left_y = start_y + row * (column_height + beam_height)
                column_left = Column(column_left_x, column_left_y, space)
                sprites.append(column_left)
                world.append(column_left)

                # Posición de la columna derecha
                column_right_x = column_left_x + beam_width
                column_right = Column(column_right_x, column_left_y, space)
                sprites.append(column_right)
                world.append(column_right)

                # Posición del beam (techo) entre las columnas
                beam_x = column_left_x + beam_width / 2
                beam_y = column_left_y + column_height / 2
                beam = Beam(beam_x, beam_y, space)
                sprites.append(beam)
                world.append(beam)

def create_triangle_beam_pyramid(space, sprites, world, num_rows, start_x: int, start_y: int):
     
    beam_size = 34  # Ancho y alto del triángulo

    for row in range(num_rows):
        # Calcular la cantidad de triángulos en esta fila
        num_beams = num_rows - row

        # Calcular el desplazamiento para centrar la fila en relación con el punto inicial
        row_start_x = start_x - (num_beams * beam_size // 2)

        for i in range(num_beams):
            # Posición de cada triángulo en la fila
            beam_x = row_start_x + i * beam_size
            beam_y = start_y + row * beam_size
            triangle_beam = Triangle_Beam(beam_x, beam_y, space)

            # Añadir el triángulo a las listas correspondientes
            sprites.append(triangle_beam)
            world.append(triangle_beam)
     
def create_warehouse(space, sprites, world, start_x: int, start_y: int):
    # Tamaños de los objetos
    box_width = 30  # Ancho de cada Box
    box_height = 30  # Altura de cada Box
    column_width = 25  # Ancho de cada columna
    column_height = 90  # Altura de cada columna
    beam_width = 100  # Ancho de cada Beam
    beam_height = 20  # Altura de cada Beam
    beam_size = 34  # Tamaño de cada Triangle Beam (piramide)

    # Crear la base con 3 Boxes juntos
    for i in range(3):
        box = Box(start_x + i * box_width, start_y, space)
        sprites.append(box)
        world.append(box)

    # Crear las columnas en los bordes izquierdo y derecho de los Boxes
    column1 = Column(start_x - column_width // 2 + box_width // 2,  box_height + column_height // 2, space)
    column2 = Column(start_x + 2 * box_width + column_width // 2 - box_width // 2,  box_height + column_height // 2, space)
    sprites.append(column1)
    sprites.append(column2)
    world.append(column1)
    world.append(column2)

    # Colocar un Beam como techo sobre las dos columnas
    beam = Beam(start_x + box_width, box_height + column_height + beam_height // 2, space)
    sprites.append(beam)
    world.append(beam)

    # Crear la pirámide de Beams (3x3) sobre el techo
    pyramid_start_x = start_x + box_width + (beam_width//2 - beam_size)
    pyramid_start_y = box_height + column_height + beam_height + beam_size // 2
    create_triangle_beam_pyramid(space, sprites, world, num_rows=2, start_x=pyramid_start_x, start_y=pyramid_start_y)


# Define cada nivel como una lista de tuplas (función, diccionario de parámetros)
level_1 = [
    (create_warehouse, {
        "start_x": WIDTH // 2 + 200,
        "start_y": 40
    }),
    (create_warehouse, {
        "start_x": WIDTH // 2 + 400,
        "start_y": 40
    }), (add_pigs,{
        "x": WIDTH // 2 + 200 + box_width,
        "y": 70
    }),(add_pigs,{
        "x": WIDTH // 2 + 400 +  box_width,
        "y": 70
    })
]


level_2 = [
    (create_pyramid, {
        "num_rows": 3,
        "start_x":  WIDTH // 2 + 100, 
        "start_y": 40
    }),
    (create_warehouse, {
        "start_x": WIDTH // 2 + 300,
        "start_y": 40
    }), (add_pigs,{
        "x": WIDTH // 2 + 100 ,
        "y": 70
    }),(add_pigs,{
        "x": WIDTH // 2 + 100 ,
        "y": 300
    }),(add_pigs,{
        "x": WIDTH // 2 + 300 +  box_width,
        "y": 70
    }),(add_pigs,{
        "x": WIDTH // 2 + 300 ,
        "y": 70
    })
]


level_3 = [
    (create_pyramid, {
        "num_rows": 5,
        "start_x":  WIDTH // 2 + 250, 
        "start_y": 40
    }),
    (create_triangle_beam_pyramid, {
        "num_rows": 4,
        "start_x": WIDTH // 2 + 650,
        "start_y": 40
    }),(create_triangle_beam_pyramid, {
        "num_rows": 3,
        "start_x": WIDTH // 2 -150,
        "start_y": 40
    }), (add_pigs,{
        "x": WIDTH // 2 + 250 ,
        "y": 70
    }),(add_pigs,{
        "x": WIDTH // 2 + 250 ,
        "y": 270
    }),(add_pigs,{
        "x": WIDTH // 2 + 250 ,
        "y": 500
    }),(add_pigs,{
        "x": WIDTH // 2 + 350 ,
        "y": 70
    }),(add_pigs,{
        "x": WIDTH // 2 + 130 ,
        "y": 70
    }),(add_pigs,{
        "x": WIDTH // 2 + 150 ,
        "y": 370
    }),(add_pigs,{
        "x": WIDTH // 2 + 450 ,
        "y": 150
    })
]
