from math import dist
SCALE = 25

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
    square_side = round(radius * SCALE * 2)
    parts = []

    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            range_y = i + square_side
            range_x = j + square_side

            values_of_part_of_matrix = []
            for arr in matrix[i:range_y]:
                values_of_part_of_matrix += arr[j:range_x] 

            params = {
                "start_point": [i, j],
                "number_of_zeros": values_of_part_of_matrix.count(0)
            }

            parts.append(params)

    parts.sort(reverse=1, key=lambda p: p["number_of_zeros"])

    needed_start_point = parts[0]["start_point"]
    return needed_start_point


def get_center(start_point: list[int], radius: float) -> list[int]:
    start_y, start_x = start_point
    center = [start_x + radius * SCALE, start_y + radius * SCALE]
    return center


def fill_max_free_space(matrix: list[list[int]], radius: float):
    square_side = round(radius * SCALE * 2)
    
    start_point = get_start_point(matrix, radius)
    start_y, start_x = start_point
    center = get_center(start_point, radius)
    print(f"Центр базовой станции: {center[0] / SCALE}, {center[1] / SCALE}")

    range_y = min(start_y + square_side, len(matrix))
    range_x = min(start_x + square_side, len(matrix[0]))

    for i in range(start_y, range_y):
        for j in range(start_x, range_x):
            distance = dist(center, [j, i])
            if distance <= radius * SCALE:
                matrix[i][j] = 1


def get_count_of_zeros(matrix: list[list[int]]) -> int:
    return sum([arr.count(0) for arr in matrix])


def main():
    width, height = get_dimensions_from_file("./tests/1/test_rect.txt")
    stations = get_stations_from_file("./tests/1/test_radius.txt")
    used_stations = 0

    matrix = make_matrix(width * SCALE, height * SCALE)

    while len(stations) > 0 and get_count_of_zeros(matrix):
        print(f"Шаг №{used_stations + 1}")
        fill_max_free_space(matrix, stations[0])
        stations.pop(0)
        used_stations += 1

    print("Использовано станций: ", used_stations)

    zeros = get_count_of_zeros(matrix)
    total_area = len(matrix) * len(matrix[0])
    covered_area = total_area - zeros

    print(f"Покрыто {round(covered_area / total_area * 100)}%")


main()