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