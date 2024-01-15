import math


class Hexagon:
    has_start_hexagon = False
    has_finish_hexagon = False
    'Словарь цветов для каждого из уровней проходимости'
    PASSABILITY_COLORS = {
        -3: (0, 255, 127),
        -2: (60, 179, 113),
        -1: (46, 139, 87),
        0: (34, 139, 34),
        1: (0, 128, 0),
        2: (0, 100, 0),
        3: (47, 79, 79)
    }

    OUTLINE_COLOR = (0, 0, 0)  # Цвет обводки
    OUTLINE_WIDTH = 1  # Толщина обводки

    HEXAGON_COUNT = 0  # Общее кол-во экземпляров класса Hexagon

    R = 50  # Радиус описанной окружности для всех экземпляров класса Hexagon

    MIN_PASSABILITY = -3  # Минимальный уровень проходимости
    MAX_PASSABILITY = 3 # Максимальный уровень проходимости

    DEFAULT_PASSABILITY = 0  # Начальная проходимость всех экземпляров класса Hexagon

    def __init__(self, center):
        """ (A) - север.
            (B) - северо-восток.
            (C) - юго-восток.
            (D) - юг.
            (E) - юго-запад.
            (F) - северо-запад."""

        def get_corner_coordinates(corner_name, center, r):
            """
            :param corner_name:
            :param center:
            :param r:
            :return координаты вершины corner_name:
            """
            x = center[0]
            y = center[1]
            corner_angles = {'A': 0,
                             'B': 60,
                             'C': 120,
                             'D': 180,
                             'E': 240,
                             'F': 300}
            angle_deg = corner_angles[corner_name] + 30
            angle_rad = math.pi / 180 * angle_deg
            return (x + r * math.cos(angle_rad), y + r * math.sin(angle_rad))

        Hexagon.HEXAGON_COUNT += 1  # Увеличение счетчика общего кол-ва экземпляров класса на 1
        self.id = Hexagon.HEXAGON_COUNT  # Уникальный идентификатор

        self.center = center  # координаты центра шестиугольника
        self.x = center[0]  # координата x шестиугольника
        self.y = center[1]  # координата y шестиугольника

        self.r = Hexagon.R  # радиус шестиугольника

        self.A_corner = get_corner_coordinates('A', self.center, self.r)
        self.A_corner_x = self.A_corner[0]
        self.A_corner_y = self.A_corner[1]

        self.B_corner = get_corner_coordinates('B', self.center, self.r)
        self.B_corner_x = self.B_corner[0]
        self.B_corner_y = self.B_corner[1]

        self.C_corner = get_corner_coordinates('C', self.center, self.r)
        self.C_corner_x = self.C_corner[0]
        self.C_corner_y = self.C_corner[1]

        self.D_corner = get_corner_coordinates('D', self.center, self.r)
        self.D_corner_x = self.D_corner[0]
        self.D_corner_y = self.D_corner[1]

        self.E_corner = get_corner_coordinates('E', self.center, self.r)
        self.E_corner_x = self.E_corner[0]
        self.E_corner_y = self.E_corner[1]

        self.F_corner = get_corner_coordinates('F', self.center, self.r)
        self.F_corner_x = self.F_corner[0]
        self.F_corner_y = self.F_corner[1]

        self.neighbors = {}  # словарь соседей шестиугольника

        self.passability = self.DEFAULT_PASSABILITY  # Проходимость экземпляра класса Hexagon

        self.color = self.PASSABILITY_COLORS.get(self.passability, (0, 0, 0))  # Цвет экземпляра класса Hexagon

        self.outline_width = Hexagon.OUTLINE_WIDTH  # Толщина обводки
        self.outline_color = Hexagon.OUTLINE_COLOR  # Цвет обводки

        self.is_start = False
        self.is_robot_here = False
        self.is_finish = False

        print(f'Создан экземпляр класса Hexagon {self.id}, вершины {self.get_corners()}')

    def set_is_start(self):
        # Проверка, нет ли уже "стартового" hexagon
        if Hexagon.has_start_hexagon is False:
            self.is_start = True
            Hexagon.has_start_hexagon = self
        else:
            Hexagon.has_start_hexagon.update_color()
            Hexagon.has_start_hexagon.is_start = False
            self.is_start = True
            Hexagon.has_start_hexagon = self

        self.color = (255, 255, 0)

    def set_is_finish(self):
        # Проверка, нет ли уже "стартового" hexagon
        if Hexagon.has_finish_hexagon is False:
            self.is_finish = True
            Hexagon.has_finish_hexagon = self
        else:
            Hexagon.has_finish_hexagon.update_color()
            Hexagon.has_finish_hexagon.is_finish = False
            self.is_finish = True
            Hexagon.has_finish_hexagon = self

        self.color = (210, 105, 30)

    def get_id(self):
        return self.id

    def get_center(self):
        return self.x, self.y

    def get_r(self):
        return self.r

    def get_passability(self):
        return self.passability

    def get_color(self):
        return self.color

    def get_outline_width(self):
        return self.outline_width

    def get_outline_color(self):
        return self.outline_color

    'Обновляет цвет шестиугольника на основе его проходимости'

    def update_color(self):
        self.color = self.PASSABILITY_COLORS.get(self.passability, (0, 0, 0))

    'Увеличивает параметр проходимости на 1'

    def increase_passability(self):
        if self.passability == self.MAX_PASSABILITY:
            self.passability = self.DEFAULT_PASSABILITY
            self.update_color()
        else:
            self.passability += 1
            self.update_color()

    'Уменьшает параметр проходимости на 1'

    def decrease_passability(self):
        if self.passability == self.MIN_PASSABILITY:
            self.passability = self.DEFAULT_PASSABILITY
            self.update_color()
        else:
            self.passability -= 1
            self.update_color()

    def get_corners(self):
        corners = self.A_corner, self.B_corner, self.C_corner, self.D_corner, self.E_corner, self.F_corner
        return corners

    def is_point_inside_hexagon(self, x, y, corners):
        """
        :param x:
        :param y:
        :param corners:
        :return:
        """
        odd_nodes = False
        vertices = corners
        j = len(vertices) - 1

        for i in range(len(vertices)):
            xi, yi = vertices[i]
            xj, yj = vertices[j]

            if ((yi < y and yj >= y) or (yj < y and yi >= y)) and (xi <= x or xj <= x):
                if xi + (y - yi) / (yj - yi) * (xj - xi) < x:
                    odd_nodes = not odd_nodes

            j = i

        if odd_nodes:
            return self  # Возвращаем шестиугольник, если точка внутри
        else:
            return None  # Возвращаем None, если точка снаружи

    def add_neighbor(self, neighbor_hexagon):
        self.neighbors[neighbor_hexagon.get_id()] = neighbor_hexagon

    def get_neighbors(self):
        return self.neighbors

    def add_neighbors(self, hexagons):
        for neighbor_hexagon in hexagons:
            if neighbor_hexagon != self and neighbor_hexagon.get_id() not in self.neighbors:
                self.add_neighbor(neighbor_hexagon)
                neighbor_hexagon.add_neighbor(self)

    def del_neighbor(self, neighbor):
        del self.neighbors[neighbor]
        print(f'У {self.id} удален сосед {neighbor} ')

    def is_it_start(self):
        if self.is_start == True:
            return True
        else:
            return False

    def is_it_finish(self):
        if self.is_finish == True:
            return True
        else:
            return False

    def set_color(self, color):
        self.color = color

    def __lt__(self, other):
        # Определите метод сравнения для объектов Hexagon
        return self.id < other.id
