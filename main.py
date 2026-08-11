import time
import json

def read_grid(n, name):
    """"
    nxn 그리드를 콘솔에서 한 줄씩(공백 구분) 입력받아 2차원 리스트로 반환한다.
    줄 수/칸 수가 안 맞거나 숫자가 아니면 안내 후 처음부터 다시 받는다.
    name: 무엇을 입력받는지 안내함. (예: "필터A")
    """

    while True:
        print(f"{name} ({n}줄 입력, 공백 구분)")
        rows = []
        ok = True

        for _ in range(n):
            line = input()
            parts = line.split() # 공백 기준으로 쪼갠 후
            if len(parts) != n: # 개수가 n개인지 확인한다.
                print(f"입력 형식 오류: 각 줄에 {n}개의 숫자를 공백으로 구분해 입력하세요.")
                ok = False
                break

            try:
                row = [float(p) for p in parts]
            except ValueError:
                print('입력 형식 오류: 숫자만 입력하세요.')
                ok = False
                break
            rows.append(row)

        if ok:
            return rows
        # ok 가 False면 while 처음으로 돌아가 다시 입력 받음

def mac(pattern, filt):

    """
    패턴과 필터를 같은 위치끼리 곱하고(Multiply) 전부 더한다(Accumulate).
    두 배열은 같은 nxn 크기라고 가정한다 (크기 검증은 호출하는 쪽에서)
    변환 : 유사도 점수 (float)
    """
    n = len(pattern)
    score = 0.0 # 항상 float 으로 만들기 위해서
    for r in range(n):
        for c in range(n):
            score += pattern[r][c] * filt[r][c]
    return score

def make_cross(n):
    """nxn 십자가(Cross) 패턴 생성: 가운데 행/열이 1, 나머지 0"""
    mid = n // 2
    grid = []
    for r in range(n):
        row = []
        for c in range(n):
            if (r==mid) or (c==mid):
                row.append(1)
            else:
                row.append(0)
        grid.append(row)

    return grid

def make_x(n):
    """nxn X패턴 생성: 두 대각선이 1, 나머지 0"""
    grid = []
    for r in range(n):
        row = []
        for c in range(n):
            if (r==c) or (r+c == n-1):
                row.append(1)
            else:
                row.append(0)

        grid.append(row)

    return grid




def measure_mac(pattern, filt, repeat=10):
    """
    mac(pattern, filt)를 repeat회 반복 실행하고 평균 시간을 ms로 반환한다.
    I/O를 제외하고 연산 함수 호출 구간만 측정한다.
    """
    start = time.perf_counter()
    for _ in range(repeat):
        mac(pattern, filt)
    end = time.perf_counter()
    total_seconds = end - start
    avg_ms = (total_seconds / repeat) * 1000
    return avg_ms


EPSILON = 1e-9 # <--- 이 값은 모드1 , 모드2 에서도 씀. 상수로 박아두면 나중에 바꿀 때, 한줄만 고치면 된다.
# 코드 최상단에 상수로 정의한 것.

def decide(score_a, score_b):
    """
    두 점수를 epsilon 기반으로 비교해 판정한다.
    차이가 EPSILON 보다 작으면 동점 -> 'UNDECIDE'
    아니면 더 높은 쪽 반환 : 'A' 또는 'B'
    """

    if abs(score_a - score_b) < EPSILON :
        return 'UNDECIDED'
    if score_a > score_b :
        return 'A'
    return 'B'

def extract_n(key):
    """ 'size_13_1' 같은 키에서 N(정수)을 추출한다. -> 13 """
    parts = key.split('_')
    return int(parts[1])

def normalize_label(raw):
    """
    입력 라벨을 표준 라벨('Cross' 또는 'X')로 정규화한다.
    '+', 'cross' -> 'Cross' / 'x' -> 'X'
    """
    s = str(raw).strip().lower()
    if s in ('+', 'cross'):
        return 'Cross'
    if s == 'x':
        return 'X'
    return None # 알 수 없는 라벨

# ------------------------------------------------------------------------

def run_mode1():
    """모드1: 사용자 입력(3x3) 흐름"""
    print('#--------------------------------------')
    print('# [1] 필터 입력')
    print('#--------------------------------------')
    filter_a = read_grid(3, '필터A')
    filter_b = read_grid(3, '필터B')

    print('#--------------------------------------')
    print('# [2] 패턴 입력')
    print('#--------------------------------------')
    pattern = read_grid(3, '패턴')

    print('#--------------------------------------')
    print('# [3] MAC 결과')
    print('#--------------------------------------')
    score_a = mac(pattern, filter_a)
    score_b = mac(pattern, filter_b)
    result = decide(score_a, score_b)

    print(f"A 점수: {score_a}")
    print(f"B 점수: {score_b}")
    if result == 'UNDECIDED':
        print('판정불가 ( |A-B| < 1e-9 )')
    else:
        print(f"판정: {result}")

    print('#--------------------------------------')
    print('# [4] 성능 분석 (평균/10회)')
    print('#--------------------------------------')
    avg_ms = measure_mac(pattern, filter_a)
    n = len(pattern)
    print(f'연산 시간(평균/10회): {avg_ms:.3f} ms')
    print(f'크기: {n}×{n} / 연산 횟수(N²): {n * n}')

