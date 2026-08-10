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

