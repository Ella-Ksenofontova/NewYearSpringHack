from math import dist, ceil, sqrt, floor
from random import randint
PRECISION_COEFFICIENT = 3

def get_dimensions_from_file(path: str) -> tuple[float]:
    with open(path) as rect_coords_file:
        width, height = map(int, rect_coords_file.readline().split())
        return width, height
    

def get_stations_from_file(path: str) -> list[float]:
    with open(path) as stations_file:
        stations = [round(float(s), 2) for s in stations_file.readlines()]
        stations.sort(reverse=1)
        return list(stations)
    

def make_matrix(w: int, h: int) -> list[list[int]]:
    columns = w
    rows = h

    matrix = []

    for i in range(rows):
        matrix.append([])
        for _ in range(columns):
            matrix[i].append(0)

    return matrix


def get_start_point(matrix: list[list[int]], radius: float) -> list[int]:
    square_side = round(radius * PRECISION_COEFFICIENT * 2)
    parts = []

    min_x = -floor(radius/2)
    min_y = -floor(radius/2)

    for i in range(min_y, len(matrix)):
        for j in range(min_x, len(matrix[0])):
            range_y = i + square_side
            range_x = j + square_side

            total_zeros = 0
            part_of_matrix = []
            for arr in matrix[max(0, i):range_y]:
                part_of_matrix.append(arr[max(0, j):range_x])
                total_zeros += arr[max(0, j):range_x].count(0)

            params = {
                "start_point": [i, j],
                "number_of_zeros": total_zeros - get_n_of_zeros_out_of_circle(part_of_matrix, radius, [i, j])
            }

            parts.append(params)

    parts.sort(reverse=1, key=lambda p: p["number_of_zeros"])

    needed_start_point = parts[0]["start_point"]
    return needed_start_point


def get_n_of_zeros_out_of_circle(matrix: list[list[int]], radius: float, start_point: list[int]) -> int:
    n = 0
    start_y, start_x = start_point
    square_side = round(radius * PRECISION_COEFFICIENT * 2)
    center = get_center(start_point, radius)
    
    max_center_y = len(matrix) - 1
    max_center_x = len(matrix[0]) - 1
    
    if center[0] > max_center_x or center[1] > max_center_y:
        if center[0] > max_center_x:
            start_x -= ceil(center[0] - max_center_x)
        if center[1] > max_center_y:
            start_y -= ceil(center[1] - max_center_y)
                
        center = get_center([start_y, start_x], radius)

    range_y = min(start_y + square_side, len(matrix))
    range_x = min(start_x + square_side, len(matrix[0]))

    for i in range(max(start_y, 0), range_y):
        for j in range(max(start_x, 0), range_x):
            distance = dist(center, [j, i])
            if radius * PRECISION_COEFFICIENT < distance <= PRECISION_COEFFICIENT * radius * sqrt(2) and matrix[i][j] == 0:
               n += 1
    return n


def get_center(start_point: list[int], radius: float) -> list[int]:
    start_y, start_x = start_point
    center = [start_x + radius * PRECISION_COEFFICIENT, start_y + radius * PRECISION_COEFFICIENT]
    return center


def fill_max_free_space(matrix: list[list[int]], radius: float):
    square_side = round(radius * PRECISION_COEFFICIENT * 2)
    
    start_point = get_start_point(matrix, radius)
    start_y, start_x = start_point
    center = get_center(start_point, radius)

    max_center_y = len(matrix) - 1
    max_center_x = len(matrix[0]) - 1
    
    if center[0] > max_center_x or center[1] > max_center_y:
        if center[0] > max_center_x:
            start_x -= ceil(center[0] - max_center_x)
        if center[1] > max_center_y:
            start_y -= ceil(center[1] - max_center_y)
                
        center = get_center([start_y, start_x], radius)

    print(f"Центр базовой станции: {round(center[0] / PRECISION_COEFFICIENT, 2)}, {round(center[1] / PRECISION_COEFFICIENT, 2)}")

    range_y = min(start_y + square_side, len(matrix))
    range_x = min(start_x + square_side, len(matrix[0]))

    for i in range(max(start_y, 0), range_y):
        for j in range(max(start_x, 0), range_x):
            distance = dist(center, [j, i])
            if distance <= radius * PRECISION_COEFFICIENT:
                matrix[i][j] = 1


def get_count_of_zeros(matrix: list[list[int]]) -> int:
    return sum([arr.count(0) for arr in matrix])


def main():
    width = randint(1, 50)
    height = randint(1, 50)
    number_of_stations = randint(1, 100)
    stations = [round(randint(1, 25) / randint(1, 5), 2) for _ in range(number_of_stations)]
    stations.sort(reverse=1)

    used_stations = 0

    matrix = make_matrix(width * PRECISION_COEFFICIENT, height * PRECISION_COEFFICIENT)
    print(f"Площадь района: {width * height} ({width}x{height})")

    while len(stations) > 0 and get_count_of_zeros(matrix):
        print(f"Шаг №{used_stations + 1}")
        print(f"Радиус базовой станции: {stations[0]}")
        fill_max_free_space(matrix, stations[0])
        stations.pop(0)
        used_stations += 1

    print(f"Использовано станций: {used_stations}/{number_of_stations}")

    zeros = get_count_of_zeros(matrix)
    total_area = len(matrix) * len(matrix[0])
    covered_area = total_area - zeros

    print(f"Покрыто {round(covered_area / total_area * 100)}%")


main()