# ------------------------------------------------------------------------

def run_mode2():
    """ 모드 2: data.json 로드 -> 판정 -> PASS/FAIL -> 요약. """
    # [1] 파일 로드 (크래시 방지)
    print('#--------------------------------------')
    print('# [1] 필터 로드')
    print('#--------------------------------------')

    try:
        with open('data.json', 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print('오류: data.json 파일을 찾을 수 없습니다.')
        return
    except json.JSONDecodeError:
        print('오루: data.json 형식이 올바르지 않습니다.')
        return

    filters = data.get('filters', {})
    patterns = data.get('patterns', {})

    for size_key in filters:
        print(f"✓ {size_key} 필터 로드 완료 (Cross, X)")

    # [2] 패턴 분석
    print()
    print('#--------------------------------------')
    print('# [2] 패턴 분석 (라벨 정규화 적용)')
    print('#--------------------------------------')

    total = 0
    passed = 0
    failed = 0
    fail_cases = []

    for pat_key in patterns:
        total += 1
        print(f"--- {pat_key} ---")

        try: 
            entry = patterns[pat_key]
            pattern = entry['input']
            expected = normalize_label(entry['expected'])

            # 키에서 N 추출 -> size_N 필터 선택
            n = extract_n(pat_key)
            filt_key = f'size_{n}'
            if filt_key not in filters:
                raise ValueError(f'{filt_key} 필터가 없습니다.')
            cross_filter = filters[filt_key]['cross']
            x_filter = filters[filt_key]['x']

            # 크기 검증
            if (len(pattern) != n) or (any(len(row) != n for row in pattern)):
                raise ValueError(f"크기 불일치 (필터 {n}, 패턴 {len(pattern)})")

            # MAC 2번
            score_cross = mac(pattern, cross_filter)
            score_x = mac(pattern, x_filter)

            # 판정 (decide의 A/B 를 Cross/x 로 매핑)
            ab = decide(score_cross, score_x)
            if ab == 'A':
                verdict = 'Cross'
            elif ab == 'B':
                verdict = 'X'
            else:
                verdict = 'UNDECIDED'

            # PASS/FAIL
            print(f"Cross 점수: {score_cross}")
            print(f"X 점수: {score_x}")
            if verdict == expected:
                print(f"판정: {verdict} | expected: {expected} | PASS")
                passed += 1
            else:
                reason = '동점 규칙' if verdict == 'UNDECIDED' else '판정 불일치'
                print(f"판정: {verdict} | expected: {expected} | FAIL: ({reason})")
                failed += 1
                fail_cases.append((pat_key, reason))
        except Exception as e:
            print(f"FAIL 오류: {e}")
            failed += 1
            fail_cases.append((pat_key, str(e)))

    # [3] 성능 분석
    print()
    print('#--------------------------------------')
    print('# [3] 성능 분석 (평균/10회)')
    print('#--------------------------------------')
    print('크기      평균 시간(ms)   연산 횟수')
    print('-----------------------------------')
    for size in [3, 5, 13, 25]:
        p = make_cross(size)
        f = make_cross(size)
        avg_ms = measure_mac(p, f)
        print(f'{size}x{size}       {avg_ms:.3f}        {size * size}')


    # [4] 결과 요약
    print()
    print('#--------------------------------------')
    print('# [4] 결과 요약')
    print('#--------------------------------------')
    print(f"총 테스트: {total}개")
    print(f"통과: {passed}개")
    print(f"실패: {failed}개")
    if fail_cases:
        print()
        print('실패 케이스')
        for key, reason in fail_cases:
            print(f"- {key}: {reason}")


# ------------------------------------------------------------------------


def main():
    """프로그램 진입점: 모드 선택 후 해당 모드 실행"""
    print("=== Mini NPU Simulator. ===")
    print()
    print('[모드 선택]')
    print()
    print('1. 사용자 입력(3x3')
    print('2. data.json 분석')
    choice = input().strip()

    if choice == '1':
        run_mode1()
    elif choice == '2':
        run_mode2() # 다음 단계에서 run_mode2()로 교체
    else:
        print('1 또는 2를 선택하세요.')

if __name__ == '__main__':
    main()