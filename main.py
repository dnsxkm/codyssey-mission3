import time

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
        print('(모드2는 아직 준비 중)') # 다음 단계에서 run_mode2()로 교체
    else:
        print('1 또는 2를 선택하세요.')

if __name__ == '__main__':
    main()