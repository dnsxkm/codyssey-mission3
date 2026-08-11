import json
from main import make_cross, make_x


def make_tie_13():
    n = 13
    cross = make_cross(n)
    x = make_x(n)
    grid = [[0.0] * n for _ in range(n)]

    # Cross만 밟는 칸 1곳에 0.9 → Cross 점수 = 0.9 (오차 없이 딱 떨어짐)
    for r in range(n):
        done = False
        for c in range(n):
            if cross[r][c] == 1 and x[r][c] == 0:
                grid[r][c] = 0.9
                done = True
                break
        if done:
            break

    # X만 밟는 칸 9곳에 0.1씩 -> X 점수 = 0.1*9 = 0.8999999999
    placed = 0
    for r in range(n):
        for c in range(n):
            if x[r][c] == 1 and cross[r][c] == 0 and placed < 9:
                grid[r][c] = 0.1
                placed += 1
    return grid


data = {
    'filters': {
        'size_5':  {'cross': make_cross(5),  'x': make_x(5)},
        'size_13': {'cross': make_cross(13), 'x': make_x(13)},
        'size_25': {'cross': make_cross(25), 'x': make_x(25)},
    },
    'patterns': {
        'size_5_1':  {'input': make_x(5),     'expected': 'x'},
        'size_5_2':  {'input': make_cross(5),  'expected': '+'},
        'size_5_3':  {'input': make_cross(5),  'expected': '+'},
        'size_13_1': {'input': make_tie_13(),  'expected': 'x'},
        'size_13_2': {'input': make_cross(13), 'expected': 'cross'},
        'size_13_3': {'input': make_x(13),     'expected': 'x'},
        'size_25_1': {'input': make_cross(25), 'expected': '+'},
        'size_25_2': {'input': make_x(25),     'expected': 'x'},
    },
}

with open('data.json', 'w') as f:
    json.dump(data, f, indent=2)

print('data.json 생성 완료')
