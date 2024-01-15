def graph(hexagons):
    """
    Создает граф, представленный в виде словаря, где ключи - это шестиугольники,
    а значения - словари соседей и их проходимостью.

    Parameters:
    - hexagons (list): Список шестиугольников.

    Returns:
    - dict: Граф в виде словаря.
    """
    graph = {}
    for hexagon in hexagons:
        neighbors = hexagon.get_neighbors().values()
        graph[hexagon] = {neighbor: neighbor.get_passability() for neighbor in neighbors}

    return graph


def bellman_ford(graph, start, finish):
    """
    Реализует алгоритм Беллмана-Форда для поиска кратчайшего пути в графе.

    Parameters:
    - graph (dict): Граф в виде словаря.
    - start: Начальный узел.
    - finish: Конечный узел.

    Returns:
    - list: Кратчайший путь от start до finish.
    """
    vertices = graph.keys()
    distance = {v: float('inf') for v in vertices}
    distance[start] = 0
    predecessor = {v: None for v in vertices}

    # Выполняем (V-1) итераций
    for _ in range(len(vertices) - 1):
        updated = False  # Переменная для отслеживания обновлений в этой итерации
        for u in vertices:
            for v, w in graph[u].items():
                if distance[u] != float('inf') and distance[u] + w < distance[v]:
                    distance[v] = distance[u] + w
                    predecessor[v] = u
                    updated = True  # Обновление произошло

        if not updated:
            break  # Нет обновлений, выходим из цикла

    # Проверка наличия отрицательных циклов
    for u in vertices:
        for v, w in graph[u].items():
            if distance[u] != float('inf') and distance[u] + w < distance[v]:
                print("Граф содержит отрицательный цикл")

                # Найти и вывести отрицательный вес цикла
                cycle = find_negative_cycle(u, predecessor)
                print("Отрицательный вес цикла:", cycle)
                return None

    # Формирование пути
    path = []
    current = finish
    while current is not None:
        path.insert(0, current)
        current = predecessor[current]

    print(f"Кратчайшее расстояние от {start.get_id()} до {finish.get_id()}: {distance[finish]}")
    print("Путь:", [hexagon.get_id() for hexagon in path])
    return path


def find_negative_cycle(start, predecessor):
    """
    Находит отрицательный цикл в графе.

    Parameters:
    - start: Начальный узел.
    - predecessor (dict): Словарь предшественников.

    Returns:
    - list: Список узлов образующих отрицательный цикл.
    """
    cycle = []
    current = start
    while current not in cycle:
        cycle.append(current)
        current = predecessor[current]
    cycle = cycle[cycle.index(current):]
    return cycle
