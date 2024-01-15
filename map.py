import sys, pygame, math, time

from hexagon import Hexagon
from robot import Robot
from algorithm import *

pygame.init()
clock = pygame.time.Clock()

# Получение размеров экрана
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h

screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME)  # Создание окна на полный экран

pygame.display.set_caption("Карта")  # Установка заголовка окна

font_size = 25
font = pygame.font.Font(None, font_size)  # Создание шрифта

hexagons = [Hexagon((screen_width // 2,
                     screen_height // 2))]  # Список для хранения всех экземпляров Hexagon и самый первый шестиугольник

map_already_created = False
robot_already_created = False
start_already_created = False
finish_already_created = False
ready_to_go = False
robot = None
go = False
path = None
robot_index = 1


def distance_between_points(first, second):
    x1 = first[0]
    y1 = first[1]
    x2 = second[0]
    y2 = second[1]
    """
    Вычисляет расстояние между двумя точками в двумерном пространстве.

    Параметры:
    - x1, y1: Координаты первой точки
    - x2, y2: Координаты второй точки

    Возвращает:
    - Расстояние между точками
    """
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def find_new_point(first, second, closest_hexagon):
    x_mid, y_mid = (first[0] + second[0]) / 2, (first[1] + second[1]) / 2
    point = closest_hexagon.get_center()
    x_symmetric, y_symmetric = 2 * x_mid - point[0], 2 * y_mid - point[1]
    return x_symmetric, y_symmetric


def find_closest_corners(click_point):
    closest_corners_first, min_distance_first, closest_hexagon = None, float('inf'), None
    for hexagon in hexagons:
        for corner in hexagon.get_corners():
            distance = math.dist(corner, click_point)
            if distance < min_distance_first:
                min_distance_first, closest_corners_first, closest_hexagon = distance, corner, hexagon

    corners = closest_hexagon.get_corners()
    min_distance_second, closest_corners_second = float('inf'), None

    for corner in corners:
        distance = math.dist(corner, click_point)
        if distance < min_distance_second and corner != closest_corners_first:
            min_distance_second, closest_corners_second = distance, corner

    return closest_corners_first, closest_corners_second, closest_hexagon


while True:
    for event in pygame.event.get():
        """
        Обработка нажатий на клавиатуру
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_g:
                if map_already_created is False:
                    print('Карта создана')
                    map_already_created = True
                else:
                    print('Включен режим редактирования карты')
                    for hexagon in hexagons:
                        hexagon.update_color()
                    map_already_created = False
                    finish_already_created = False
                    start_already_created = False
                    robot_already_created = False
                    go = False
                    robot = None
                    path = None
                    robot_index = 1

            if event.key == pygame.K_SPACE and ready_to_go is True:
                print(graph(hexagons))
                path = bellman_ford(graph(hexagons), Hexagon.has_start_hexagon, Hexagon.has_finish_hexagon)
                for hex in path:
                    hex.set_color((255, 228, 225))
                go = True
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Проверка, было ли нажатие внутри какого-либо Hexagon
            clicked_hexagon = next((hexagon for hexagon in hexagons if
                                    hexagon.is_point_inside_hexagon(mouse_x, mouse_y, hexagon.get_corners())), None)

            if map_already_created is False:
                if clicked_hexagon:
                    # Проверка нажатия правой кнопки мыши
                    if event.button == 3:
                        clicked_hexagon.increase_passability()

                    if event.button == 2:
                        print(clicked_hexagon.get_neighbors())
                        for i in clicked_hexagon.get_neighbors().values():
                            i.del_neighbor(clicked_hexagon.get_id())
                        print('Все соседи удалены')
                        hexagons.remove(clicked_hexagon)
                        del clicked_hexagon

                    # Проверка нажатия левой кнопки мыши
                    elif event.button == 1:
                        clicked_hexagon.decrease_passability()
                else:
                    closest_corners_first, closest_corners_second, closest_hexagon = find_closest_corners(
                        (mouse_x, mouse_y))
                    new_hexagon_point = find_new_point(closest_corners_first, closest_corners_second, closest_hexagon)
                    new_hexagon = Hexagon(new_hexagon_point)
                    neighbors_to_add = []
                    R = closest_hexagon.R
                    for neighbor in hexagons:
                        distance = math.dist(new_hexagon.get_center(), neighbor.get_center())
                        if distance < 2 * R:
                            neighbors_to_add.append(neighbor)
                    new_hexagon.add_neighbors(neighbors_to_add)
                    hexagons.append(new_hexagon)
            else:
                if clicked_hexagon:
                    if event.button == 1:
                        print('Робот создан')
                        robot_already_created = True
                        start_already_created = True
                        clicked_hexagon.set_is_start()
                        robot_center = (mouse_x, mouse_y)
                        robot = Robot(robot_center, clicked_hexagon)
                    elif event.button == 2:
                        print(f'id текущего {clicked_hexagon.get_id()} сам объект {clicked_hexagon}')
                        print(clicked_hexagon.get_neighbors())
                    elif event.button == 3:
                        finish_already_created = True
                        clicked_hexagon.set_is_finish()
                else:
                    print('В этом месте нельзя создать робота')

    screen.fill((255, 255, 255))  # Заполнение экрана белым цветом

    # Текст в левом верхнем углу
    hints = [
        "1. Закрытие приложения (ESC)",
        "2. Создание шестиугольника (ЛКМ на пустую область)",
        "3. Увеличение значения проходимости шестиугольника (ЛКМ)",
        "4. Уменьшение значения проходимости шестиугольника (ПКМ)",
        "5. Удаление шестиугольника (Колесико мыши)",
        "6. Включение/Выключение редактирования карты (g)"
    ]

    # Текст в правом верхнем углу
    variable_text = f"Число шестиугольников на карте: {len(hexagons)}"
    variable_text_rendered = font.render(variable_text, True, (0, 0, 0))
    variable_text_rect = variable_text_rendered.get_rect()
    variable_text_rect.topright = (screen_width - 10, 10)

    if map_already_created is False:
        bottom_left_text = font.render('Режим редактирования карты', True, (139, 0, 0))
    else:
        bottom_left_text = font.render('Карта создана', True, (0, 100, 0))
    bottom_left_text_rect = bottom_left_text.get_rect()
    bottom_left_text_rect.bottomleft = (10, screen_height - 10)
    screen.blit(bottom_left_text, bottom_left_text_rect)

    # Отображение текста в правом верхнем углу
    screen.blit(variable_text_rendered, variable_text_rect)

    # Отображение текста в левом верхнем углу
    y_position = 10  # Начальная позиция по вертикали
    for hint in hints:
        text = font.render(hint, True, (0, 0, 0))
        screen.blit(text, (10, y_position))
        y_position += 25  # Увеличиваем позицию для следующей подсказки

    # Отрисовка всех Hexagon
    for hexagon in hexagons:
        pygame.draw.polygon(screen, hexagon.get_color(), hexagon.get_corners())
        pygame.draw.lines(screen, hexagon.get_outline_color(), True, hexagon.get_corners(),
                          hexagon.get_outline_width())
        text = font.render(str(hexagon.get_passability()), True, hexagon.get_outline_color())
        text_rect = text.get_rect(center=hexagon.get_center())
        screen.blit(text, text_rect)

        text_id = font.render(str(hexagon.get_id()), True, (0, 0, 255))  # Синий цвет
        text_id_rect = text_id.get_rect(topleft=hexagon.get_corners()[3])  # Верхний левый угол
        screen.blit(text_id, text_id_rect)

    if map_already_created is True and start_already_created is True and finish_already_created is True and robot_already_created is True:
        ready_to_go = True
    else:
        ready_to_go = False

    if go is True:
        # Робот двигается по маршруту
        if robot_index < len(path):
            target_hexagon = path[robot_index]
            target_point = target_hexagon.get_center()
            robot.set_target(target_point)
            robot.update()  # Обновление координат робота
            robot.draw(screen)

            # Проверка, достиг ли робот целевого шестиугольника
            if math.dist(robot.center, target_point) < Robot.MOVE_SPEED:
                robot_index += 1

    # Отрисовка робота
    if robot_already_created is True and go is False:
        robot.draw(screen)

    if ready_to_go is True and go is False:
        bottom_right_text = font.render('Нажмите пробел для запуска', True, (0, 100, 0))
        bottom_right_text_rect = bottom_right_text.get_rect()
        bottom_right_text_rect.bottomright = (screen_width - 10, screen_height - 10)
        screen.blit(bottom_right_text, bottom_right_text_rect)

    pygame.display.flip()  # Обновление экрана
    clock.tick(60)  # Частота обновления экрана
